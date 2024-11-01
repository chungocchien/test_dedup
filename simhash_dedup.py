from simhash import Simhash
from collections import defaultdict
import re
import pandas as pd


def get_simhash(text):
    # Hàm tính SimHash cho văn bản
    return Simhash(str(text), f=128).value


def hamming_distance(hash1, hash2):
    # Hàm tính khoảng cách Hamming giữa hai SimHash
    x = hash1 ^ hash2
    dist = bin(x).count('1')
    return dist


def lsh_grouping(texts, threshold, num_bands):
    simhashes = [(i, get_simhash(text)) for i, text in enumerate(texts)]
    buckets = defaultdict(list)

    # Chia SimHash thành các bands
    for idx, simhash in simhashes:
        # Chuyển SimHash thành chuỗi nhị phân 128 bit
        hash_str = f'{simhash:128b}'
        band_size = len(hash_str) // num_bands
        for band in range(num_bands):
            band_hash = hash_str[band * band_size:(band + 1) * band_size]
            buckets[(band, band_hash)].append(idx)

    # Sử dụng DFS để gom các nhóm dữ liệu có Hamming distance <= threshold
    visited = set()
    unique_groups = []

    def dfs(index, group):
        visited.add(index)
        group.append(index)
        for neighbor in neighbors[index]:
            if neighbor not in visited:
                dfs(neighbor, group)

    # Xây dựng danh sách các hàng xóm dựa trên khoảng cách Hamming
    neighbors = defaultdict(list)
    for bucket, indices in buckets.items():
        for i in range(len(indices)):
            for j in range(i + 1, len(indices)):
                idx1, idx2 = indices[i], indices[j]
                hash1, hash2 = simhashes[idx1][1], simhashes[idx2][1]
                if hamming_distance(hash1, hash2) <= threshold:
                    neighbors[idx1].append(idx2)
                    neighbors[idx2].append(idx1)

    # Gom các nhóm dựa trên DFS và chỉ giữ lại 1 đại diện cho mỗi nhóm
    for idx in range(len(texts)):
        if idx not in visited:
            group = []
            dfs(idx, group)
            # Giữ lại chỉ một đại diện trong mỗi nhóm
            unique_groups.append(group[0])
    # Trả về các văn bản không bị trùng lặp
    return [texts[i] for i in unique_groups]


def remove_codes(text):
    '''
    Hàm loại bỏ mã code phục vụ cho việc
    loại bỏ các data có nội dung giống nhau, cấu trúc giống nhau
    '''
    pattern = r'\b\w{5,}\b'
    cleaned_text = re.sub(pattern, '', text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    return cleaned_text


def remove_duplicates(array):
    seen = set()
    unique_array = []
    for i in range(len(array)):
        if array[i] not in seen:
            unique_array.append(i)
            seen.add(array[i])
    return unique_array


texts = pd.read_csv('data_duplicate.csv')['text']
new_texts = []
for text in texts:
    new_texts.append(remove_codes(str(text)))
indice_array = remove_duplicates(new_texts)
unique_texts = [texts[i] for i in indice_array]

output_texts = lsh_grouping(texts=unique_texts, threshold=20, num_bands=16)
output = pd.DataFrame({'text': output_texts})
output.to_csv('new_data_simhash.csv')
