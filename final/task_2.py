def roman_to_int(s):
    roman_values = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    }
    result = 0
    for i in range(len(s)):
        # Получаем значение текущей цифры
        current_value = roman_values[s[i]]
        # Если это не последняя цифра
        if i < len(s) - 1:
            # Получаем значение следующей цифры
            next_value = roman_values[s[i + 1]]
            # Если текущая цифра меньше следующей, вычитаем её
            if current_value < next_value:
                result -= current_value
            else:
                result += current_value
        else:
            # Для последней цифры просто добавляем её значение
            result += current_value
    return result
s=input()
print(roman_to_int(s))