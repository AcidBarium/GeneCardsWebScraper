from deep_translator import GoogleTranslator


def translate_text(data):

    rows, columns = data.shape
    data['翻译结果'] = ""

    for i in range(rows):
        print(f"正在{i + 1}/{rows}")
        value = data.iloc[i, 1]
        value_str = str(value).strip()
        try:
            txt_after_translate = GoogleTranslator(
                source='en', target='zh-CN').translate(value_str)
            data.iloc[i, 2] = txt_after_translate
        except Exception as e:
            print(f"翻译失败: {e}")
            data.iloc[i, 2] = "翻译失败"

    data.to_csv("./gene_summaries_afterTrans.csv",
                index=False, encoding='utf-8')
    print("翻译完毕,翻译文件保存到了gene_summaries_afterTrans.csv.")
