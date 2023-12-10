import json
import pickle
import random
import numpy as np
import psycopg2  # Import psycopg2 for PostgreSQL connection
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model

# Your existing code...
lemmatizer = WordNetLemmatizer()

intents_file_path = r"C:\Users\Admin\Documents\GitHub\CSCobot\intelbot - Copy\intents.json"
INTENTS = json.loads(open(intents_file_path).read())

words_file_path = r"C:\Users\Admin\Documents\GitHub\CSCobot\intelbot - Copy\words.pkl"
words = pickle.load(open(words_file_path, 'rb'))

classes_file_path = r"C:\Users\Admin\Documents\GitHub\CSCobot\intelbot - Copy\classes.pkl"
classes = pickle.load(open(classes_file_path, 'rb'))

model_file_path = r"C:\Users\Admin\Documents\GitHub\CSCobot\intelbot - Copy\chatbotmodel.keras"
model = load_model(model_file_path)


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words


def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)


def predict_class(sentence):
    bow = bag_of_words(sentence)
    # res = model.predict(np.array([bow]))[0]
    res = model.predict(np.array([bow]), verbose=0)[0]

    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list


# Connect to PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="cisc",
    user="postgres",
    password="Password123"
)


def get_response(intents_list, intents_json, student_id):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']

    # Check if it's a personal query based on the intent tag or keywords
    personal_queries = ["student_name",
                        "year_level", "course", "track", "fine_id"]

    if tag in personal_queries:

        if tag == "fine_id":
            cursor = conn.cursor()
            cursor.execute(
                f"SELECT amount, reason FROM fines WHERE student_id='{student_id}'")
            student_data = cursor.fetchall()
            cursor.close()

            fine_list = []

            for fines in student_data:
                fine = f"{fines[0]} - {fines[1]}"
                fine_list.append(fine)

            response = '\n'.join(fine_list)

        else:
            # Fetch user-specific data from the database
            cursor = conn.cursor()
            cursor.execute(
                f"SELECT {tag} FROM students WHERE student_id='{student_id}'")
            student_data = cursor.fetchone()
            cursor.close()

            # Process the personal query and generate a response
            if student_data:
                # response = student_data[0] if student_data[0] else "I couldn't retrieve that information."
                if tag == "student_name":
                    response = f"Your name is {student_data[0]}."

                elif tag == "year_level":
                    if student_data[0] == 1:
                        response = "You are a first year student."
                    elif student_data[0] == 2:
                        response = "You are a second year student."
                    elif student_data[0] == 3:
                        response = "You are a third year student."
                    elif student_data[0] == 4:
                        response = "You are a fourth year student."

                elif tag == "course":
                    response = f"You are a {student_data[0]} student."

                elif tag == "track":
                    response = f"Your in the {student_data[0]} track."
            else:
                response = "I couldn't retrieve your information."
    else:
        # Process non-personal queries
        for intent in list_of_intents:
            if intent['tag'] == tag:
                result = random.choice(intent['responses'])
                response = result
                break
        else:
            response = "I'm sorry, I couldn't understand your query."

    return response


print('CSCobot is running!')

if __name__ == '__main__':

    while True:
        # Here, user_id should be obtained after the user logs in
        student_id = '2'

        message = input("You: ")
        # Predict intent
        ints = predict_class(message)
        # Get response
        res = get_response(ints, INTENTS, student_id)
        print("CSCobot:", res)
