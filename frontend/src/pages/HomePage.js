import React, { useState, useRef, useEffect } from 'react';
import { 
  Box, 
  Container, 
  Typography, 
  TextField, 
  IconButton, 
  List, 
  Avatar,
  CircularProgress,
  Tooltip,
  Zoom
} from '@mui/material';
import { 
  Send as SendIcon, 
  Mic as MicIcon, 
  MicOff as MicOffIcon,
  Person as PersonIcon,
  SmartToy as BotIcon
} from '@mui/icons-material';
import { format } from 'date-fns';

const MessageBubble = ({ message, isUser }) => {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: isUser ? 'flex-end' : 'flex-start',
        width: '100%',
        mb: 1,
      }}
    >
      <Box
        sx={{
          display: 'flex',
          flexDirection: isUser ? 'row-reverse' : 'row',
          alignItems: 'flex-start',
          maxWidth: '80%',
        }}
      >
        <Tooltip 
          title={isUser ? 'You' : 'Assistant'}
          placement={isUser ? 'left' : 'right'}
          TransitionComponent={Zoom}
        >
          <Avatar 
            sx={{ 
              bgcolor: isUser ? 'primary.main' : 'secondary.main',
              width: 32, 
              height: 32,
              m: 1
            }}
          >
            {isUser ? <PersonIcon fontSize="small" /> : <BotIcon fontSize="small" />}
          </Avatar>
        </Tooltip>
        
        <Box
          sx={{
            p: 2,
            bgcolor: isUser ? 'primary.light' : 'grey.100',
            color: isUser ? 'white' : 'text.primary',
            borderRadius: 2,
            position: 'relative',
            maxWidth: '100%',
            wordBreak: 'break-word',
            boxShadow: 1,
          }}
        >
          <Typography variant="body1">{message.text}</Typography>
          <Typography 
            variant="caption" 
            sx={{
              display: 'block',
              textAlign: 'right',
              mt: 0.5,
              opacity: 0.7,
              color: isUser ? 'rgba(255, 255, 255, 0.8)' : 'text.secondary',
              fontSize: '0.7rem'
            }}
          >
            {format(new Date(message.timestamp), 'h:mm a')}
          </Typography>
        </Box>
      </Box>
    </Box>
  );
};

