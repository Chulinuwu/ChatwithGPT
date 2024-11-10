from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ]
    )

    response_message = completion.choices[0].message.content
    return jsonify({"response": response_message})

if __name__ == '__main__':
    app.run(debug=True)