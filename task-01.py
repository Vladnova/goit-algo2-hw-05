import hashlib

class BloomFilter:
    def __init__(self, size, num_hashes):
        """Ініціалізація фільтра Блума.

        :param size: Розмір бітового масиву.
        :param num_hashes: Кількість хеш-функцій.
        """

        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def _hash(self, element, seed):
        """Створення хешу для елемента з певним сідом."""
        hash_value = hashlib.md5((str(seed) + element).encode()).hexdigest()
        return int(hash_value, 16) % self.size

    def add(self, element):
        """Додавання елемента до фільтра Блума."""
        for i in range(self.num_hashes):
            hash_value = self._hash(element, i)
            self.bit_array[hash_value] = 1

    def check(self, element):
        """Перевірка, чи елемент вже є у фільтрі."""
        for i in range(self.num_hashes):
            hash_value = self._hash(element, i)
            if self.bit_array[hash_value] == 0:
                return False
        return True

def check_password_uniqueness(bloom_filter, passwords):
    """Перевірка на унікальність паролів за допомогою фільтра Блума.

    :param bloom_filter: Екземпляр BloomFilter.
    :param passwords: Список нових паролів для перевірки.
    :return: Результат перевірки для кожного пароля.
    """
    results = {}
    for password in passwords:
        if bloom_filter.check(password):
            results[password] = 'вже використаний'
        else:
            bloom_filter.add(password)
            results[password] = 'унікальний'
    return results

if __name__ == "__main__":
    # Ініціалізація фільтра Блума
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Додавання існуючих паролів
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    # Перевірка нових паролів
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Виведення результатів
    for password, status in results.items():
        print(f"Пароль '{password}' — {status}.")
