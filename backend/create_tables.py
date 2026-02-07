from app.db import engine
from app.models.user import User
from app.models.message import Message

User.metadata.create_all(bind=engine)
Message.metadata.create_all(bind=engine)
