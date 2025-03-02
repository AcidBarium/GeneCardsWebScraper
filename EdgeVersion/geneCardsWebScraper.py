from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import transModeFree
# import transModeGoogle
from bs4 import BeautifulSoup
import pandas as pd
import re
import csv
import time


def scrape_gene_summaries(gene):
    # 修改为Edge浏览器的配置
    webdriver_service = Service('./msedgedriver.exe')
    options = webdriver.EdgeOptions()
    options.add_argument('--headless')  # 无头模式
    options.add_argument('--disable-blink-features=AutomationControlled')
    # 添加常见浏览器特征
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0')
    driver = webdriver.Edge(service=webdriver_service, options=options)

    try:
        url = f"https://www.genecards.org/cgi-bin/carddisp.pl?gene={gene}"
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "summaries")))
        page_source = driver.page_source
    except Exception as e:
        print(f"Failed to load summaries for {gene}: {e}")
        driver.quit()
        return {}

    soup = BeautifulSoup(page_source, 'html.parser')
    driver.quit()

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
        uniprot_pattern = re.compile(
            f'UniProtKB/Swiss-Prot Summary for {gene} Gene')

        ncbi_summary = summaries_section.find('h3', string=ncbi_pattern)
        if ncbi_summary:
            ncbi_summary_text = ncbi_summary.find_next('p').text
            summaries['NCBI Gene Summary'] = ncbi_summary_text.strip()

        genecards_summary = summaries_section.find(
            'h3', string=genecards_pattern)
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

    with open('./gene_summaries.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Gene', 'Summary'])

    for index, gene in enumerate(gene_list, start=1):
        gene_data = scrape_gene_summaries(gene)
        if gene_data:
            with open('./gene_summaries.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([gene_data['gene'],
                                 "NCBI Gene Summary" + "   :   " + gene_data['NCBI Gene Summary'] + "   \n \n  " +
                                 "GeneCards Summary" + "   :   " + gene_data['GeneCards Summary'] + "   \n \n  " +
                                 "UniProtKB/Swiss-Prot Summary" + "   :   " + gene_data['UniProtKB/Swiss-Prot Summary']])
            print(
                f"Progress: {index}/{total_genes} genes processed. Gene '{gene}' summaries fetched.")
            time.sleep(2)  # 每次请求间隔2秒
        else:
            print(
                f"Progress: {index}/{total_genes} genes processed. No summaries found for gene '{gene}'.")

    print("处理完毕,文件保存到了gene_summaries.csv.")
    print("开始翻译")

    # api_key_ = ':fx'
    data = pd.read_csv("./gene_summaries.csv", encoding='utf-8')
    # 根据需要选择合适的翻译函数
    transModeFree.translate_text(data)  # 使用免费的国内翻译模式
    # transModeGoogle.translate_text(data)  # 使用Google翻译模式


if __name__ == "__main__":
    main()
