from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_path = '/root/autodl-tmp/DeepSeek-R1-Distill-Qwen-14B'

# 加载tokenizer和模型
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(
    model_path, 
    device_map="auto",
    torch_dtype=torch.bfloat16
)

# 设置pad token和eos token
tokenizer.pad_token = tokenizer.eos_token
model.config.pad_token_id = model.config.eos_token_id

# 初始化对话历史
messages = []

def chat(prompt):
    try:
        # 添加用户输入到对话历史
        messages.append({"role": "user", "content": prompt})
        
        # 使用对话模板格式化整个对话历史
        text = tokenizer.apply_chat_template(
            messages, 
            tokenize=False, 
            add_generation_prompt=True
        )
        
        # 生成回复
        model_inputs = tokenizer(
            [text], 
            return_tensors="pt",
            padding=True,
            truncation=True,
        ).to('cuda')
        
        # 直接生成完整回复
        outputs = model.generate(
            input_ids=model_inputs.input_ids,
            attention_mask=model_inputs.attention_mask,
            max_new_tokens=512,
            do_sample=True,
            top_p=0.9,
            temperature=0.7,
            repetition_penalty=1.2,
            pad_token_id=tokenizer.pad_token_id
        )
        
        # 解码生成的回复
        response = tokenizer.decode(outputs[0][len(model_inputs.input_ids[0]):], skip_special_tokens=True)
        
        print("\nAI:", response , "\n </lcx_out_mark>")
        
        # 将AI的回复添加到对话历史
        messages.append({"role": "assistant", "content": response})

        
        return response
        
    finally:
        # 清理显存
        del model_inputs
        torch.cuda.empty_cache()

# 交互式对话循环
# # print("开始对话，输入 'quit' 结束对话")
# while True:
#     user_input = input("\n用户: ")
#     if user_input.lower() == 'quit':
#         print("对话结束")
#         break


# 打开文件并读取整个内容
with open('/root/deepseek/inference/ciallo2.txt', 'r') as file:
    content = file.read()


response = chat(content)

with open('/root/deepseek/inference/ciallo3.txt', 'w', encoding="utf-8") as file2 :
    file2.write(response)



