# lesson2.py

from lesson_2_data import respondents as defendants_data

COURTS = [
    {"code": "А33", "name": "Арбитражный суд Красноярского края",    "address": "660000, г. Красноярск, ул. Мира, д. 76"},
    {"code": "А40", "name": "Арбитражный суд города Москвы",        "address": "115225, г. Москва, ул. Большая Тульская, д. 17"},
    {"code": "А47", "name": "Арбитражный суд Московской области",    "address": "143981, Московская область, г. Красногорск, ул. Карла Маркса, д. 9"},
    {"code": "А56", "name": "Арбитражный суд Омской области",        "address": "644043, г. Омск, ул. Ленина, д. 12"},
    {"code": "А60", "name": "Арбитражный суд Самарской области",     "address": "443099, Самарская обл., г. Самара, ул. Авроры, д. 150"},
    {"code": "А41", "name": "Арбитражный суд Нижегородской области", "address": "603000, г. Нижний Новгород, ул. Большая Покровская, д. 42"},
    {"code": "А53", "name": "Арбитражный суд Иркутской области",     "address": "664020, Иркутская обл., г. Иркутск, ул. Ленина, д. 25"}
]

def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("n должно быть неотрицательным")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def max_of_three(numbers: tuple[int, int, int]) -> int:
    if len(numbers) != 3:
        raise ValueError("Ожидается кортеж из трёх чисел")
    return max(numbers)

def right_triangle_area(cathetus1: float, cathetus2: float) -> float:
    return (cathetus1 * cathetus2) / 2

def get_court_by_code(code: str) -> dict:
    for court in COURTS:
        if court["code"] == code:
            return court
    return {"name": f"Н/Д (код {code})", "address": "Адрес не найден"}

def generate_header(defendant: dict, plaintiff: dict, case_number: str) -> str:
    court_code = case_number.split('-')[0]
    court = get_court_by_code(court_code)
    return (
        f"В {court['name']}\n"
        f"Адрес: {court['address']}\n\n"
        f"Истец: {plaintiff['name']}\n"
        f"ИНН {plaintiff['inn']} ОГРНИП {plaintiff.get('ogrnip', '')}\n"
        f"Адрес: {plaintiff['address']}\n\n"
        f"Ответчик: {defendant.get('short_name', defendant.get('full_name',''))}\n"
        f"ИНН {defendant['inn']} ОГРН {defendant.get('ogrn', '')}\n"
        f"Адрес: {defendant['address']}\n\n"
        f"Номер дела {case_number}"
    )

def generate_all_headers(defendants: list[dict], plaintiff: dict) -> None:
    for defendant in defendants:
        case_number = defendant.get("case_number")
        if not case_number:
            continue
        print(generate_header(defendant, plaintiff, case_number))
        print("\n" + "-" * 40 + "\n")

if __name__ == "__main__":
    plaintiff_data = {
        "name": "Иванов Иван Иванович",
        "inn": "111222333444",
        "ogrnip": "304440000123456",
        "address": "603000, г. Нижний Новгород, ул. Примерная, д. 1"
    }
generate_all_headers(defendants_data, plaintiff_data)