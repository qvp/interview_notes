# Examples

## Чтения данных из сети по URL в строку
```go
url := "https://example.com" // Замените на нужный URL

// Отправляем GET-запрос
resp, err := http.Get(url)
if err != nil {
    log.Fatalf("Ошибка при запросе: %v", err)
}
defer resp.Body.Close() // Закрываем тело ответа

// Читаем тело ответа в строку
body, err := io.ReadAll(resp.Body)
if err != nil {
    log.Fatalf("Ошибка при чтении ответа: %v", err)
}

// Выводим результат
fmt.Println(string(body))
```

## Чтение локального файла построчно
```go
filePath := "test.txt" // Укажите путь к файлу

// Открываем файл
file, err := os.Open(filePath)
if err != nil {
    log.Fatalf("Ошибка при открытии файла: %v", err)
}
defer file.Close() // Закрываем файл в конце

// Создаём сканер для чтения файла построчно
scanner := bufio.NewScanner(file)

// Читаем и выводим каждую строку
lineNum := 1
for scanner.Scan() {
    line := scanner.Text()
    fmt.Printf("Строка %d: %s\n", lineNum, line)
    lineNum++
}

// Проверяем на ошибки сканирования
if err := scanner.Err(); err != nil {
    log.Fatalf("Ошибка при чтении файла: %v", err)
}
```