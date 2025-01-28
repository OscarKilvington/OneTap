# OneTap - The Smart AI Aggregator

OneTap is a universal interface for AI, enabling individuals and businesses to seamlessly discover and use a range of AI models, agents, and tools through a single, intuitive chat interface. Rather than forcing users to pick from a confusing assortment of services, OneTap intelligently routes every query to the most suitable model.

## Features

- **Smart Model Routing**: Automatically directs queries to the most appropriate AI model based on task type
- **Real-time Chat Interface**: Seamless conversation with message history
- **Multi-Model Support**: 
  - OpenAI (GPT-4)
  - Anthropic (Claude)
  - Deepseek
- **File Processing**:
  - Support for PDF, PNG, JPG, CSV files
  - File content integration with chat context
- **Task Categories**:
  - Math
  - Data analytics
  - Programming
  - Creative writing
  - Translations
  - Search
  - Image generation
  - Text to Speech

## Tech Stack

- **Frontend**: 
  - React
  - Material-UI
  - Socket.IO Client
  - TypeScript

- **Backend**:
  - FastAPI
  - SQLite
  - Socket.IO
  - Python

## Getting Started

### Prerequisites

- Node.js (v16+)
- Python (v3.8+)
- API keys for:
  - OpenAI
  - Anthropic
  - Deepseek

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/OneTap.git
cd OneTap
```

2. Install frontend dependencies:
```bash
npm install
```

3. Install backend dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

4. Create a .env file in the root directory:
```env
DATABASE_URL=sqlite:///./onetap.db
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key
```

### Running the Application

1. Start the backend server:
```bash
python run.py
```

2. Start the frontend development server:
```bash
npm run dev
```

3. Visit http://localhost:52501 in your browser

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details
