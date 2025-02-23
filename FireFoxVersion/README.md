# GeneCardsWebScraper Edge 浏览器版本

## 介绍

基于firefox浏览器的爬虫

## 环境要求

- `Python 3.x`
-  firefox浏览器
-  geckodriver.exe,火狐浏览器驱动

### 所需`Python`包

- selenium
- beautifulsoup4
- pandas
- deep-translator

安装依赖：

```bash
pip install selenium beautifulsoup4 pandas deep-translator
```

### 设置步骤

1. 下载与您的火狐浏览器版本匹配的 Microsoft Edge WebDriver
   - 从[GeckoDriver Releases](https://github.com/mozilla/geckodriver/releases)下载适合您电脑环境的驱动程序。
   - 将`geckodriver.exe`放在脚本同一目录下
2. 准备基因列表:
   - 创建名为`genelist.csv`的 CSV 文件
   - 在第一列添加基因符号
3. 配置 DeepL API(可自行替换源码)：
   - 获取您的 DeepL API 密钥
   - 将脚本中的 :fx 替换为您的实际 API 密钥

> [!NOTE]
> 同时，请确保使用的翻译工具支持国内环境

## 使用方法

运行脚本

```bash
python geneCardsWebScraper.py
```

## 输出文件

- `gene_summaries.csv`：包含原始英文摘要
- `gene_summaries_afterTrans.csv`：包含英文摘要和中文翻译

