
from database import Base
from sqlalchemy import Column, String, Integer, TIMESTAMP

class feed(Base):

    __tablename__ = 'feed_data'
    __table_args__ = {'schema': 'public'}


    timestamp = Column(TIMESTAMP, primary_key=True)
    user_id = Column(Integer)
    post_id = Column(Integer)
    action = Column(String)
    target = Column(Integer)