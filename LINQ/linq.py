# coding: utf-8

from collections import Iterable
from itertools import islice, groupby
import re


class LinqContainer:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return str(self.data)

    def Select(self, selector):
        self.data = map(selector, self.data)
        # self.data = filter(selector, self.data)
        return self

    def Flatten(self):
        def flatten_sequence(sequence):
            for item in sequence:
                if isinstance(item, Iterable) and not isinstance(item, str):
                    yield from flatten_sequence(item)
                else:
                    yield item

        self.data = list(flatten_sequence(self.data))
        return self

    def Where(self, predicate):
        self.data = filter(predicate, self.data)
        return self

    def Take(self, count):
        self.data = islice(self.data, count)
        return self

    def GroupBy(self, key_selector=None):
        # result = []
        # for key, group in groupby(sorted(self.data, key=key_selector), key_selector):
        #     result.append((key, list(group)))
        # self.data = result
        self.data = [(key, list(group)) for key, group in groupby(sorted(self.data, key=key_selector), key_selector)]
        return self

    def OrderBy(self, key_selector=None):
        self.data = sorted(self.data, key=key_selector)
        return self

    def ToList(self):
        self.data = list(self.data)
        return self


# def flatten_sequence(sequence):
#     for item in sequence:
#         if isinstance(item, Iterable) and not isinstance(item, str):
#             yield from flatten_sequence(item)
#         else:
#             yield item


# class List(LinqContainer):
#     def __repr__(self):
#         return str(list(self.data))

def fibonacci_sequence():
    f_0, f_1 = 0, 1
    while True:
        yield f_0
        f_0, f_1 = f_1, f_0 + f_1


def tokenize_into_words(text):
    regexp = u"[^а-яА-Яё]"
    text = re.sub(regexp, u" ", text)
    return text.lower().split()


def main():
    print('test')
    lis = LinqContainer([[1, 3],[2, [[4]]], [[]]])
    # lis.Select(lambda x: x.upper()).ToList()
    lis.Flatten().ToList()
    print(lis)

    lis = LinqContainer(range(10))
    lis.GroupBy(lambda x: x % 2).ToList()
    print(lis)

    lis = LinqContainer(['apple', 'orange', 'banana', 'pear', 'raspberry', 'peach', 'plum'])
    lis.OrderBy(lambda x: len(x)).ToList()
    print(lis)

    lis = LinqContainer(range(10))
    lis.Where(lambda x : x % 2 == 0).Select(lambda x : x ** 2).Take(2).ToList()
    print(lis)

    drunk_f = LinqContainer(fibonacci_sequence())
    drunk_f.Where(lambda x: x % 3 == 0).Select(lambda x: x ** 2 if x % 2 == 0 else x).Take(5).ToList()
    print(drunk_f)

    text = "Ваша реализация должна быть ленивой: например, в первой задаче не нужно генерировать бесконечное количество чисел Фибоначчи, а только потом их фильтровать. Сгенерировано должно быть лишь минимально необходимое их количество – это стоит продемонстрировать явно, например, выводя на экран число при его генерации."
    # print(tokenize_into_words(text))

    word_count = LinqContainer(tokenize_into_words(text))
    word_count.GroupBy().Select(lambda x: (x[0], len(x[1]))).OrderBy(lambda x: -x[1]).ToList()
    print(word_count)


    # print(lis.__flatten_sequence("1"))
    # print(list(filter(lambda x: x.upper(), "self.data")))


if __name__ == '__main__':
    main()
