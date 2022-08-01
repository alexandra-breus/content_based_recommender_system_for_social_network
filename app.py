import os
from dotenv import load_dotenv
import pandas as pd
from typing import List
from fastapi import FastAPI
from datetime import datetime
from sqlalchemy import cast, func
from catboost import CatBoostClassifier

from schema import PostGet
from database import SessionLocal
from table_user import users
from table_post import posts
from table_feed import feed


with SessionLocal() as session:
    
    # делаем запрос в базу данных и берем данные всех пользователей
    user_query = session.query(users.user_id, users.gender, 
                                    users.age, users.country, users.city,
                                    users.exp_group, users.os, users.source) \
                                    .all()

    user = pd.DataFrame(user_query) 

    # делаем запрос в таблицу feed и берем id постов, отсортированных по убыванию количества лайков
    result = session.query(feed.post_id) \
                        .group_by(feed.post_id) \
                        .order_by((func.sum(feed.target)).desc()) \
                        .all()

    top_posts = [x[0] for x in result]

    # достаем из таблицы posts 500 самых популярных постов для ускорения расчета рекомендаций
    post_query = session.query(posts.post_id, posts.text, posts.topic) \
        .filter(posts.post_id.in_(top_posts)) \
        .limit(500) \
        .all()


    post = pd.DataFrame(post_query)

app = FastAPI() #запуск сервиса FastAPI

def get_model_path() -> str: #функция проверки, где исполняется код (на учебном сервере или локально)
    if os.environ["IS_LMS"] == "1": 
        MODEL_PATH = '/workdir/user_input/model'
    else:
        os.environ.get('MODEL_PATH') 
    return MODEL_PATH


async def load_features(id : int, time : datetime): 


    data = user.loc[user['user_id'] == id].merge(post, how='cross') #отбираем признаки о пользователе по id


    if time.hour in (7, 8, 9): #создаем признаки is_morning и is_eve используя timestamp из запроса

        data['is_morning'] = 1

    else:

        data['is_morning'] = 0

    if time.hour in (19, 20, 21, 22):

        data['is_eve'] = 1

    else:

        data['is_eve'] = 0

    return data



async def load_models(): #загружаем заранее обученный catboost

    model_path = get_model_path()

    from_file = CatBoostClassifier()

    return from_file.load_model(model_path)


@app.get("/post/recommendations/", response_model=List[PostGet]) # GET endpoint дающий топ-k рекомендаций постов для пользователя user_id = id 
                                                                 # на момент времени time
async def recommended_posts(
		id: int, 
		time : datetime, 
		limit: int = 10) -> List[PostGet]:

    
    model = await load_models()

    data = await load_features(id, time)

    # предсказываем вероятности для выбранных постов
    data['predict'] = model.predict_proba(data.drop(['user_id', 'post_id'], axis=1))[:, 1]

    # создаем датафрейм с топ-k рекомендациями через сортировку вероятностей

    result = data.nlargest(limit,'predict')[['post_id', 'text', 'topic']].rename({'post_id' : 'id'}, axis=1).to_dict(orient='records')


    return result


