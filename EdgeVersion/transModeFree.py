import re
import translators as ts
import time


def chunk_text(text, max_chunk_size=1000):
    if len(text) <= max_chunk_size:
        return [text]

    chunks = []
    current_chunk = ""
    sentences = re.split(r'(?<=[.!?])\s+', text)

    for sentence in sentences:
        # 如果单个句子超过最大长度，按照单词分割
        if len(sentence) > max_chunk_size:
            words = sentence.split()
            temp_chunk = ""
            for word in words:
                if len(temp_chunk) + len(word) + 1 > max_chunk_size:
                    chunks.append(temp_chunk.strip())
                    temp_chunk = word
                else:
                    temp_chunk += " " + word if temp_chunk else word
            if temp_chunk:
                current_chunk += temp_chunk + " "
        # 正常处理不超长的句子
        elif len(current_chunk) + len(sentence) + 1 > max_chunk_size:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
        else:
            current_chunk += sentence + " "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def translate_text(data):

    rows, columns = data.shape
    data['翻译结果'] = ""

    for i in range(rows):
        gene_name = data.iloc[i, 0]
        print(f"正在翻译第 {i + 1}/{rows} 条数据，基因: {gene_name}")

        value = data.iloc[i, 1]
        value_str = str(value).strip()

        if not value_str or value_str.isspace():
            print("警告: 检测到空文本，跳过翻译")
            data.iloc[i, 2] = "空文本，无需翻译"
            continue

        # 文本分块
        text_chunks = chunk_text(value_str)
        print(f"文本已分割为 {len(text_chunks)} 个块进行翻译")

        translated_chunks = []
        chunk_success = True

        for chunk_idx, chunk in enumerate(text_chunks):
            try:
                print(
                    f"  - 正在翻译块 {chunk_idx + 1}/{len(text_chunks)}，长度: {len(chunk)} 字符")
                start_time = time.time()

                translated_chunk = ts.translate_text(
                    chunk, from_language='en', to_language='zh')

                elapsed_time = time.time() - start_time
                print(
                    f"  ✓ 块 {chunk_idx + 1} 翻译成功，用时: {elapsed_time:.2f}秒")

                translated_chunks.append(translated_chunk)

                # 每个块之间增加短暂延迟
                time.sleep(1.5)

            except Exception as e:
                import traceback
                error_details = traceback.format_exc()

                print(f"  ✗ 块 {chunk_idx + 1} 翻译失败: {e}")
                print(f"  详细错误信息: \n{error_details}")

                # 记录失败的块
                translated_chunks.append(f"[翻译失败: {str(e)}]")
                chunk_success = False

                # 如果遇到错误，增加等待时间
                print("  增加等待时间到5秒后继续...")
                time.sleep(5)

        # 合并所有翻译结果
        final_translation = " ".join(translated_chunks)
        data.iloc[i, 2] = final_translation

        # 单条数据处理完后稍作延迟
        time.sleep(2)

    # 最终保存
    data.to_csv("./gene_summaries_afterTrans.csv",
                index=False, encoding='utf-8')
    print(f"✓ 翻译完毕! 共处理 {rows} 条记录，翻译文件保存到了gene_summaries_afterTrans.csv.")

    return data
