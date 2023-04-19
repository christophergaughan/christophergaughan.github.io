lst = [{'name': 'Alice', 'age': 25},       {'name': 'Bob', 'age': 30},       {'name': 'Charlie', 'age': 35}]
filtered_lst = list(filter(lambda x: x['age'] > 28, lst))
print(filtered_lst)
