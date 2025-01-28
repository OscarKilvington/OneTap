import { io, Socket } from 'socket.io-client';

export interface Message {
  id?: string;
  content: string;
  role: 'user' | 'assistant';
  model?: string;
  provider?: string;
  timestamp?: Date;
}

export interface ChatResponse {
  chatId: string;
  content: string;
  role: 'assistant';
  model: string;
  provider: string;
}

class ChatService {
  private socket: Socket | null = null;
  private messageHandlers: ((message: ChatResponse) => void)[] = [];
  private errorHandlers: ((error: any) => void)[] = [];

  connect() {
    this.socket = io('http://localhost:59500', {
      path: '/ws/socket.io',
      transports: ['websocket'],
    });

    this.socket.on('connect', () => {
      console.log('Connected to chat server');
    });

    this.socket.on('message', (response: ChatResponse) => {
      this.messageHandlers.forEach(handler => handler(response));
    });

    this.socket.on('error', (error: any) => {
      this.errorHandlers.forEach(handler => handler(error));
    });

    this.socket.on('disconnect', () => {
      console.log('Disconnected from chat server');
    });
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }

  sendMessage(content: string, chatId?: string, taskType: string = 'general') {
    if (!this.socket) {
      throw new Error('Not connected to chat server');
    }

    this.socket.emit('message', {
      content,
      chatId,
      taskType,
    });
  }

  onMessage(handler: (message: ChatResponse) => void) {
    this.messageHandlers.push(handler);
    return () => {
      this.messageHandlers = this.messageHandlers.filter(h => h !== handler);
    };
  }

  onError(handler: (error: any) => void) {
    this.errorHandlers.push(handler);
    return () => {
      this.errorHandlers = this.errorHandlers.filter(h => h !== handler);
    };
  }
}

export const chatService = new ChatService();
export default chatService;