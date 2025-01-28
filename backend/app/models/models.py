from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Chat(Base):
    __tablename__ = "chats"
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    messages = relationship("Message", back_populates="chat")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    content = Column(Text)
    role = Column(String)  # 'user' or 'assistant'
    model = Column(String, nullable=True)  # Which AI model generated this response
    created_at = Column(DateTime, default=datetime.utcnow)
    message_metadata = Column(JSON, nullable=True)  # Additional metadata like tokens, model settings
    
    chat = relationship("Chat", back_populates="messages")

class AIModel(Base):
    __tablename__ = "ai_models"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    provider = Column(String)  # 'openai', 'anthropic', 'deepseek'
    model_id = Column(String)  # e.g., 'gpt-4', 'claude-2'
    capabilities = Column(JSON)  # List of tasks this model can handle
    priority = Column(Integer)  # Ranking for task routing