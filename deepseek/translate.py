import requests

def query_model(prompt):
    url = "http://172.20.10.4:1234/v1/chat/completions"  
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-r1-distill-qwen-7b",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.0,
        "top_p": 0.95
    }
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()

# 使用示例
result = query_model("请把下面的英语翻译成中文，不要给思考过程，同时注意这里的英语是非常专业的医学英语，不需要给我思考过程，直接告诉我翻译结果 Diseases associated with VWA1 include Neuronopathy, Distal Hereditary Motor, Autosomal Recessive 7 and Neuronopathy, Distal Hereditary Motor, ")
print(result['choices'][0]['message']['content'])
