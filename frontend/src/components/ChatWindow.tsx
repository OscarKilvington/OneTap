import React, { useState, useEffect } from 'react';
import { Box, Paper, TextField, IconButton, Typography, CircularProgress } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import AttachFileIcon from '@mui/icons-material/AttachFile';
import chatService, { Message, ChatResponse } from '../services/ChatService';

const ChatWindow: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentChatId, setCurrentChatId] = useState<string>();

  useEffect(() => {
    chatService.connect();

    const messageHandler = (response: ChatResponse) => {
      setIsLoading(false);
      setCurrentChatId(response.chatId);
      
      const newMessage: Message = {
        id: Date.now().toString(),
        content: response.content,
        role: 'assistant',
        model: response.model,
        provider: response.provider,
        timestamp: new Date(),
        metrics: response.metrics,
      };
      
      setMessages(prev => [...prev, newMessage]);
    };

    const errorHandler = (error: any) => {
      setIsLoading(false);
      console.error('Chat error:', error);
      // TODO: Add error notification
    };

    const unsubscribeMessage = chatService.onMessage(messageHandler);
    const unsubscribeError = chatService.onError(errorHandler);

    return () => {
      unsubscribeMessage();
      unsubscribeError();
      chatService.disconnect();
    };
  }, []);

  const handleSend = () => {
    if (!input.trim() || isLoading) return;

    const newMessage: Message = {
      id: Date.now().toString(),
      content: input,
      role: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, newMessage]);
    setInput('');
    setIsLoading(true);

    try {
      chatService.sendMessage(input, currentChatId);
    } catch (error) {
      console.error('Failed to send message:', error);
      setIsLoading(false);
    }
  };

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files && files.length > 0) {
      // TODO: Handle file upload
      console.log('File uploaded:', files[0].name);
    }
  };

  return (
    <Paper elevation={3} sx={{ height: '80vh', display: 'flex', flexDirection: 'column' }}>
      <Box sx={{ flexGrow: 1, overflow: 'auto', p: 2 }}>
        {messages.map((message) => (
          <Box
            key={message.id}
            sx={{
              display: 'flex',
              justifyContent: message.role === 'user' ? 'flex-end' : 'flex-start',
              mb: 2,
            }}
          >
            <Paper
              sx={{
                p: 2,
                backgroundColor: message.role === 'user' ? 'primary.light' : 'grey.100',
                maxWidth: '70%',
              }}
            >
              {message.model && (
                <Typography variant="caption" color="textSecondary" display="block">
                  {message.model} ({message.provider})
                </Typography>
              )}
              <Typography>{message.content}</Typography>
              {message.metrics && (
                <Typography variant="caption" color="textSecondary" display="block" sx={{ mt: 1, fontSize: '0.7rem' }}>
                  Tokens: {message.metrics.tokens_used} | 
                  Cost: ${message.metrics.cost_usd.toFixed(6)} | 
                  Latency: {message.metrics.latency_ms.toFixed(0)}ms
                </Typography>
              )}
            </Paper>
          </Box>
        ))}
        {isLoading && (
          <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
            <CircularProgress size={24} />
          </Box>
        )}
      </Box>
      <Box sx={{ p: 2, backgroundColor: 'background.default' }}>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <input
            type="file"
            id="file-upload"
            style={{ display: 'none' }}
            onChange={handleFileUpload}
            accept=".pdf,.png,.jpg,.csv"
          />
          <IconButton
            color="primary"
            component="label"
            htmlFor="file-upload"
          >
            <AttachFileIcon />
          </IconButton>
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
            disabled={isLoading}
          />
          <IconButton
            color="primary"
            onClick={handleSend}
            disabled={!input.trim() || isLoading}
          >
            {isLoading ? <CircularProgress size={24} /> : <SendIcon />}
          </IconButton>
        </Box>
      </Box>
    </Paper>
  );
};

export default ChatWindow;