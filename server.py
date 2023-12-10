from flask import Flask, request, jsonify,  render_template
from flask import Flask
from intelbot import predict_class, get_response, INTENTS
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('main.html')


@app.route('/get')
def get_message():
    student_id = '2'
    message = request.args.get('message')

    ints = predict_class(message)

    # Get response
    chatbot_response = get_response(ints, INTENTS, student_id)

    print(chatbot_response)

    return chatbot_response  # Return the chatbot response to the client


if __name__ == '__main__':
    app.run()
