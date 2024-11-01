import re
from datasketch import MinHash, MinHashLSH


def make_features(input_str):
    """break the long input string into features, with length = 3
    """
    length = 3
    input_str = input_str.lower()
    out_str = re.sub(r'[^\w]+', '', input_str)
    return [out_str[i:i + length]
            for i in range(max(len(out_str) - length + 1, 1))]


def get_minhash(text, num_perm=128):
    # Tách các từ trong văn bản bằng cách dùng CountVectorizer
    tokens_list = make_features(str(text))

    minhash = MinHash(num_perm=num_perm)

    # Tạo MinHash object
    for token in tokens_list:
        minhash.update(token.encode('utf8'))

    return minhash


def minhash_dedup(texts, threshold, num_perm):
    # Khởi tạo LSH với số lượng permutators (num_perm) cho MinHash
    lsh = MinHashLSH(threshold, num_perm)

    # Thêm các văn bản vào LSH
    minhashes = []
    for i in range(len(texts)):
        minhash = get_minhash(texts[i])
        lsh.insert(f"doc_{i}", minhash)  # Gắn tên mỗi văn bản là doc_{i}
        minhashes.append(minhash)

    deduplicated_texts = []
    seen_docs = set()

    for i in range(len(texts)):
        if f"doc_{i}" not in seen_docs:
            # Tìm các văn bản t-pound trường lặp
            similar_docs = lsh.query(minhashes[i])
            # Đánh dêu tất cả các văn bản t-pound trường lặp
            seen_docs.update(similar_docs)
            # Chỉ giữ lại văn bản đầu tiên của nhóm trùng lặp
            deduplicated_texts.append(texts[i])
    return set(deduplicated_texts)


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
