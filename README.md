# expert-system-chatbot-

A responsive and interactive AI chatbot application built with a Flask backend, Groq for AI-powered responses, and a modern HTML/CSS/JavaScript frontend. It supports session management, streaming responses, theme toggling, and conversation reset.

## Features

*   **AI-Powered Conversations:** Utilizes Groq API (specifically `meta-llama/llama-4-scout-17b-16e-instruct` model) for intelligent chat responses.
*   **Streaming Responses:** Bot replies are streamed in real-time for a smoother user experience.
*   **Session Management:** Maintains conversation history within a session using Flask sessions and in-memory storage.
*   **Modern UI:**
    *   Clean and responsive chat interface.
    *   Dark/Light theme toggle.
    *   Dynamic particle background effect.
*   **User Experience:**
    *   Typing indicator while the bot is generating a response.
    *   Auto-resizing text input area.
    *   Scroll-to-bottom button for long conversations.
    *   Clear input button.
*   **Conversation Control:** Ability to reset the conversation and start fresh.

## Technologies Used

*   **Backend:**
    *   Python
    *   Flask (Web framework, API endpoints)
    *   Groq Python SDK (Interface with Groq API)
    *   Flask-CORS (Cross-Origin Resource Sharing)
*   **Frontend:**
    *   HTML
    *   CSS (Styling, theme management, animations)
    *   JavaScript (DOM manipulation, API calls using Fetch, Server-Sent Events for streaming, particle effects)

## Project Structure


.
├── back.py # Flask backend server, API logic, Groq integration
└── index.html # Frontend HTML, CSS, and JavaScript

## Setup and Installation

1.  **Prerequisites:**
    *   Python 3.x
    *   `pip` (Python package installer)

2.  **Clone the repository (if you haven't already):**
    ```bash
    git clone https://github.com/abdallah-bassem/expert-system-chatbot-.git
    cd expert-system-chatbot-
    ```

3.  **Install Python dependencies:**
    ```bash
    pip install Flask Groq Flask-CORS
    ```
    *(Consider creating a `requirements.txt` file for easier dependency management: `Flask Groq Flask-CORS`)*

4.  **Configure Groq API Key:**
    For testing purposes, the Groq API key is currently added directly in the `back.py` file:
    ```python
    api_key = "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"
    ```
    Ensure this key is valid if you intend to run the application. For production or shared environments, it's best practice to manage API keys more securely, for example, using environment variables.

5.  **Run the backend server:**
    ```bash
    python back.py
    ```
    The server will start, typically on `http://0.0.0.0:5000/` or `http://127.0.0.1:5000/`. Check the console output for the exact address.

6.  **Access the chatbot:**
    Open your web browser and navigate to the address where the Flask app is running (e.g., `http://localhost:5000/`).

## How to Use

1.  Once the application is running and open in your browser, you'll see the chat interface.
2.  The bot will greet you with an initial message.
3.  Type your query or message in the input field at the bottom.
4.  Press `Enter` or click the send button (paper plane icon) to send your message.
5.  The bot's response will be streamed into the chat window.
6.  **Theme Toggle:** Click the moon/sun icon in the header to switch between dark and light themes.
7.  **Reset Conversation:** Click the refresh icon in the header to clear the current conversation history and start a new session.
