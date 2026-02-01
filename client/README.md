# Astra Web Client

Simple web interface for Astra Voice Assistant.

## Features

- User registration and authentication
- Send text commands to Astra
- View conversation history
- Clean, modern UI

## Usage

1. Start the Astra backend:
   ```bash
   cd ../
   docker compose up --build
   ```

2. Open `index.html` in your browser

3. Register a new account or login

4. Start chatting with Astra!

## API Configuration

The client connects to `http://localhost:8000` by default. To change this, edit the `API_BASE` variable in `index.html`.

## Future Enhancements

- Voice input (Speech-to-Text)
- Voice output (Text-to-Speech)
- Reminder management UI
- Conversation history persistence
- Dark mode
- Mobile-responsive design improvements
