## content_based_recommender_system_for_social_network

***Финальный проект с курса START ML школы [Karpov.Courses](https://karpov.courses/)***

> **Главная задача проекта:** построить рекомендательную систему, которая 
> будет для каждого юзера в любой момент времени возвращать посты, которые пользователю покажут в ленте его соцсети.

**Метрика для оценки модели:**

![image](https://user-images.githubusercontent.com/36912961/182170314-1159aad1-2115-400e-96d0-f287477292ce.png)


**Пайплайн, который реализован в проекте**

1. Загрузка данных из БД в Jupyter notebook, обзор данных

2. Создание признаков и обучающей выборки

3. Тренировка модели в Jupyter notebook и оценка ее качества на валидационной выборке 

4. Сохранение модели 

5. Написание сервиса: загрузка модели -> получение признаков для модели по user_id -> предсказание постов, которые лайкнут -> возвращение ответа.

Стек, используемый при написании проекта:
+
+
+
+
___________________________________________

#### **Структура проекта**

* [app.py](app.py) - основной файл, в котором реализован API-сервис FastAPI для выдачи рекомендаций
* [EDA+catboost_training.ipynb](EDA+catboost_training.ipynb) - jupiter-notebook с предобработкой данных и обучением модели CatboostClassifier
* [catboost_model](catboost_model) - заранее обученная модель, сохраненная в файл
* [schema.py](schema.py) - описание класса `PostGet` как модели pydantic для валидации результатов запроса
* [table_feed.py](table_feed.py) -  описание класса `Feed`, который описывает таблицу `feed` на ORM
* [table_post.py](table_post.py) - описание класса `Posts`, который описывает таблицу `post` на ORM
* [table_user.py](table_user.py) - описание класса `Users`, который описывает таблицу `user` на ORM
* [database.py](database.py) - файл, отвечающий за сессии подключения к БД
* [requirements.txt](requirements.txt) - файл зависимостей приложения
* [.env.example](.env.example) - образец файла `.env`
___________________________________________

В качестве базовых сырых данных использовались таблицы `user`, `post`, `feed` из БД курса.

#### **Структура базы данных**

> Таблица `user` содержит данные о пользователях

![img](https://sun9-83.userapi.com/impg/ApsVGlL5COpZIMMiTJNND_D_pb4qz_b9UswLFg/otQpMcK4kUo.jpg?size=190x216&quality=95&sign=8485ffdd633d15fc7a80c971402a4c0b&type=album)

> Таблица `post` содержит данные о постах

![img2](https://sun9-66.userapi.com/impg/MFYVqytBlaamDmICWdlkFT5Q-eUwK4xSpW2ELw/utDw0DLjwk4.jpg?size=107x100&quality=95&sign=3c28810fff10277548dfabeef4773d59&type=album)

> Таблица `feed_action` содержит данные о взаимодействии пользователей с постами

![img3](https://sun9-81.userapi.com/impg/SKb6hnQjYFHQlQJL9kDdlsrpjsyLWSEKZ4Nj8A/9GH7iPfU_JM.jpg?size=285x117&quality=95&sign=d5b86fd87679b2392dc43d481396e8fa&type=album)
___________________________________________

#### Техническая спецификация
`Endpoint GET /post/recommendations/`

**Parameters**

|Parameter | Overview|
|----------|----------|
user_id   |	ID user’а для которого запрашиваются посты
time |	 Объект типа datetime: datetime.datetime(year=2021, month=1, day=3, hour=14)
limit	| Количество постов для юзера

**Response**
```
[{
  "id": 345,
  "text": "COVID-19 runs wild....",
  "topic": "news"
}, 
{
  "id": 134,
  "text": "Chelsea FC wins UEFA..",
  "topic": "news"
}, 
...]
```
______________________________________

#### **Содержание app.py**

1.
2.
3.
