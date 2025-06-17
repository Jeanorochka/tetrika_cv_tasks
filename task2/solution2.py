#!/usr/bin/env python3
"""
скрипт получает со страницы категории "животные по алфавиту" википедии
список всех страниц‑участников категории и подсчитывает, сколько названий
начинается на каждую букву. Результат сохраняется в файл beasts.csv в формате
~буква,количество~.

dlya requirements.txt: requests (pip install requests)
"""
import csv
import collections
import requests
from typing import Iterator

API_URL = "https://ru.wikipedia.org/w/api.php"
CATEGORY = "Животные_по_алфавиту"
OUTPUT_FILE = "beasts.csv"


def fetch_titles(category: str) -> Iterator[str]:
    """итерирует заголовки всех страниц из указанной категории википедии."""
    cmcontinue = None
    while True:
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": f"Category:{category}",
            "cmlimit": "500",  # максимум за один запрос
            "cmtype": "page",   # игнорируем подкатегории и файлы
            "format": "json",
        }
        if cmcontinue:
            params["cmcontinue"] = cmcontinue

        response = requests.get(API_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        for page in data["query"]["categorymembers"]:
            yield page["title"]

        # Проверяем, есть ли продолжение
        if "continue" in data:
            cmcontinue = data["continue"]["cmcontinue"]
        else:
            break


def count_by_initial(titles: Iterator[str]) -> collections.Counter:
    """подсчитывает количество названий, начинающихся с каждой буквы."""
    counts: collections.Counter[str] = collections.Counter()
    for title in titles:
        if not title:
            continue
        first_char = title[0].upper()
        counts[first_char] += 1
    return counts


def write_csv(counts: collections.Counter, filename: str = OUTPUT_FILE) -> None:
    """записывает результаты в csv без заголовка"""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # Сортируем по алфавиту (Unicode‑порядок). При необходимости можно настроить
        for letter in sorted(counts):
            writer.writerow([letter, counts[letter]])


def main() -> None:
    titles = fetch_titles(CATEGORY)
    counts = count_by_initial(titles)
    write_csv(counts)
    print(f"готово. результаты сохранены в {OUTPUT_FILE}")

def test_count_by_initial():
    sample_titles = [
        "Акула", "Аист", "Бобр", "Барсук", "Воробей", "Выхухоль",
        "Гусь", "Горностай", "Тигр", "Ёжик", "Жук", "Жираф", "Зебра", "Заяц",
    ]
    expected = {
        "А": 2,
        "Б": 2,
        "В": 2,
        "Г": 2,
        "Ё": 1,
        "Ж": 2,
        "З": 2,
        "Т": 1
    }

    result = count_by_initial(sample_titles)

    for letter, count in expected.items():
        assert result.get(letter, 0) == count, f"ошибка в подсчёте для буквы {letter}: ожидалось {count}, получено {result.get(letter, 0)}"
    
    print("Тест count_by_initial прошёл успешно.")

if __name__ == "__main__":
    test_count_by_initial()  
    main()
