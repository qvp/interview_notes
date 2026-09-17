"""
Генерирует список ссылок на основе markdown-файлов.

# - Заголовок заметки.
## - Раздел внутри заметки.
"""

import json
import os
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


def parse_markdown(file_path, file_name):
    """Парсит # и ## заголовки из markdown-файла."""
    title = None
    sections = []

    try:
        with open(file_path, encoding="utf-8") as file:
            in_code_block = False

            for line in file:
                if "```" in line:
                    in_code_block = not in_code_block
                    continue

                if in_code_block:
                    continue

                line = line.rstrip()

                match = re.match(r"^(#{1,2})\s+(.+)$", line)
                if not match:
                    continue

                level, text = len(match.group(1)), match.group(2).strip()

                if level == 1:
                    title = text
                else:
                    sections.append({
                        "file": file_name,
                        "title": text,
                        "uri": f"## {text}",
                        "child": [],
                    })

    except Exception as e:
        print(f"Ошибка при чтении файла {file_path}: {e}")

    if title is None:
        title = Path(file_name).stem.replace("_", " ").title()

    return {
        "file": file_name,
        "title": title,
        "uri": f"# {title}",
        "child": sections,
    }


def generate_links_js(folders):
    """Генерирует lib/links.js."""
    output_file = "lib/links.js"

    if not os.path.isdir(NOTES_DIR):
        print(f"Папка '{NOTES_DIR}' не найдена.")
        return

    result = []

    for folder_name in folders:
        folder_path = os.path.join(NOTES_DIR, folder_name)

        if not os.path.isdir(folder_path):
            continue

        print(f"Обработка папки: {folder_name}")

        folder_data = {
            "dir": folder_name,
            "icon": ICONS.get(folder_name, "fa-regular fa-folder"),
            "header": folder_name.replace("_", " "),
            "links": [],
        }

        for file_name in sorted(os.listdir(folder_path)):
            if not file_name.lower().endswith(".md"):
                continue

            print(f"  Парсинг файла: {file_name}")

            file_path = os.path.join(folder_path, file_name)
            folder_data["links"].append(
                parse_markdown(file_path, file_name)
            )

        if folder_data["links"]:
            result.append(folder_data)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Преобразуем результат в JSON строку с правильным форматированием
    json_str = json.dumps(result, ensure_ascii=False, indent=2)

    # Создаем JavaScript содержимое
    js_content = f"const LINKS = {json_str};"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(js_content)

    print(f"\nФайл {output_file} успешно создан.")
    print(f"Обработано папок: {len(result)}")
    print(
        f"Всего файлов: "
        f"{sum(len(folder['links']) for folder in result)}"
    )


if __name__ == "__main__":
    folders = sorted(
        folder
        for folder in os.listdir(NOTES_DIR)
        if folder != "images"
    )

    generate_links_js(folders)
