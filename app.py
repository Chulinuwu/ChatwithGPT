from transformers import GPTNeoXForCausalLM, GPTNeoXTokenizerFast
from flask import Flask, jsonify, request
from flask_cors import CORS
import torch
import time

app = Flask(__name__)
CORS(app)

model_id = "EleutherAI/gpt-neox-20b"
print("Loading model and tokenizer...")

try:
    print("Loading model...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    model = GPTNeoXForCausalLM.from_pretrained(model_id, device_map="auto", low_cpu_mem_usage=True)
    print("Model loaded successfully.")
    
    print("Loading tokenizer...")
    tokenizer = GPTNeoXTokenizerFast.from_pretrained(model_id)
    print("Tokenizer loaded successfully.")
except Exception as e:
    print(f"Error loading model and tokenizer: {e}")

@app.route('/chat', methods=['POST'])
def generate():
    print("Received POST request at /chat")
    input_text = request.json.get('message')
    if not input_text:
        print("No input text provided")
        return jsonify({"error": "No input text provided"}), 400

    print(f"Input text: {input_text}")
    start_time = time.time()
    inputs = tokenizer(input_text, return_tensors='pt')
    print("Got input")
    input_ids = inputs['input_ids'].to(device)
    print("Got input2")
    attention_mask = inputs['attention_mask'].to(device)
    print("Got attention mask, now generating")
    
    outputs = model.generate(input_ids, attention_mask=attention_mask, pad_token_id=tokenizer.eos_token_id, max_new_tokens=20)
    print("Generated successfully")
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print("Decoded successfully")
    
    end_time = time.time()
    print(f"Generated text: {generated_text}")
    print(f"Time taken: {end_time - start_time} seconds")
    return jsonify({"response": generated_text})

@app.route('/')
def home():
    return jsonify({"message": "Flask server is running!"})

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(host='0.0.0.0', port=5000)