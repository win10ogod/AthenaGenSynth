import requests
import base64
import json
import os
import datetime

def generate_data(model, prompts, images=None, options=None, system=None, template=None, context=None, stream=False, raw=False, keep_alive="5m"):
    url = "http://localhost:11434/api/generate"
    
    generated_texts = []
    
    for prompt in prompts:
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
            "options": {
            "num_predict": 100,
            "top_k": 20,
            "top_p": 0.9,
            "temperature":0.7,
            "stop": ["\n", "user:"],
            "num_ctx": 4096,
            },
            "raw": raw,
            "keep_alive": keep_alive
        }
        
        if images:
            encoded_images = [base64.b64encode(image).decode('utf-8') for image in images]
            payload["images"] = encoded_images
        
        if options:
            payload["options"] = options
        
        if system:
            payload["system"] = system
        
        if template:
            payload["template"] = template
        
        if context:
            payload["context"] = context
        
        response = requests.post(url, json=payload)
        
        print(f"API response status code: {response.status_code}")
        print(f"API response content: {response.text}")        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict) and "response" in data:
                generated_text = data["response"]
                generated_texts.append(generated_text)
            else:
                print("API response format is not correct")
        else:
            print(f"Request failed, status code: {response.status_code}")
    
    return generated_texts

def load_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def load_prompts_from_file(file_path):
    with open(file_path, 'r') as file:
        prompts = file.readlines()
        prompts = [prompt.strip() for prompt in prompts if prompt.strip()]
        return prompts

def save_to_file(file_path, texts):
    try:
        with open(file_path, 'w') as file:
            for text in texts:
                file.write(f"{text}\n")
        print(f"Generated text saved to {file_path}")
    except IOError as e:
        print(f"Error saving file: {e}")

def create_output_file():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"generated_texts_{timestamp}.txt"
    return file_name

def main():
    model = input("Please enter the model name: ")
    prompt_type = input("Please select prompt type (1-Input prompt, 2-Load prompt from file): ")
    
    if prompt_type == "1":
        prompts = []
        while True:
            prompt = input("Please enter a prompt (enter 'done' to end): ")
            if prompt.lower() == 'done':
                break
            prompts.append(prompt)
    elif prompt_type == "2":
        file_path = input("Please input file path: ")
        prompts = load_prompts_from_file(file_path)
    else:
        print("Invalid selection")
        return
    
    generated_texts = generate_data(model, prompts)
    
    if generated_texts:
        output_file = create_output_file()
        save_to_file(output_file, generated_texts)
    else:
        print("No text was generated")

if __name__ == "__main__":
    main()
