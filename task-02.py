import time
import re
from hyperloglog import HyperLogLog

LOG_FILE = 'lms-stage-access.log'
ERROR_RATE = 0.01  # Похибка HyperLogLog

def load_ip_addresses(file_path):
    ip_addresses = set()  # Використання множини для уникнення дублікатів під час зчитування
    with open(file_path, 'r') as file:
        for line in file:
            # Знаходимо всі IP-адреси в рядку
            match = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
            ip_addresses.update(match)
    return list(ip_addresses)

def exact_count(ip_addresses):
    return len(ip_addresses)

def hyperloglog_count(ip_addresses, error_rate=ERROR_RATE):
    hll = HyperLogLog(error_rate)
    for ip in ip_addresses:
        hll.add(ip)
    return hll.card()

if __name__ == "__main__":
    try:
        ip_addresses = load_ip_addresses(LOG_FILE)

        # HyperLogLog підрахунок
        start_time = time.time()
        hll_result = hyperloglog_count(ip_addresses)
        hll_time = time.time() - start_time

        # Точний підрахунок
        start_time = time.time()
        exact_result = exact_count(ip_addresses)
        exact_time = time.time() - start_time

        # Виведення результатів
        print(f"{'Результати порівняння:':<30}")
        print(f"{' ':<30}{'Точний підрахунок':<20}{'HyperLogLog':<20}")
        print(f"{'Унікальні елементи':<30}{exact_result:<20.0f}{hll_result:<20.0f}")
        print(f"{'Час виконання (сек.)':<30}{exact_time:.4f}    {hll_time:.4f}")
    except FileNotFoundError:
        print(f"Файл {LOG_FILE} не знайдено.")
    except Exception as e:
        print(f"Виникла помилка: {str(e)}")