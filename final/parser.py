
import requests
import xml.etree.ElementTree as ET
import json
from pathlib import Path
from datetime import datetime, timedelta
from decimal import Decimal

class ParserCBRF:
    def __init__(self, start_date=None, end_date=None, currencies=None):
        self.start_date = start_date
        self.end_date = end_date
        self.currencies = currencies or ['USD', 'EUR', 'CNY']
        self.base_url = 'https://www.cbr.ru/scripts/XML_daily.asp'
        self.rates_data = []

    def get_currency_rates(self, date=None):
        url = self.base_url
        if date:
            url = f'{url}?date_req={date}'
        try:
            response = requests.get(url, timeout=10)
            response.encoding = 'windows-1251'
            if response.status_code != 200:
                return None
            root = ET.fromstring(response.content)
            rates_date = root.attrib.get('Date')
            currency_rates = {'date': rates_date, 'currencies': {}}
            for valute in root.findall('Valute'):
                char_code = valute.find('CharCode').text
                num_code = valute.find('NumCode').text
                nominal = int(valute.find('Nominal').text)
                name = valute.find('Name').text
                value = float(valute.find('Value').text.replace(',', '.'))
                currency_rates['currencies'][char_code] = {
                    'num_code': num_code, 'name': name, 'nominal': nominal,
                    'value': value, 'rate_per_unit': value / nominal
                }
            return currency_rates
        except Exception as e:
            print(f"Ошибка получения данных: {e}")
            return None

    def serialize_single_currency(self, rates_list, currency_code):
        return {
            rate['date']: f"{rate['currencies'][currency_code]['value']:.4f}"
            for rate in rates_list
            if rate and currency_code in rate['currencies']
        }

    def serialize_currency_rates_by_date(self, rates_list):
        return {
            rate['date']: {
                code: f"{info['value']:.4f}"
                for code, info in rate['currencies'].items()
            }
            for rate in rates_list if rate
        }

    def deserialize_currency_data(self, serialized_data):
        return {
            datetime.strptime(date, '%d.%m.%Y'): (
                {code: Decimal(value) for code, value in currencies.items()}
                if isinstance(currencies, dict)
                else Decimal(currencies)
            )
            for date, currencies in serialized_data.items()
        }

    def fill_missing_dates(self, currency_rates_dict):
        if not currency_rates_dict:
            return {}
        dates_values = {
            datetime.strptime(date, '%d.%m.%Y'): value
            for date, value in currency_rates_dict.items()
        }
        sorted_dates = sorted(dates_values.keys())
        if len(sorted_dates) == 0:
            return {}
        filled_dict = {}
        last_value = None
        current_date = sorted_dates[0]
        while current_date <= sorted_dates[-1]:
            if current_date in dates_values:
                last_value = dates_values[current_date]
                filled_dict[current_date.strftime('%Y-%m-%d')] = str(last_value)
            elif last_value is not None:
                filled_dict[current_date.strftime('%Y-%m-%d')] = str(last_value)
            current_date += timedelta(days=1)
        return filled_dict

    def get_parsed_data_path(self):
        script_dir = Path(__file__).parent.resolve()
        parsed_data_dir = script_dir / 'parsed_data'
        parsed_data_dir.mkdir(exist_ok=True)
        return parsed_data_dir

    def save_to_json(self, data, filename):
        parsed_data_dir = self.get_parsed_data_path()
        filepath = parsed_data_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Сохранено: {filepath}")
        return filepath

    def load_from_json(self, filename):
        parsed_data_dir = self.get_parsed_data_path()
        filepath = parsed_data_dir / filename
        if not filepath.exists():
            return None
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def generate_date_range(self, start_date_str, end_date_str):
        start = datetime.strptime(start_date_str, '%d.%m.%Y')
        end = datetime.strptime(end_date_str, '%d.%m.%Y')
        dates = []
        current = start
        while current <= end:
            dates.append(current.strftime('%d.%m.%Y'))
            current += timedelta(days=1)
        return dates

    def fetch_data(self):
        if self.start_date and self.end_date:
            dates = self.generate_date_range(self.start_date, self.end_date)
        else:
            dates = [None]
        print(f"Получение данных за {len(dates)} дат...")
        self.rates_data = []
        for date in dates:
            rates = self.get_currency_rates(date)
            if rates:
                self.rates_data.append(rates)
        print(f"Получено данных: {len(self.rates_data)} дат")
        return self.rates_data

    def process_currencies(self, fill_gaps=True):
        results = {}
        for currency in self.currencies:
            print(f"Обработка {currency}...")
            serialized = self.serialize_single_currency(self.rates_data, currency)
            if fill_gaps:
                filled = self.fill_missing_dates(serialized)
                results[currency] = filled
            else:
                results[currency] = serialized
            filename = f"{currency.lower()}_rates.json"
            self.save_to_json(results[currency], filename)
        return results

    def start(self, fill_gaps=True):
        print("="*70)
        print("ЗАПУСК ПАРСЕРА ЦБ РФ")
        print("="*70)
        self.fetch_data()
        if not self.rates_data:
            print("Нет данных для обработки")
            return None
        results = self.process_currencies(fill_gaps=fill_gaps)
        print("\n" + "="*70)
        print("ПАРСЕР ЗАВЕРШИЛ РАБОТУ")
        print("="*70)
        print(f"Обработано валют: {len(results)}")
        for currency, data in results.items():
            print(f"{currency}: {len(data)} записей")
        return results

