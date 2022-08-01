from database import Base
from sqlalchemy import Column, String, Integer


class posts(Base):

    __tablename__ = 'post_text_df'
    __table_args__ = {'schema': 'public'}


    post_id = Column(Integer, primary_key=True)
    text = Column(String)
    topic = Column(String)