import socketio
from ..services.ai_service import AIService
from ..core.database import SessionLocal
from ..models.models import Chat, Message
import json

sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=[
        'http://localhost:51692',
        'http://localhost:55237'
    ]
)
app = socketio.ASGIApp(sio)

ai_service = AIService()

@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    
@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.event
async def message(sid, data):
    try:
        content = data.get('content')
        chat_id = data.get('chatId')
        task_type = data.get('taskType', 'general')
        
        # Store user message
        db = SessionLocal()
        if not chat_id:
            chat = Chat()
            db.add(chat)
            db.commit()
            chat_id = chat.id
        
        user_message = Message(
            chat_id=chat_id,
            content=content,
            role='user'
        )
        db.add(user_message)
        db.commit()
        
        # Generate AI response
        response = await ai_service.route_query(content, task_type)
        
        # Store AI response
        ai_message = Message(
            chat_id=chat_id,
            content=response['content'],
            role='assistant',
            model=response['model'],
            metadata={
                'provider': response['provider'],
                'metrics': response['metrics']
            }
        )
        db.add(ai_message)
        db.commit()
        
        # Send response back to client
        await sio.emit('message', {
            'chatId': chat_id,
            'content': response['content'],
            'role': 'assistant',
            'model': response['model'],
            'provider': response['provider'],
            'metrics': response['metrics']
        }, room=sid)
        
    except Exception as e:
        print(f"Error processing message: {str(e)}")
        await sio.emit('error', {'message': str(e)}, room=sid)
    finally:
        db.close()