from flask import Flask, render_template, request, jsonify, session
from gpt import GPTAssistant
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def index():
    # Generate a unique session_id during the first request
    if 'session_id' not in session:
        assitant = GPTAssistant()
        session['session_id'] = assitant.session_id

    return render_template('chat.html')

@app.route("/get", methods=["POST"])
def chat():
    msg = request.form["msg"]
    
    # Retrieve session_id from the session
    try:
        session_id = session.get('session_id', None)
        assitant = GPTAssistant(session_id)
    except:
        assitant = GPTAssistant()
        session['session_id'] = assitant.session_id       
    bot_response = assitant.gpt_response(msg)

    return bot_response


if __name__ == '__main__':
    app.run()
