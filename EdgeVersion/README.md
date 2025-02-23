# GeneCardsWebScraper Edge 浏览器版本

## 介绍

考虑到大部分同学使用的浏览器为微软的`Microsoft Edge`，这里提供一个基于此浏览器的爬虫版本

## 环境要求

- `Python 3.x`
- Microsoft Edge 浏览器
- Microsoft Edge WebDriver (msedgedriver.exe)

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

1. 下载与您的 Edge 浏览器版本匹配的 Microsoft Edge WebDriver
   - 从[微软官方网站](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/?form=MA13LH)下载
   - 将`msedgedriver.exe`放在脚本同一目录下
2. 准备基因列表:
   - 创建名为`genelist.csv`的 CSV 文件
   - 在第一列添加基因符号
3. 配置 DeepL API(可自行替换源码)：
   - 获取您的 DeepL API 密钥
   - 将脚本中的 :fx 替换为您的实际 API 密钥

> [!NOTE]
> 此版本需要的网络环境较不稳定，edge 爬虫结果仅在国内网络环境下具有可靠的爬取效果，在代理环境下爬取结果**较不稳定**
>
> 默认使用的谷歌翻译需要代理环境

## 使用方法

运行脚本

```bash
python geneCardsWebScraper.py
```

## 输出文件

- `gene_summaries.csv`：包含原始英文摘要
- `gene_summaries_afterTrans.csv`：包含英文摘要和中文翻译

## 注意事项

- 脚本包含 2 秒的请求延迟，以避免对 GeneCards 服务器造成过大压力
- 确保网络连接稳定
- 脚本使用无头浏览器模式以提高性能
- 处理大量基因可能需要较长时间
