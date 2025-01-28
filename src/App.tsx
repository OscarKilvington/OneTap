import { useState } from 'react';
import { Container, Box, CssBaseline, ThemeProvider, createTheme } from '@mui/material';
import ChatWindow from './components/ChatWindow';
import ModelSelector from './components/ModelSelector';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
  },
});

function App() {
  const [currentModel, setCurrentModel] = useState('gpt4');

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="lg">
        <Box sx={{ py: 4 }}>
          <Box sx={{ mb: 2 }}>
            <ModelSelector
              currentModel={currentModel}
              onModelChange={setCurrentModel}
            />
          </Box>
          <ChatWindow />
        </Box>
      </Container>
    </ThemeProvider>
  )
}

export default App
