def count_words(text):
    word_counts = {}
    words = text.split()
    for word in words:
        word = word.lower()
        if word in word_counts:
            word_counts[word] = word_counts[word] + 1
        else:
            word_counts[word] = 1
    return word_counts

text = "This is a test. This test is only a test."
print(count_words(text))
