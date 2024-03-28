import json
import os

# 獲取當前檔案所在目錄的絕對路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
# 設定父目錄的路徑
parent_dir = os.path.dirname(current_dir)

# 讀取 JSON 檔案
json_file_path = os.path.join(parent_dir, 'BlockInfoDump.json')
with open(json_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 確認每個元素的第一級 key 以及它們的重複次數
key_counts = {}
for item in data['data_blocks']:
    for key in item.keys():
        if key in key_counts:
            key_counts[key] += 1
        else:
            key_counts[key] = 1

# 輸出結果
for key, count in key_counts.items():
    print(f'Key: {key}, 重複次數: {count}')

print('--------')
print('--------')
print('--------')

# 首先建立包含 0: '公用屬性' 的字典，用於記錄每個 key 在所有元素中是否出現過
all_keys = set()
for item in data['data_blocks']:
    for key in item.keys():
        all_keys.add(key)

# 創建一個空的字典來儲存資料
data_category = {}

# 創建一個集合來記錄不重複的 category_int 和 category 組合
category_combinations = set()

# 遍歷 data_blocks 中的每個元素，將 category_int 和 category 組合加入集合
for item in data['data_blocks']:
    category_int = item.get('category_int')
    category = item.get('category')
    if category_int is not None and category is not None:
        category_combinations.add((category_int, category))

# 將集合轉換為列表並按 category_int 排序
sorted_category_combinations = sorted(list(category_combinations), key=lambda x: x[0])

# 初始化 data_category 字典中的每個類別對應的字典，並為每個元素的 data 新增所有的鍵並將值設置為 0
for combination in sorted_category_combinations:
    category_int = combination[0]
    category = combination[1]
    key = f"{category_int}_{category}"  # 使用 category_int 和 category 組合成鍵
    count = sum(1 for item in data['data_blocks'] if item.get('category_int') == category_int)
    data_category[key] = {'category_int': category_int, 'category': category, 'count': count, 'data': {}}
    # 將所有的鍵新增到 data 字典中並將值設置為 0
    for item_key in all_keys:
        data_category[key]['data'][item_key] = 0

# 將 data_category 轉換為 JSON 字串
data_category_json = json.dumps(data_category, ensure_ascii=False, indent=4)

# 將 JSON 字串寫入檔案
data_category_json_path = os.path.join(current_dir, 'data_category.json')
with open(data_category_json_path, 'w', encoding='utf-8') as f:
    f.write(data_category_json)

# 讀取 data_category_json
with open(data_category_json_path, 'r', encoding='utf-8') as f:
    data_category_json = json.load(f)

# 檢查 data_blocks 下的每個元素
for item in data['data_blocks']:
    # 獲取元素的 category_int
    category_int = item.get('category_int')
    if category_int is not None:
        # 根據 category_int 找到對應的 data_category_json 的鍵
        category_key = str(category_int) + '_' + item.get('category')
        if category_key in data_category_json:
            # 更新對應類別的數據
            for key in item.keys():
                # 只更新第一級的鍵，不更新其子鍵
                if key != 'data':
                    data_category_json[category_key]['data'][key] += 1

# 將更新後的 data_category_json 寫回檔案
with open(data_category_json_path, 'w', encoding='utf-8') as f:
    json.dump(data_category_json, f, ensure_ascii=False, indent=4)

print(data_category_json)