from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Boolean, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class APICall(Base):
    __tablename__ = 'api_calls'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    provider = Column(String)  # 'openai' or 'anthropic'
    model = Column(String)
    prompt = Column(String)
    response = Column(String)
    success = Column(Boolean)
    error = Column(String, nullable=True)
    latency = Column(Float)  # in seconds
    tokens_used = Column(Integer)
    cost_usd = Column(Float)

engine = create_engine('sqlite:///api_calls.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def log_api_call(provider, result):
    session = Session()
    try:
        api_call = APICall(
            provider=provider,
            model=result.get('model'),
            prompt=result.get('prompt'),
            response=result.get('response'),
            success=result.get('success'),
            error=result.get('error') if not result.get('success') else None,
            latency=result.get('metrics', {}).get('latency', 0) if result.get('success') else 0,
            tokens_used=result.get('metrics', {}).get('tokens', 0) if result.get('success') else 0,
            cost_usd=result.get('metrics', {}).get('cost_usd', 0) if result.get('success') else 0
        )
        session.add(api_call)
        session.commit()
    finally:
        session.close()

def get_api_stats():
    session = Session()
    try:
        total_calls = session.query(APICall).count()
        successful_calls = session.query(APICall).filter_by(success=True).count()
        total_cost = session.query(APICall).filter_by(success=True).with_entities(
            func.sum(APICall.cost_usd)).scalar() or 0
        
        return {
            'total_calls': total_calls,
            'successful_calls': successful_calls,
            'failed_calls': total_calls - successful_calls,
            'total_cost_usd': total_cost
        }
    finally:
        session.close()