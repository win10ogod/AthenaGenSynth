\[ 中文 | [English](README.md) \]
# AthenaGen
使用 OLLAMA 產生數據
並使用簡單的腳本建立預訓練數據集

# 如何使用
參考ollama serve的使用方法啟動api。

運行 python Synth.py

輸入您要使用的 ollama 模型。

輸入提示，輸入done結束手動輸入提示，或在txt檔案中每行放置一個提示。
# alltxttojson.py
修改data=""

例如:

txt存放在./cleaned3

data="./cleaned3"

運行 python alltxttojson.py

就會得到data{}.json文件
