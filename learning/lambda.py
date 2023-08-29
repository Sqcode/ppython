
items = [{"a":1,"b":2},{"a":2,"b":3},{"a":3,"b":4},{"a":4,"b":5}]
print(a := [item["a"] for item in items])
print(set(map(lambda item: item["a"], items)))

print(list(map(lambda item:item["a"], items)))

# # 定义一个 lambda 函数，用于计算两个数的和
# add = lambda x, y: x + y
# print(add(2, 3))  # 输出 5

# # 使用 lambda 函数对列表中的每个元素进行平方
# numbers = [1, 2, 3, 4, 5]
# squared = list(map(lambda x: x**2, numbers))
# print(squared)  # 输出 [1, 4, 9, 16, 25]

# # 使用 lambda 函数筛选列表中的偶数
# even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
# print(even_numbers)  # 输出 [2, 4]

# # 使用 lambda 函数对列表中的元组按第二个元素排序
# pairs = [(1, 'one'), (4, 'four'), (3, 'three'), (2, 'two')]
# sorted_pairs = sorted(pairs, key=lambda x: x[1])
# print(sorted_pairs)  # 输出 [(4, 'four'), (1, 'one'), (3, 'three'), (2, 'two')]