class CurrencyRateCBRF:
    def __init__(self, currency_code, data_file=None):
        self.currency_code = currency_code.upper()
        self.data_file = data_file or f"{currency_code.lower()}_rates.json"
        self.data = self._load_data()

    def _get_parsed_data_path(self):
        script_dir = Path(__file__).parent.resolve()
        return script_dir / 'parsed_data'

    def _load_data(self):
        filepath = self._get_parsed_data_path() / self.data_file
        if not filepath.exists():
            raise FileNotFoundError(f"Файл {filepath} не найден")
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def rate_by_date(self, date):
        if isinstance(date, datetime):
            date = date.strftime('%Y-%m-%d')
        return self.data.get(date)

    def rate_last(self):
        if not self.data:
            return None
        sorted_dates = sorted(self.data.keys())
        return self.data[sorted_dates[-1]]

    def rate_first(self):
        if not self.data:
            return None
        sorted_dates = sorted(self.data.keys())
        return self.data[sorted_dates[0]]

    def rate_range_dates(self, from_date, to_date):
        if isinstance(from_date, datetime):
            from_date = from_date.strftime('%Y-%m-%d')
        if isinstance(to_date, datetime):
            to_date = to_date.strftime('%Y-%m-%d')
        return [
            (date, value)
            for date, value in sorted(self.data.items())
            if from_date <= date <= to_date
        ]

    def rate_min(self):
        if not self.data:
            return None
        min_date = min(self.data.items(), key=lambda x: Decimal(x[1]))
        return min_date

    def rate_max(self):
        if not self.data:
            return None
        max_date = max(self.data.items(), key=lambda x: Decimal(x[1]))
        return max_date

    def rate_average(self, from_date=None, to_date=None):
        if from_date and to_date:
            data_range = dict(self.rate_range_dates(from_date, to_date))
        else:
            data_range = self.data
        if not data_range:
            return None
        values = [Decimal(v) for v in data_range.values()]
        return str(sum(values) / len(values))

    def rate_dates_list(self):
        return sorted(self.data.keys())

    def rate_count(self):
        return len(self.data)

    def rate_exists(self, date):
        if isinstance(date, datetime):
            date = date.strftime('%Y-%m-%d')
        return date in self.data

    def rate_get_all(self):
        return dict(sorted(self.data.items()))


if __name__ == "__main__":

    parser = ParserCBRF(
        start_date='07.04.2022',
        end_date='13.04.2022',
        currencies=['USD', 'EUR', "CNY"]
    )
    results = parser.start()
    usd = CurrencyRateCBRF('USD')

    print(f"\nКурс на 2022-04-07: {usd.rate_by_date('2022-04-07')}")
    print(f"Последний курс: {usd.rate_last()}")

    print("\nКурсы за период:")
    rates = usd.rate_range_dates('2022-04-07', '2022-04-13')
    for date, value in rates[:5]:
        print(f"  {date}: {value}")

    print(f"\nМинимальный курс: {usd.rate_min()}")
    print(f"Максимальный курс: {usd.rate_max()}")
    print(f"Средний курс: {usd.rate_average('2022-04-07', '2022-04-13')}")