"""
Генерирует список ссылок на основе markdown-файлов.

# - Заголовок заметки.
## - Раздел внутри заметки.

После каждого ## заголовка должен идти комментарий:

<!-- junior 3283858 3923237 -->

где:
- первое поле — уровень автора/заметки: junior, middle или senior;
- остальные поля — числовые ID авторов.
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

VALID_LEVELS = {"junior", "middle", "senior"}

METADATA_PATTERN = re.compile(
    r"^<!--\s+(junior|middle|senior)(?:\s+(\d+(?:\s+\d+)*))\s+-->$"
)


def parse_metadata(line, file_path):
    """Парсит уровень и авторов из HTML-комментария."""
    line = line.strip()

    match = METADATA_PATTERN.match(line)

    if not match:
        raise ValueError(
            f"{file_path}: некорректный комментарий метаданных: {line!r}. "
            f"Ожидается формат: "
            f"'<!-- junior 123456 -->'"
        )

    level = match.group(1)
    authors = [
        int(author_id)
        for author_id in match.group(2).split()
    ]

    return level, authors


def parse_markdown(file_path, file_name):
    """Парсит # и ## заголовки из markdown-файла."""
    title = None
    sections = []

    try:
        with open(file_path, encoding="utf-8") as file:
            lines = list(file)

        in_code_block = False
        i = 0

        while i < len(lines):
            line = lines[i]
            stripped_line = line.rstrip()

            # ---------------------------------------------------------
            # Блок кода вне заметки
            # ---------------------------------------------------------
            if stripped_line.strip().startswith("```"):
                in_code_block = not in_code_block
                i += 1
                continue

            if in_code_block:
                i += 1
                continue

            # ---------------------------------------------------------
            # Заголовок
            # ---------------------------------------------------------
            match = re.match(
                r"^(#{1,2})\s+(.+)$",
                stripped_line,
            )

            if not match:
                i += 1
                continue

            heading_level = len(match.group(1))
            text = match.group(2).strip()

            # ---------------------------------------------------------
            # # Заголовок файла
            # ---------------------------------------------------------
            if heading_level == 1:
                title = text
                i += 1
                continue

            # ---------------------------------------------------------
            # ## Новая заметка
            # ---------------------------------------------------------

            # Metadata должна быть сразу после ##.
            if i + 1 >= len(lines):
                raise ValueError(
                    f"{file_path}: у заметки "
                    f"'## {text}' отсутствует комментарий "
                    f"с уровнем и авторами."
                )

            metadata_line = lines[i + 1]

            level, authors = parse_metadata(
                metadata_line,
                file_path,
            )

            # Начало содержимого заметки.
            content_start = i + 2

            # Ищем конец заметки.
            j = content_start
            in_section_code_block = False

            while j < len(lines):
                current_line = lines[j]
                current_stripped = current_line.rstrip()

                # Переключаем состояние code block.
                if current_stripped.strip().startswith("```"):
                    in_section_code_block = not in_section_code_block
                    j += 1
                    continue

                # ## внутри code block не является новой заметкой.
                if not in_section_code_block:
                    next_heading = re.match(
                        r"^##\s+(.+)$",
                        current_stripped,
                    )

                    if next_heading:
                        break

                j += 1

            content = lines[content_start:j]

            is_empty = not any(
                line.strip()
                for line in content
            )

            sections.append({
                "file": file_name,
                "title": text,
                "uri": f"## {text}",
                "level": level,
                "authors": authors,
                "is_empty": is_empty,
            })

            # Переходим сразу к следующему ##.
            i = j

    except Exception as e:
        raise RuntimeError(
            f"Ошибка при обработке файла {file_path}: {e}"
        ) from e

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

            file_path = os.path.join(
                folder_path,
                file_name,
            )

            folder_data["links"].append(
                parse_markdown(file_path, file_name)
            )

        if folder_data["links"]:
            result.append(folder_data)

    os.makedirs(
        os.path.dirname(output_file),
        exist_ok=True,
    )

    json_str = json.dumps(
        result,
        ensure_ascii=False,
        indent=2,
    )

    js_content = f"const LINKS = {json_str};"

    with open(
            output_file,
            "w",
            encoding="utf-8",
    ) as file:
        file.write(js_content)

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
