"""
Генерирует список ссылок на основе markdown файлов.

# - Заголовок блока меню.
## - заголовок раздела в блоке.
### - подзаголовок раздела в блоке (вложенность может быть до 6).
"""
import os
import json
import re
from pathlib import Path


NOTES_DIR = "notes"
ICONS = {
    "Python": "fa-brands fa-python",
    "Code_Quality": "fa-solid fa-code",
    "Apache_Kafka": "fa-solid fa-lines-leaning",
    "PostgreSQL": "fa-brands fa-postgresql",
    "Architecture": "fa-solid fa-building-columns",
    "Redis": "fa-solid fa-database",
    "Golang": "fa-brands fa-golang",
    "AI": "fa-solid fa-hexagon-nodes",
}


def parse_markdown_headers(file_path, file_name):
    """Парсит заголовки из markdown файла."""
    headers = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            in_code_block = False
            for line in file:
                # Если в строке встречается ``` — переключаем режим
                if '```' in line:
                    in_code_block = not in_code_block
                    continue

                # Внутри блока кода заголовки не ищем
                if in_code_block:
                    continue

                # Ищем заголовки markdown (от # до ######)
                match = re.match(r'^(#{1,6})\s+(.+)$', line.rstrip('\n').rstrip('\r'))
                if match:
                    hashes = match.group(1)
                    level = len(hashes)
                    title = match.group(2).strip()
                    uri = f"{hashes} {title}"
                    headers.append({
                        "level": level,
                        "title": title,
                        "uri": uri
                    })
    except Exception as e:
        print(f"Ошибка при чтении файла {file_path}: {e}")
        # Если не удалось прочитать или файл пустой, используем имя файла
        file_title = Path(file_name).stem.replace('_', ' ').title()
        headers.append({
            "level": 1,
            "title": file_title,
            "uri": f"# {file_title}"
        })

    return headers


def build_hierarchy(headers, file_name):
    """Строит иерархию заголовков до 6 уровня."""
    if not headers:
        return {
            "file": file_name,  # полное имя файла с расширением
            "title": "",
            "uri": "",
            "child": []
        }

    # Создаем корневой узел из первого заголовка
    root = {
        "file": file_name,  # полное имя файла с расширением
        "title": headers[0]["title"],  # без #
        "uri": headers[0]["uri"],  # с #
        "child": []
    }

    # Стек для отслеживания текущего пути в иерархии
    # Каждый элемент стека - (уровень, узел)
    stack = [(headers[0]["level"], root)]

    for i in range(1, len(headers)):
        current_level = headers[i]["level"]
        current_title = headers[i]["title"]  # без #
        current_uri = headers[i]["uri"]  # с #

        # Ищем родительский узел для текущего заголовка.
        # Убираем из стека узлы с уровнем >= текущему.
        while stack and stack[-1][0] >= current_level:
            stack.pop()

        # Если стек пуст, добавляем к корню
        if not stack:
            parent_node = root
        else:
            parent_node = stack[-1][1]

        # Создаем новый узел с атрибутом file
        new_node = {
            "file": file_name,  # полное имя файла с расширением
            "title": current_title,  # без #
            "uri": current_uri,  # с #
            "child": []
        }

        # Добавляем к родителю
        parent_node["child"].append(new_node)

        # Добавляем в стек
        stack.append((current_level, new_node))

    return root


def generate_links_js(show_folders: list[str]):
    """Генерирует JavaScript файл со структурой ссылок."""
    output_file = "lib/links.js"

    if not os.path.exists(NOTES_DIR):
        print(f"Папка '{NOTES_DIR}' не найдена.")
        return

    result = []

    # Проходим по всем подпапкам в notes
    for folder_name in show_folders:
        folder_icon = ICONS.get(folder_name, "fa-regular fa-folder")
        folder_path = os.path.join(NOTES_DIR, folder_name)

        if os.path.isdir(folder_path):
            print(f"Обработка папки: {folder_name}")

            folder_data = {
                "dir": folder_name,  # оригинальное имя папки
                "icon": folder_icon,  # font awesome icon
                "header": folder_name.replace('_', ' '),
                "links": []
            }

            # Ищем markdown файлы в папке
            md_files = []
            for file_name in sorted(os.listdir(folder_path)):
                if file_name.lower().endswith('.md'):
                    md_files.append(file_name)

            for file_name in md_files:
                file_path = os.path.join(folder_path, file_name)
                print(f"  Парсинг файла: {file_name}")

                # Парсим заголовки из файла
                headers = parse_markdown_headers(file_path, file_name)

                if headers:
                    # Строим иерархию заголовков с передачей полного имени файла
                    hierarchy = build_hierarchy(headers, file_name)
                    folder_data["links"].append(hierarchy)
                else:
                    # Если файл без заголовков, используем имя файла
                    title = Path(file_name).stem.replace('_', ' ').title()
                    folder_data["links"].append({
                        "file": file_name,  # полное имя файла с расширением
                        "title": title,  # без #
                        "uri": f"# {title}",  # с #
                        "child": []
                    })

            # Добавляем папку только если в ней есть файлы
            if folder_data["links"]:
                result.append(folder_data)
            else:
                print(f"  Папка '{folder_name}' пуста, пропускаем")

    # Записываем результат в JavaScript файл
    try:
        # Преобразуем результат в JSON строку с правильным форматированием
        json_str = json.dumps(result, ensure_ascii=False, indent=2)

        # Создаем JavaScript содержимое
        js_content = f"const LINKS = {json_str};"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(js_content)

        print(f"\nФайл {output_file} успешно создан.")
        print(f"Обработано {len(result)} папок.")
        print(f"Всего файлов: {sum(len(folder['links']) for folder in result)}")

        # Выводим пример структуры
        if result:
            print("\nПример структуры первого элемента:")
            print(json.dumps(result[0], ensure_ascii=False, indent=2))

    except Exception as e:
        print(f"Ошибка при записи файла: {e}")


if __name__ == "__main__":
    folders = [f for f in sorted(os.listdir(NOTES_DIR)) if f not in ("images",)]

    generate_links_js(folders)
