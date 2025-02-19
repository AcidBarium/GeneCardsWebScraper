import pandas as pd
from deep_translator import GoogleTranslator
# from deep_translator import DeeplTranslator

# api_key_ = '77893326-5985-42b5-9119-f3ab0d456f13:fx'          #这里放deepl的api


data = pd.read_csv("./gene_summaries.csv", encoding='utf-8')   # 这个地方放文件路径
rows, columns = data.shape

data['翻译结果'] = ""  

for i in range(rows):
    print(f"正在{i}/{rows}")
    value = data.iloc[i, 1]  
    value_str = str(value).strip()  
    try:
        # txt_after_translate = DeeplTranslator(api_key = api_key_,source='en', target='zh').translate(value_str)
        txt_after_translate = GoogleTranslator(api_key = api_key_,source='en', target='zh-CN').translate(value_str)
        data.iloc[i, 2] = txt_after_translate  
    except Exception as e:
        print(f"翻译失败: {e}")  
        data.iloc[i, 2] = "翻译失败"  

data.to_csv("./gene_summaries_afterTrans.csv", index=False, encoding='gbk')

