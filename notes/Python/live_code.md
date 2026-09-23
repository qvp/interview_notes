# Live codding

## Dict
<!-- junior 3525480 -->
**clear()**	удалить все элементы  
**copy()** возвращает поверхностную копию  
**fromkeys(keys: List, default_value=None)** возвращает словарь с ключами и значением по умолчанию  
**get(key, default_value=None)** получить значение по ключу или по умолчанию  
**items()** возвращает список кортежей ключ-значение  
**keys()** возвращает список ключей  
**pop(keyname, default_value=None)** удаляет значение по ключу и возвращает его или по умолчанию  
**popitem()** удаляет и возвращает последнюю добавленную пару ключ-значение в виде кортежа  
**setdefault(key, default_value=None)** вставляет значение если такого ключа нет и возвращает значение  
**update()** обновить словарь используя другой словарь  
**values()** возвращает список значений  

## List
<!-- junior 3525480 -->
**append()** добавляет элемент в конец списка  
**clear()**	удаляет все элементы списка  
**copy()** возвращает поверхностную копию, как и \[:]  
**count(value)** возвращает количество вхождений элемента в список  
**extend(list|iterable)** добавляет несколько значений в конец списка  
**index(value)** возвращает индекс первого найденного элемента или ValueError  
**insert(index, value)** вставляет элемент в указанную позицию сдвигая другие элементы  
**pop(index: Optional)** удаляет элемент по индексу и возвращает его  
**remove(value)** удаляет значение из списка, если его нет то ValueError  
**reverse()** меняет порядок элементов в исходном списке на противоположный  
**sort(reverse=True|False, key=myFunc)** сортирует исходный список  

## Str
<!-- junior 3525480 -->
**center(len, char)** дополнить строку по бокам до указанной длинны  
**count(value, start, end)** посчитать количество элементов  
**endswith(value, start, end)** возвращает True если строка заканчивается строкой  
**find(value, start, end)** возвращает index первой найденной строки  
**rfind(value, start, end)** возвращает index последней найденной строки  
**ljust(length, character)** дополнить строку слева  
**partition(value)** возвращает строку до вхождения, саму строку и строку после вхождения  
**strip(characters)** возвращает новую строку без указанных символов (по умолчанию пробелов)  
**zfill(len)** заполняет строку нулями до указанной длинны  

## Tuple
<!-- junior 3525480 -->
**count(value)** возвращает количество вхождений элемента в кортеж  
**index(value)** возвращает индекс первого найденного элемента или ValueError  

## Set
<!-- junior 3525480 -->
**add(value)** добавить значение  
**clear()**	удаляет все элементы списка  
**copy()** возвращает поверхностную копию  
**discard(value)** удалить значение без исключения  
**pop()** удаляет произвольный элемент, KeyError если множество пустое  


## Фибоначчи
<!-- junior 3525480 -->
Числа Фибоначчи - элементы числовой последовательности, в которой первые два числа равны 0 и 1, а каждое последующее число равно сумме двух предыдущих чисел.

Напишите программу, которая построит список чисел Фибоначчи от 0 до n:
```python
def fib(n: int):
    numbers = [0, 1]
    for i in range(2, n):
        numbers.append(numbers[i - 2] + numbers[i - 1])
    return numbers
```

N-е число Фибоначчи:
```python
def fib_n(n):
    if n in (1, 2):
        return 1
    return fib_n(n - 1) + fib_n(n - 2)
```

## Факториал
<!-- junior 3525480 -->
Факториалом числа называют произведение всех натуральных чисел до него включительно.  
Например, факториал числа 5 равен произведению 1 * 2 * 3 * 4 * 5 = 120.

```python
def fact(n):
    res = 1
    while n > 1:
        res *= n
        n -= 1
    return res
```

```python
def fact(n):
    if n == 0:
        return 1
    return n * fact(n - 1)
```

## Сортировка методом "пузырька"
<!-- junior 3525480 -->
```python
def sort_buble(*args):
    items = list(args)
    for i in range(len(items)):
        for j in range(len(items) - 1):
            if items[j] > items[j + 1]:
                items[j], items[j + 1] = items[j + 1], items[j]
    return items
```

## Изменить порядок слов
<!-- junior 3525480 -->
```python
def words_reverse(words_str):
    words_list = words_str.split(' ')
    return ' '.join(w.strip() for w in words_list[::-1] if w != '')
```

## Частота символов в строке
<!-- junior 3525480 -->
```python
def char_count(s: str):
    res = {}
    for c in s:
        res.setdefault(c, 0)
        res[c] += 1
    return res
```

## Поиск второго наибольшего числа в списке
<!-- junior 3525480 -->
```python
from math import inf

def sb(numbers):
    biggest = second_big_num = -inf
    for n in numbers:
        if n > biggest:
            second_big_num = biggest
            biggest = n
        elif n > second_big_num and n != biggest:
            second_big_num = n
    return second_big_num
```

```python
def second_big(x):
    first = 0  # тут будет 1-й по размеру элемент
    second = 0  # тут будет 2-й по размеру элемент

    for i in range(len(x)):
        if x[i] > first and x[i] > second:
            """ Он на первом месте! Бывший чемпион смещается на второе место """
            second = first
            first = x[i]
        elif first > x[i] > second:
            """ Он на втором месте """
            second = x[i]
        else:
            """ Он меньше всех """
            pass

    return second
```

## Отсортировать массив сохраняя позиции четных элементов
<!-- junior 3525480 -->
Желательно вернуть тот же список и учесть, что размер списка может быть большим.

Вход: \[20, 1, 20, -1, 20, 1111, 11, 20, 111]  
Выход: \[20, -1, 20, 1, 20, 11, 111, 20, 1111]  

```python
def magic_sort(lst):
    even = {idx: item for idx, item in enumerate(lst) if item % 2 == 0}
    odd = [item for item in lst if item % 2]

    odd.sort()

    for k, v in even.items():
        odd.insert(k, v)

    return odd
```
