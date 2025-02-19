from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from deep_translator import GoogleTranslator
# from deep_translator import DeeplTranslator
from bs4 import BeautifulSoup
import pandas as pd
import re
import csv


    

# 爬虫的主要功能
def scrape_gene_summaries(gene):
    # 在函数内部创建新的WebDriver服务
    webdriver_service = Service('./geckodriver.exe')  # 替换为你的GeckoDriver路径
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')  # 无头模式
    driver = webdriver.Firefox(service=webdriver_service, options=options)

    try:
        url = f"https://www.genecards.org/cgi-bin/carddisp.pl?gene={gene}"
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "summaries")))
        page_source = driver.page_source
    except Exception as e:
        print(f"Failed to load summaries for {gene}: {e}")
        driver.quit()
        return {}

    soup = BeautifulSoup(page_source, 'html.parser')
    driver.quit()  # 关闭浏览器实例

    summaries = {
        'gene': gene,
        'NCBI Gene Summary': '',
        'GeneCards Summary': '',
        'UniProtKB/Swiss-Prot Summary': ''
    }

    summaries_section = soup.find('section', id='summaries')
    if summaries_section:
        ncbi_pattern = re.compile(f'NCBI Gene Summary for {gene} Gene')
        genecards_pattern = re.compile(f'GeneCards Summary for {gene} Gene')
        uniprot_pattern = re.compile(f'UniProtKB/Swiss-Prot Summary for {gene} Gene')

        ncbi_summary = summaries_section.find('h3', string=ncbi_pattern)
        if ncbi_summary:
            ncbi_summary_text = ncbi_summary.find_next('p').text
            summaries['NCBI Gene Summary'] = ncbi_summary_text.strip()

        genecards_summary = summaries_section.find('h3', string=genecards_pattern)
        if genecards_summary:
            genecards_summary_text = genecards_summary.find_next('p').text
            summaries['GeneCards Summary'] = genecards_summary_text.strip()

        uniprot_summary = summaries_section.find('h3', string=uniprot_pattern)
        if uniprot_summary:
            uniprot_summary_text = uniprot_summary.find_next('p').text
            summaries['UniProtKB/Swiss-Prot Summary'] = uniprot_summary_text.strip()

    return summaries


def main():
    gene_list = pd.read_csv('./genelist.csv').iloc[:, 0].tolist()
    total_genes = len(gene_list)

    # 打开 CSV 文件并写入标题行
    with open('./gene_summaries.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Gene', 'Summary'])

    for index, gene in enumerate(gene_list, start=1):
        gene_data = scrape_gene_summaries(gene)
        if gene_data:
            # 将数据写入到 CSV 文件的一行中
            with open('./gene_summaries.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([gene_data['gene'], 
                                 "NCBI Gene Summary"  + "   :   "  +   gene_data['NCBI Gene Summary'] + "   \n \n  " +
                                  "GeneCards Summary" + "   :   "  + gene_data['GeneCards Summary']   + "   \n \n  " +
                                  "UniProtKB/Swiss-Prot Summary" + "   :   " +  gene_data['UniProtKB/Swiss-Prot Summary']])
            print(f"Progress: {index}/{total_genes} genes processed. Gene '{gene}' summaries fetched.")
        else:
            print(f"Progress: {index}/{total_genes} genes processed. No summaries found for gene '{gene}'.")
    
    
    
    print("处理完毕,文件保存到了gene_summaries.csv.")
    print("开始翻译")
    

    # api_key_ = '77893326-5985-42b5-9119-f3ab0d456f13:fx'  #如果用deepl翻译的话需要这个api

    data = pd.read_csv("./gene_summaries.csv", encoding='utf-8')   # 这个地方放文件路径
    rows, columns = data.shape

    data['翻译结果'] = ""  

    for i in range(rows):
        print(f"正在{i + 1}/{rows}")
        value = data.iloc[i, 1]  
        value_str = str(value).strip()  
        try:
            # txt_after_translate = DeeplTranslator(api_key = api_key_,source='en', target='zh').translate(value_str)
            txt_after_translate = GoogleTranslator(source='en', target='zh-CN').translate(value_str)
            data.iloc[i, 2] = txt_after_translate  
        except Exception as e:
            print(f"翻译失败: {e}")  
            data.iloc[i, 2] = "翻译失败"  

    data.to_csv("./gene_summaries_afterTrans.csv", index=False, encoding='gbk')


    print("翻译完毕,翻译文件保存到了gene_summaries_afterTrans.csv.")
    


if __name__ == "__main__":
    main()
