# Kira Client

## Overview

Kira Client is an AI-driven application designed for automating IoT tasks using voice commands. It listens for a specific trigger word, processes spoken instructions to comprehend user intent, and executes actions on IoT devices. The application integrates with OpenAI's API for advanced intent recognition

## Key Features
- **Voice Activation**: Activates upon hearing a pre-defined trigger word.
- **Audio Capture & Analysis**: Records and analyzes spoken instructions.
- **Advanced Intent Recognition**: Leverages OpenAI API to accurately interpret user intents.
- **Dynamic IoT Interaction**: Sends requests to IoT devices based on interpreted intents.
- **Visual Feedback System**: Uses an LED strip to provide visual status updates.

## Enhanced Intent Recognition
Kira Client utilizes a sophisticated intent recognition system powered by OpenAI. The system interprets user commands based on a configured list of intents. Each intent includes a name, description, and associated action.

Example intent configuration:
```json
[
  {
    "name": "NewMeeting",
    "description": "create a new meeting",
    "action": {
      "type": "request",
      "options": {
        "url": "http://localhost:8090/execute?name=Create Google Meet",
        "method": "GET"
      }
    }
  }
]
```

## Workflow
1. Waits for the trigger word to start the listening mode.
2. Records and transcribes the subsequent spoken instructions.
3. The OpenAIClient interprets the intent using the provided template.
4. Executes actions on IoT devices based on the recognized intent

## HTTP Server Functionality
Kira Client incorporates an HTTP server to manage voice trigger detection and initiate intent recognition.

### Key Endpoints
- `/intents/start-recognition`: Pauses the voice trigger detector and starts listening for text to recognize the intent.

## Installation

### Prerequisites
- Python 3.11+
- Poetry
- PortAudio

### Steps
1. Clone the repository
2. Install dependencies using Poetry
```bash
poetry install
```
3. Run the application
```bash
poetry run python kira_client/main.py
```

## License
This project is licensed under the MIT License - [MIT license](/LICENSE).