# 自动从genecards爬出相关基因的相关信息，并且进行一个翻译

## 介绍

帮助中国医学生从genecards找到相关基因的相关信息，并进行一个简单的翻译操作


## 项目修改说明

这个项目是基于 [marswh12312313的爬虫项目](https://github.com/marswh12312313/GeneSumCrawler/tree/main) 修改而来的，原项目的版权属于 Maria (2023)，并使用 MIT 许可证。

我对原项目做了以下修改：
- 新增了中文翻译功能
- 修改了代码实现中表格设计的方式
- 更改了不同系统所需要的geckodriver文件

此项目同样遵循 MIT 许可证，详细信息请参考 `LICENSE` 文件。



## 项目文件说明

- geneCardsWebScraper是主程序，包含了爬虫和翻译，直接运行即可。
- geckodriver.exe来自于[GeckoDriver Releases](https://github.com/mozilla/geckodriver/releases),原仓库中为linux下的文件，考虑到中国大多数医学生使用的是windows操作系统，这里进行了一个更替。如果你使用的是mac或者linux，你仍然可以在[GeckoDriver Releases](https://github.com/mozilla/geckodriver/releases)选择适合你的版本。
- trans和trans_deepl是单独摘出来的翻译代码
- genelist.csv中放你需要查询的基因的名字
- gene_summaries.csv爬取到的信息
- gene_summaries_afterTrans.csv为翻译后的信息

## 安装依赖项
```
pip install selenium deep-translator beautifulsoup4 pandas
```

## 项目驱动
- 里面包含了一个windows的项目驱动文件，详情见上文项目文件说明的geckodriver.exe。

- 确保 GeckoDriver 已正确安装并位于系统的 PATH 中，或使用 GeckoDriver 可执行文件的正确路径更新脚本

- 你可能还需要一个最新版的火狐浏览器(感谢[kpmark](https://github.com/markzhang12345)，他写了一个edge浏览器的版本)


## 运行脚本

```python
python geneCardsWebScraper.py
```

## 运行效果
![alt text](img/image.png)


## 鸣谢

[marswh12312313](https://github.com/marswh12312313)，[kpmark](https://github.com/markzhang12345)


## 联系方式

acidbarium@163.om