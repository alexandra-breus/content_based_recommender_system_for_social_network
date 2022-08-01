from database import Base
from sqlalchemy import Column, String, Integer

class users(Base):
    
    __tablename__ = 'user_data'
    __table_args__ = {'schema': 'public'}

    user_id = Column(Integer, primary_key=True)
    gender = Column(Integer)
    age = Column(Integer)
    country = Column(String)
    city = Column(String)
    exp_group = Column(Integer)
    os = Column(String)
    source = Column(String)