# Import the necessary modules and create a Flask app
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import re
import random
app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app)

##### chatbot reply start
rules = {'I want (.*)': ['What would it mean if you got {0}',
  'Why do you want {0}',
  "What's stopping you from getting {0}"],
 'do you remember (.*)': ['Did you think I would forget {0}',
  "Why haven't you been able to forget {0}",
  'What about {0}',
  'Yes .. and?'],
 'do you think (.*)': ['if {0}? Absolutely.', 'No chance'],
 'if (.*)': ["Do you really think it's likely that {0}",
  'Do you wish that {0}',
  'What do you think about {0}',
  'Really--if {0}']}

def match_rule(rules, message):
    response, phrase = "default", None
    
    for pattern, responses in rules.items():
        match = re.search(pattern, message)
        if match is not None:
            response = random.choice(responses)
            if '{0}' in response:
                phrase = match.group(1)
    return response.format(phrase)

# Creating pronouns replacing fucntion
def replace_pronouns(message):

    message = message.lower()
    if 'me' in message:
        return re.sub('me', 'you', message)
    if 'my' in message:
        return re.sub('my', 'your', message)
    if 'your' in message:
        return re.sub('your', 'my', message)
    if 'you' in message:
        return re.sub('you', 'me', message)

    return message

# Creating response function
def respond(message):
    response, phrase = match_rule(rules, message)
    if '{0}' in response:
        phrase = replace_pronouns(phrase)
        response = response.format(phrase)
    return response
##### chatbot reply start


# Create a route for the home page:
@app.route('/')
def index():
    return render_template('index.html')

# Modify your Flask app to handle the socket events:
@socketio.on('message')
def handle_message(data):
    message = data['message']
    # Implement the logic to process the message, perform sentiment analysis, etc.

    # Emit a 'message' event back to the client
    emit('message', { 'message':  message })

# Run the Flask app
if __name__ == '__main__':
    socketio.run(app, port=8000,debug=True)