const HomePage = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const messagesEndRef = useRef(null);

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

  // Load initial messages
  useEffect(() => {
    const fetchChatHistory = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/chat/history`);
        if (response.ok) {
          const data = await response.json();
          if (data.status === 'success' && data.history) {
            // Convert timestamp strings to Date objects
            const formattedHistory = data.history.map(msg => ({
              ...msg,
              timestamp: new Date(msg.timestamp)
            }));
            setMessages(formattedHistory);
          }
        }
      } catch (error) {
        console.error('Error fetching chat history:', error);
        // Fallback to default message if API fails
        setMessages([
          { 
            id: 1, 
            text: 'Hello! I\'m your VOICERAG assistant. How can I help you today?', 
            sender: 'bot',
            timestamp: new Date()
          }
        ]);
      }
    };

    fetchChatHistory();
  }, [API_BASE_URL]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (input.trim() === '' || isSending) return;
    
    // Add user message
    const userMessage = { 
      id: Date.now(), 
      text: input, 
      sender: 'user',
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsSending(true);
    
    try {
      // Send message to backend
      const response = await fetch(`${API_BASE_URL}/text`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: input })
      });
      
      if (!response.ok) {
        throw new Error('Failed to send message');
      }
      
      const data = await response.json();
      
      if (data.status === 'success' && data.response) {
        // Add bot response to messages
        setMessages(prev => [...prev, data.response]);
      } else {
        throw new Error('Invalid response format');
      }
    } catch (error) {
      console.error('Error sending message:', error);
      // Add error message
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, there was an error processing your message. Please try again.',
        sender: 'bot',
        isError: true,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsSending(false);
    }
  };

  const toggleVoiceInput = () => {
    // TODO: Implement voice input
    setIsListening(!isListening);
    // Show a temporary message about voice input
    if (!isListening) {
      const voiceMessage = {
        id: Date.now(),
        text: 'Voice input is not yet implemented. Please type your message instead.',
        sender: 'bot',
        isInfo: true,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, voiceMessage]);
    }
  };

  // Auto-scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <Container 
      maxWidth="md" 
      sx={{ 
        height: '100vh', 
        display: 'flex', 
        flexDirection: 'column',
        p: 0,
        bgcolor: 'background.default'
      }}
    >
      <Box 
        sx={{ 
          bgcolor: 'primary.main', 
          color: 'white',
          p: 2,
          boxShadow: 2,
          zIndex: 1
        }}
      >
        <Typography variant="h6" align="center" fontWeight="bold">
          VOICERAG Assistant
        </Typography>
      </Box>
      
      <Box 
        sx={{ 
          flex: 1, 
          overflow: 'hidden',
          display: 'flex',
          flexDirection: 'column',
          bgcolor: 'background.paper',
        }}
      >
        <List 
          sx={{ 
            flex: 1, 
            overflowY: 'auto',
            p: 2,
            '&::-webkit-scrollbar': {
              width: '6px',
            },
            '&::-webkit-scrollbar-track': {
              background: 'transparent',
            },
            '&::-webkit-scrollbar-thumb': {
              backgroundColor: 'rgba(0,0,0,0.2)',
              borderRadius: '3px',
            },
          }}
        >
          {messages.map((message) => (
            <MessageBubble 
              key={message.id} 
              message={message} 
              isUser={message.sender === 'user'}
            />
          ))}
          <div ref={messagesEndRef} />
        </List>
        
        <Box 
          component="form" 
          onSubmit={handleSendMessage} 
          sx={{ 
            p: 2, 
            borderTop: '1px solid',
            borderColor: 'divider',
            bgcolor: 'background.paper',
            position: 'relative'
          }}
        >
          <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
            <TextField
              fullWidth
              variant="outlined"
              placeholder="Type your message..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={isSending}
              size="small"
              sx={{
                '& .MuiOutlinedInput-root': {
                  borderRadius: '24px',
                  bgcolor: 'background.paper',
                  '& fieldset': {
                    borderColor: 'divider',
                  },
                  '&:hover fieldset': {
                    borderColor: 'primary.main',
                  },
                },
              }}
              onKeyPress={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSendMessage(e);
                }
              }}
            />
            <Tooltip title={isListening ? 'Stop listening' : 'Start voice input'}>
              <span>
                <IconButton 
                  color={isListening ? 'error' : 'default'}
                  onClick={toggleVoiceInput}
                  disabled={isSending}
                  sx={{
                    bgcolor: isListening ? 'error.light' : 'action.hover',
                    '&:hover': {
                      bgcolor: isListening ? 'error.main' : 'action.selected',
                    },
                  }}
                >
                  {isListening ? <MicOffIcon /> : <MicIcon />}
                </IconButton>
              </span>
            </Tooltip>
            <Tooltip title="Send message">
              <span>
                <IconButton 
                  type="submit" 
                  color="primary" 
                  disabled={!input.trim() || isSending}
                  sx={{
                    bgcolor: 'primary.main',
                    color: 'white',
                    '&:hover': {
                      bgcolor: 'primary.dark',
                    },
                    '&:disabled': {
                      bgcolor: 'action.disabledBackground',
                      color: 'action.disabled',
                    },
                  }}
                >
                  {isSending ? (
                    <CircularProgress size={24} color="inherit" />
                  ) : (
                    <SendIcon />
                  )}
                </IconButton>
              </span>
            </Tooltip>
          </Box>
          {isSending && (
            <Box sx={{ 
              position: 'absolute', 
              bottom: 0, 
              left: 0, 
              right: 0, 
              height: '2px',
              overflow: 'hidden',
            }}>
              <Box 
                sx={{
                  height: '100%',
                  width: '100%',
                  bgcolor: 'primary.main',
                  animation: 'progress 2s ease-in-out infinite',
                  '@keyframes progress': {
                    '0%': { transform: 'translateX(-100%)' },
                    '100%': { transform: 'translateX(100%)' },
                  },
                }}
              />
            </Box>
          )}
        </Box>
      </Box>
    </Container>
  );
};

export default HomePage;
