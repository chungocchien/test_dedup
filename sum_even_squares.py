# Tính tổng bình phương các số chẵn từ 0 đến n
def sum_even_squares(n):
    result = 0
    for i in range(n + 1):
        if i % 2 == 0:
            result = result + i * i
    return result

print(sum_even_squares(10000))
