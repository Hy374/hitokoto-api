# 第 1 题：写一个函数 count_vowels(text)，统计一个字符串里元音字母（a、e、i、o、u）的个数，返回数字。
# 例：count_vowels("hello world") 应该返回 3。

def count_vowels(text):
    num = 0
    for char in text:
        if char.lower() in 'aeiou':
            num += 1
    return num

print(count_vowels("Hello world"))




# 第 2 题：写一个函数 even_squares(numbers)，接收一个整数列表，返回其中偶数的平方组成的新列表。
# 例：even_squares([1, 2, 3, 4, 5]) 应该返回 [4, 16]。

def even_squares(numbers):
    new_list = []
    for num in numbers:
        if num % 2 == 0:
            new_list.append(num * num)
    return new_list

print(even_squares([1, 2, 3, 4, 5]))