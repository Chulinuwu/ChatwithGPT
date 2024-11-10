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
    total_tokens = completion.usage.total_tokens
    input_tokens = completion.usage.prompt_tokens
    output_tokens = completion.usage.prompt_tokens

    cost_per_input_token = 0.0000025  # $2.50 per 1M input tokens
    cost_per_output_token = 0.00001   # $10.00 per 1M output tokens

    total_cost = (input_tokens * cost_per_input_token) + (output_tokens * cost_per_output_token)

    response_with_cost = f"{response_message} ({total_cost:.5f} dollar)"
    return jsonify({"response": response_with_cost})

if __name__ == '__main__':
    app.run(debug=True)