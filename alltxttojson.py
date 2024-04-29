import os
import random
import multiprocessing
from tqdm import tqdm
import json

data = "./cleaned3/"

def process_files(file_list):
    all_text = []
    for filename in file_list:
        with open(data + filename, encoding='utf-8') as f:
            lines = f.read()
            lines = lines.split('\n')  # 以换行符号分割文本
            text = '\n'.join(f"{i + 1}:{line}" for i, line in enumerate(lines) if line.strip())  # 新增行号
        all_text.append({"text": text})
    return all_text

if __name__ == '__main__':
    lst = os.listdir(data)
    random.shuffle(lst)
    num = len(lst)
    cnt = 1
    batch_size = 10  # 定义每个 JSON 文件包含的文本文件数量

    # 使用多进程处理文件
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())  # 使用 CPU 核心数量的进程

    # 使用 tqdm 显示进度条
    with tqdm(total=num, desc="Processing Files") as pbar:
        while cnt < num:
            batch_files = lst[cnt:cnt + batch_size]  # 取得下一个批次的文件列表
            batch_text = pool.map(process_files, [batch_files])[0]
            cnt += batch_size
            pbar.update(batch_size)  # 更新进度条

            # 将批次的文字转换为 JSON 数组
            output_json = [{"text": entry["text"]} for entry in batch_text]

            # 将 JSON 写入文件
            json_filename = f'data{cnt // batch_size:02d}.json'  # 根据 cnt 计算输出文件的名称
            with open(json_filename, 'w', encoding='utf-8') as json_file:
                json.dump(output_json, json_file, ensure_ascii=False, indent=4)  # 写入整个列表

    pool.close()
    pool.join()

    print("JSON files have been created.")
