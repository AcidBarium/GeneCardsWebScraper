import requests

def query_model(prompt):
    url = "http://192.168.31.70:1234/v1/chat/completions"  
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

def translate_Deepseek_Locate(source):
    
    resq_ = "请将下面医学相关的英语翻译成中文，要求术语准确，数据无误，深入理解原文的语境和医学逻辑，避免因误解导致的翻译错误，语言流畅，逻辑清晰，风格一致。不要使用markdown格式，直接以文本的形式回答 。 \n"
    
    resq_ = resq_ + source
    
    result = query_model(resq_)
    
    # print(result['choices'][0]['message']['content'])
    
    ans = result['choices'][0]['message']['content']
    
    
    parts = ans.split('</think>', 1)
    if len(parts) > 1:
        result_ans = parts[1]
    else:
        result_ans = ans
    
    
    return result_ans



