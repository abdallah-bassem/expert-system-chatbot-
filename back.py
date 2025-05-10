import os
import json
import logging
import uuid
from flask import Flask, request, jsonify, send_from_directory, Response, stream_with_context, session
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = '369'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

api_key = "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"

if not api_key or not api_key.startswith("gsk_"):
    logger.error("Groq API key not configured properly. Please set the GROQ_API_KEY environment variable or update the script.")
client = Groq(api_key=api_key)

current_directory = os.path.dirname(os.path.abspath(__file__))
conversations = {}

system_prompt = ("You are a helpful, general-purpose AI assistant. Engage in conversation, answer questions, provide explanations, and assist with various tasks to the best of your abilities. Strive to be clear, informative, and friendly.")

def get_or_create_conversation(session_id):
    if session_id not in conversations:
        conversations[session_id] = [{"role": "system", "content": system_prompt}]
        logger.info(f"New conversation created for session_id: {session_id}")
    return conversations[session_id]

@app.route('/')
def index():
    logger.info(f"Serving index.html from {current_directory}")
    return send_from_directory(current_directory, 'index.html')

@app.route('/api/create_session', methods=['GET'])
def create_session():
    session_id = str(uuid.uuid4())
    session['session_id'] = session_id
    conversations[session_id] = [{"role": "system", "content": system_prompt}]
    logger.info(f"Created new session: {session_id}")
    return jsonify({"session_id": session_id, "message": "Session created successfully."}), 200

@app.route('/api/query', methods=['POST'])
def query():
    logger.info("Received query request.")
    if not session.get('session_id'):
        logger.info("No active session found for query, creating a new one.")
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id
        conversations[session_id] = [{"role": "system", "content": system_prompt}]
    else:
        session_id = session['session_id']
        if session_id not in conversations:
            logger.info(f"Session ID {session_id} found in session cookie, but not in memory. Re-initializing conversation.")
            conversations[session_id] = [{"role": "system", "content": system_prompt}]

    user_query = request.form.get('query', '')
    if not user_query.strip():
        logger.warning(f"Empty query received for session {session_id}.")
        return jsonify({"error": "Query cannot be empty."}), 400

    logger.info(f"Query from session {session_id}: \"{user_query[:100]}{'...' if len(user_query) > 100 else ''}\"")
    conversation_history = get_or_create_conversation(session_id)
    
    user_message_content = [{"type": "text", "text": user_query}]
    conversation_history.append({"role": "user", "content": user_message_content})

    def generate(current_conversation_history, s_id):
        try:
            logger.info(f"Starting Groq stream for session {s_id}. Conversation length: {len(current_conversation_history)} messages.")
            stream = client.chat.completions.create(
                model='meta-llama/llama-4-scout-17b-16e-instruct',
                messages=current_conversation_history,
                temperature=0.7,
                stream=True
            )
            assistant_response_parts = []
            for chunk in stream:
                if chunk.choices[0].delta and chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    assistant_response_parts.append(content)
                    yield f"data: {json.dumps({'content': content})}\n\n"

            assistant_full_response = "".join(assistant_response_parts)
            current_conversation_history.append({"role": "assistant", "content": assistant_full_response})
            logger.info(f"Groq stream finished for session {s_id}. Assistant response length: {len(assistant_full_response)} chars.")
            yield f"data: {json.dumps({'event': 'stream_end'})}\n\n"
        except Exception as e:
            logger.error(f"Error in Groq stream for session {s_id}: {str(e)}", exc_info=True)
            yield f"data: {json.dumps({'error': f'An error occurred: {str(e)}'})}\n\n"

    return Response(stream_with_context(generate(conversation_history, session_id)), content_type='text/event-stream')

@app.route('/api/reset_conversation', methods=['POST'])
def reset_conversation():
    old_session_id = session.get('session_id')
    if old_session_id:
        if old_session_id in conversations:
            conversations.pop(old_session_id, None)
            logger.info(f"Cleared conversation history for old session: {old_session_id}")
        session.pop('session_id', None)
        logger.info(f"Cleared session cookie for old session: {old_session_id}")

    new_session_id = str(uuid.uuid4())
    session['session_id'] = new_session_id
    conversations[new_session_id] = [{"role": "system", "content": system_prompt}]
    logger.info(f"Conversation reset. New session created: {new_session_id}")
    return jsonify({"message": "Conversation reset successfully.", "session_id": new_session_id}), 200

if __name__ == '__main__':
    logger.info("Starting Flask app...")
    app.run(host='0.0.0.0', port=5000, debug=True)