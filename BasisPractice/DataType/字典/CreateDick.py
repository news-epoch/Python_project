# 创建空字典
dict1 = dict()
dict1 = {}
# 创建数据字典
dict1 = {'a': 1, 'b': 2}
dict1 = dict({'a': 1, 'b': 3})
print(dict1)

# 创建多重字典
## 二重数组
dict2 = {'a': 'null', 'b': 'null', 'c': 'null'}
dict2['a'] = {1: 'one',2: 'two',3: 'three'}
print(dict2['a'][1])