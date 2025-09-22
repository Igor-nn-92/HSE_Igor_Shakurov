"""
Задание 1.
Создайте несколько переменных разных типов, выведите их значения и адреса в памяти.
Запросите у пользователя числа и строки, сохраните их в переменные и также выведите.
"""

a = 10
b = 3.14
c = "Привет, мир!"
print("Значение a =", a)
print("Адрес a (id):", id(a))
print("Значение b =", b)
print("Адрес b (id):", id(b))
print("Значение c =", c)
print("Адрес c (id):", id(c))

user_num = input("Введите любое число: ")
user_str = input("Введите любую строку: ")
print("Вы ввели число:", user_num, "с адресом", id(user_num))
print("Вы ввели строку:", user_str, "с адресом", id(user_str))


"""
Задание 2.
Пользователь вводит время в секундах.
Вычислите, сколько это часов, минут и секунд, сохраните в отдельные переменные и выведите.
"""

seconds_input = input("Введите время в секундах (только цифры): ")
if not seconds_input.isdigit():
    print("Ошибка: введены не только цифры.")
else:
    total_seconds = int(seconds_input)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    print("Часы:", hours)
    print("Минуты:", minutes)
    print("Секунды:", seconds)


"""
Задание 3.
Пользователь вводит цифру n (от 1 до 9).
Найдите сумму n + nn + nnn и выведите результат.
"""

n = input("Введите цифру от 1 до 9: ")
if not (n.isdigit() and 1 <= int(n) <= 9):
    print("Ошибка: нужно ввести цифру от 1 до 9.")
else:
    n_int = int(n)
    term1 = n
    term2 = n * 2
    term3 = n * 3
    result = n_int + int(term2) + int(term3)
    print(f"{n} + {term2} + {term3} =", result)
