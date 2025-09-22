import json
import csv
import re


def load_inns(path_txt: str) -> list[str]:
    with open(path_txt, encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]


def load_traders(path_json: str) -> list[dict]:
    with open(path_json, encoding='utf-8') as f:
        return json.load(f)


def save_traders_csv(inns: list[str], traders: list[dict], output_csv: str):
    filtered = [t for t in traders if t.get("inn") in inns]
    with open(output_csv, mode='w', encoding='cp1251', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_ALL)
        writer.writerow(["ИНН", "ОГРН", "Адрес"])
        for t in filtered:
            writer.writerow([
                f'="{t.get("inn", "")}"',
                f'="{t.get("ogrn", "")}"',
                t.get("address", "")
            ])


EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")


def extract_emails(dataset_path: str) -> dict[str, set[str]]:
    result: dict[str, set[str]] = {}
    with open(dataset_path, encoding='utf-8') as f:
        data = json.load(f)
    for msg in data:
        inn = msg.get("publisher_inn")
        text = msg.get("msg_text", "")
        if not inn:
            continue
        emails = set(EMAIL_REGEX.findall(text))
        if emails:
            result.setdefault(inn, set()).update(emails)
    return result


def save_emails_json(emails_dict: dict[str, set[str]], output_json: str):
    serializable = {inn: list(emails) for inn, emails in emails_dict.items()}
    with open(output_json, mode='w', encoding='utf-8') as f:
        json.dump(serializable, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    txt_path = "traders.txt"
    json_path = "traders.json"
    dataset_path = "1000_efrsb_messages.json"

    out_csv = "traders.csv"
    out_emails = "emails.json"

    # Часть 1: создаём CSV
    inns = load_inns(txt_path)
    traders = load_traders(json_path)
    save_traders_csv(inns, traders, out_csv)
    print(f"Сохранён файл {out_csv} с данными {len(inns)} организаций")

    # Часть 2: извлекаем email-адреса
    emails_dict = extract_emails(dataset_path)
    save_emails_json(emails_dict, out_emails)
    print(f"Сохранён файл {out_emails} с адресами от {len(emails_dict)} ИНН")
