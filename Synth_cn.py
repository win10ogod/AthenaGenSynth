import requests
import base64
import json
import os
import datetime
import glob

def generate_data(model, prompts, options=None, images=None, system=None, template=None, context=None, stream=False, raw=False, done=False, keep_alive="30m", output_json=False):
    url = "http://localhost:11434/api/generate"
    
    generated_texts = []
    json_data = []
    

    for prompt in prompts:
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
            "top_p": 0.9,
            "temperature":0.7,
            "max_ctx":32768,
            "done":done,
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
        
        print(f"API 響應狀態碼: {response.status_code}")
        print(f"API 響應內容: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict) and "response" in data:
                generated_text = data["response"]
                generated_texts.append(generated_text)
                if output_json:
                    json_data.append({"instruction": prompt, "Response": generated_text})
            else:
                print("API 響應格式不正確")
        else:
            print(f"請求失敗,狀態碼: {response.status_code}")
    
    if output_json:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        json_file_name = f"generated_texts_{timestamp}.json"
        with open(json_file_name, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)
        print(f"生成的 JSON 文件已保存到 {json_file_name}")
    
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
        print(f"生成的文本已保存到 {file_path}")
    except IOError as e:
        print(f"保存文件時出錯: {e}")

def create_output_file():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"generated_texts_{timestamp}.txt"
    return file_name
    

def main():
    model = input("請輸入模型名稱: ")
    prompt_type = input("請選擇提示類型 (1-輸入提示, 2-從文件載入提示:)")
    output_json = input("是否輸出 JSON 文件 (yes/no): ")
    output_json = output_json.lower() == 'yes'
    
    if prompt_type == "1":
        prompts = []
        while True:
            prompt = input("請輸入提示 (輸入 'done' 完成): ")
            if prompt.lower() == 'done':
                break
            prompts.append(prompt)
    elif prompt_type == "2":
        file_path = input("請輸入文件路徑: ")
        prompts = load_prompts_from_file(file_path)
  
    else:
        print("無效的選擇")
        return
    
    generated_texts = generate_data(model, prompts, output_json=output_json)
    
    if generated_texts:
        output_file = create_output_file()
        save_to_file(output_file, generated_texts)
    else:
        print("未生成任何文本")

if __name__ == "__main__":
    main()
