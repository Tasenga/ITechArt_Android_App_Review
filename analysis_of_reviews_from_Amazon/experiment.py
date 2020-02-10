from itertools import groupby

a = [{"a": "vasya", "b": "cat"}, {"a": "petya", "b": "fox"}, {"a": "vasya", "b": "dog"}]
print(a)

result_1 = {key: list(item) for key, item in groupby(a, key=lambda x: x["a"])}
print(result_1)

result_2 = {
    key: list(item)
    for key, item in groupby(sorted(a, key=lambda x: x["a"]), key=lambda x: x["a"])
}
print(result_2)
