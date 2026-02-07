from sqlalchemy import Column, Integer, String, DateTime
from app.db import Base
import datetime

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer)
    user_id = Column(Integer)
    content = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
