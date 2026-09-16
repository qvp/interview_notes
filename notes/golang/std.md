# Std

## fmt
Форматированный ввод/вывод.
```go
fmt.Print("Hello")                        // Вывод без перевода строки  
fmt.Println("Hello")                      // Вывод с переводом строки  
fmt.Printf("Name: %s Age: %d", "Bob", 25) // Форматированный вывод  
fmt.Fprint(os.Stdout, "Hi")               // Запись в io.Writer  
s := fmt.Sprintf("%d items", 5)           // Возвращает форматированную строку  
er := fmt.Errorf("error: %v", err)        // Создание ошибки с форматированием

fmt.Scan(&name)                           // Чтение из stdin в переменную  
fmt.Scanf("%s %d", &name, &age)           // Форматированное чтение  
fmt.Sscan("10 20", &a, &b)                // Чтение из строки   
fmt.Println(fmt.Scanln(&x))               // Чтение строки до \n  
```

## os
Взаимодействие с ОС (работа с файлами, аргументами командной строки, переменными окружения).
```go
file, _ := os.Open("file.txt")            // Открытие файла для чтения  
file, _ := os.Create("file.txt")          // Создание файла (если есть — перезаписывает)  
file, _ := os.OpenFile("file.txt", os.O_APPEND|os.O_WRONLY, 0644) // Открытие с флагами  
file.Close()                              // Закрытие файла (обязательно!)  
data, _ := os.ReadFile("file.txt")        // Чтение всего файла в []byte  
os.WriteFile("file.txt", data, 0644)      // Запись []byte в файл (перезаписывает)  

os.Mkdir("dir", 0755)                     // Создание директории  
os.MkdirAll("dir/subdir", 0755)           // Рекурсивное создание директорий  
os.Remove("file.txt")                     // Удаление файла  
os.RemoveAll("dir")                       // Рекурсивное удаление директории  
os.Rename("old.txt", "new.txt")           // Переименование/перемещение  
files, _ := os.ReadDir(".")               // Чтение содержимого директории  

args := os.Args                           // Аргументы командной строки ([]string)  
val := os.Getenv("HOME")                  // Получение переменной окружения  
os.Setenv("KEY", "value")                 // Установка переменной окружения  

os.Exit(1)                                // Немедленное завершение программы с кодом  
pid := os.Getpid()                        // Получение PID текущего процесса  
host, _ := os.Hostname()                  // Получение имени хоста  

cwd, _ := os.Getwd()                      // Текущая рабочая директория  
os.Chdir("/tmp")                          // Смена рабочей директории  
os.Stdout.Write([]byte("Hi"))             // Доступ к stdin/stdout/stderr  
```

## io
Базовые интерфейсы ввода-вывода.
```go
var r io.Reader  // Интерфейс для чтения
var w io.Writer  // Интерфейс для записи
var c io.Closer  // Интерфейс для закрытия ресурсов
offset, err := io.SeekStart   // Константа для позиционирования
var _ io.ReadWriter           // Комбинированный интерфейс
var _ io.ReadCloser           // Reader + Closer

n, err := io.Copy(w, r)          // Копирует из Reader в Writer до EOF
n, err := io.CopyN(w, r, 1024)   // Копирует N байт
b, err := io.ReadAll(r)          // Читает всё до EOF в []byte
n, err := io.WriteString(w, "s") // Записывает строку в Writer

r = io.LimitReader(r, 100)      // Ограничивает чтение N байтами
r = io.MultiReader(r1, r2)      // Объединяет несколько Reader'ов
w = io.MultiWriter(w1, w2)      // Пишет в несколько Writer'ов
r = io.TeeReader(r, w)          // Читает из r и параллельно пишет в w
s := io.NewSectionReader(r, 0, 100) // Читает определённый участок
```

## bufio
Буферизованный ввод-вывод (чтение/запись построчно).
```go
reader := bufio.NewReader(os.Stdin)       // Создает буферизованный Reader
line, _ := reader.ReadString('\n')        // Читает строку до разделителя
data, _ := reader.ReadBytes('\n')         // Читает байты до разделителя
b, _ := reader.Peek(5)                    // Просматривает N байт без чтения

writer := bufio.NewWriter(os.Stdout)      // Создает буферизованный Writer
writer.WriteString("Hello")               // Записывает строку в буфер
writer.Flush()                            // Сбрасывает буфер в Writer

scanner := bufio.NewScanner(os.Stdin)         // Создает Scanner для построчного чтения
for scanner.Scan() { text := scanner.Text() } // Читает очередную строку
scanner.Bytes()                               // Возвращает текущую строку как []byte
```

## encoding/json
Работа с JSON (маршалинг и анмаршалинг).
```go
data, _ := json.Marshal(user)                 // Преобразует структуру в JSON ([]byte)  
data, _ := json.MarshalIndent(user, "", "  ") // Форматированный JSON с отступами  

json.Unmarshal(jsonData, &user)           // Парсит JSON в структуру  
json.NewEncoder(writer).Encode(user)      // Пишет JSON в io.Writer  
json.NewDecoder(reader).Decode(&user)     // Читает JSON из io.Reader  
```

## strconv
Преобразование строк в числа и обратно.
```go
i, e := strconv.Atoi("42")                 // Строка → int (парсинг целого)  
s := strconv.Itoa(42)                      // int → строка  
f, _ := strconv.ParseFloat("3.14", 64)     // Строка → float64  
s := strconv.FormatFloat(3.14, 'f', 2, 64) // float64 → строка (2 знака после точки)  

i, _ := strconv.ParseInt("1010", 2, 64)  // Двоичная строка → int64  
s := strconv.FormatInt(42, 16)           // int64 → шестнадцатеричная строка  

b, _ := strconv.ParseBool("true")        // Строка → bool ("1", "t", "true" → true)  
s := strconv.FormatBool(true)            // bool → строка ("true"/"false")  

q := strconv.Quote("Hello\tWorld!")      // Экранирует спецсимволы → `"Hello\tWorld!"`  
q := strconv.QuoteToASCII("Привет")      // Экранирует Unicode → `"\u041f\u0440\u0438\u0432\u0435\u0442"`  
r := strconv.QuoteRune('☺')             // Руна → экранированная строка `'☺'`  
```

## strings
Операции со строками (поиск, замена, разбиение).
```go
strings.Contains("hello", "ell")         // true если подстрока найдена
strings.HasPrefix("file.txt", "file")    // true если строка начинается с префикса
strings.HasSuffix("file.txt", ".txt")    // true если строка заканчивается суффиксом
strings.Index("hello", "l")              // индекс первого вхождения подстроки (2)
strings.LastIndex("hello", "l")          // индекс последнего вхождения (3)

strings.ToLower("HELLO")                 // "hello" (нижний регистр)
strings.ToUpper("hello")                 // "HELLO" (верхний регистр)
strings.Trim(" hello ", " ")             // "hello" (удаляет пробелы по краям)
strings.TrimSpace(" \thello\n ")         // "hello" (удаляет все whitespace)
strings.Replace("oink", "o", "m", 1)     // "moink" (замена N вхождений)

strings.Split("a,b,c", ",")              // []string{"a", "b", "c"}
strings.Join([]string{"a", "b"}, "-")    // "a-b" (объединение через разделитель)
strings.Fields("a b  c")                 // []string{"a", "b", "c"} (по whitespace)

strings.Repeat("a", 3)                   // "aaa" (повтор строки N раз)
strings.ReplaceAll("oink", "o", "m")     // "mink" (замена всех вхождений)

strings.Compare("a", "b")                // -1 (лексикографическое сравнение)
strings.EqualFold("Go", "go")            // true (без учета регистра)

strings.Count("cheese", "e")             // 3 (количество вхождений)
strings.TrimLeft("hello", "he")          // "llo" (удаляет символы с начала)
strings.TrimRight("hello", "lo")         // "he" (удаляет символы с конца)

builder := strings.Builder{}             // Эффективная конкатенация строк за счет буфера
builder.WriteString("hello")             // Добавление строки в билдер
```

## bytes
Работа с байтовыми срезами (аналогично `strings`, но для `[]byte`).
```go
b := bytes.Buffer{}                     // Создает буфер для эффективной работы с []byte
b.Write([]byte("hello"))               // Записывает байты в буфер
b.WriteString(" world")                // Записывает строку в буфер
b.Bytes()                              // Возвращает содержимое как []byte
b.String()                             // Возвращает содержимое как string

bytes.Contains([]byte("hello"), []byte("ell"))  // true если подпоследовательность найдена
bytes.Equal([]byte("abc"), []byte("abc"))      // true если слайсы байт идентичны
bytes.Index([]byte("hello"), []byte("l"))      // 2 (индекс первого вхождения)
bytes.HasPrefix([]byte("file.txt"), []byte("file")) // true если начинается с префикса

bytes.ToLower([]byte("HELLO"))          // []byte("hello") (нижний регистр)
bytes.ToUpper([]byte("hello"))          // []byte("HELLO") (верхний регистр)
bytes.Trim([]byte(" hello "), " ")      // []byte("hello") (удаляет указанные байты)
bytes.Replace([]byte("oink"), []byte("o"), []byte("m"), 1) // []byte("moink")

bytes.Split([]byte("a,b,c"), []byte(",")) // [][]byte{[]byte("a"), []byte("b"), ...}
bytes.Join([][]byte{[]byte("a"), []byte("b")}, []byte("-")) // []byte("a-b")
bytes.Fields([]byte("a b  c"))           // Разделяет по whitespace

r := bytes.NewReader([]byte("data"))    // Создает Reader из []byte
r.Read(b)                              // Читает байты в указанный буфер

bytes.Count([]byte("cheese"), []byte("e")) // 3 (количество вхождений)
bytes.Repeat([]byte("a"), 3)             // []byte("aaa") (повтор N раз)
bytes.Compare([]byte("a"), []byte("b"))  // -1 (сравнение)
```

## time
Работа с датами, временем и таймерами.
```go
now := time.Now()                                   // Текущее время
t := time.Date(2023, 5, 10, 15, 30, 0, 0, time.UTC) // Создание конкретной даты
t := time.Unix(1678901234, 0)                       // Время из Unix timestamp

s := now.Format("2006-01-02 15:04:05")         // Форматирование в строку (стандартный layout)
t, _ := time.Parse("2006-01-02", "2023-05-10") // Парсинг строки во время

t1 := t.Add(24 * time.Hour)             // Добавить 24 часа
t2 := t.AddDate(0, 1, 0)                // Добавить 1 месяц
dur := t1.Sub(t2)                       // Разница между временем (Duration)

time.Sleep(2 * time.Second)               // Блокировка на 2 секунды
timer := time.NewTimer(3 * time.Second)   // Таймер на 3 секунды
ticker := time.NewTicker(1 * time.Second) // Тикер каждую секунду

d := time.Hour * 2                      // 2 часа как Duration
sec := d.Seconds()                      // Конвертация в секунды (float64)
ms := d.Milliseconds()                  // Конвертация в миллисекунды

now.Before(t)                           // true если now раньше t
now.After(t)                            // true если now позже t
now.Equal(t)                            // true если времена равны

loc, _ := time.LoadLocation("America/New_York") // Загрузка локации
t.In(loc)                                       // Конвертация времени в другой пояс
time.UTC                                        // UTC временная зона

time.Nanosecond                        // Константа наносекунды
time.RFC3339                           // Стандартный формат "2006-01-02T15:04:05Z07:00"

time.Since(t)                          // Прошедшее время с момента t
time.Until(t)                          // Оставшееся время до момента t
```

## reflect
```go
t := reflect.TypeOf(42)                // Возвращает тип значения (reflect.Type)
v := reflect.ValueOf("hello")          // Возвращает reflect.Value объекта
kind := v.Kind()                       // Возвращает базовый тип (int, string, struct и т.д.)

numFields := t.NumField()              // Количество полей структуры
field := t.Field(0)                    // Получает i-ое поле структуры
tag := field.Tag.Get("json")            // Получает тег поля (например, `json:"name"`)

x := v.Interface()                     // Преобразует Value обратно в interface{}
v.SetInt(42)                           // Устанавливает значение (должно быть addressable)
v.Elem()                               // Разыменовывает указатель (для изменения значений)

newV := reflect.New(t)                 // Создает новый объект того же типа
slice := reflect.MakeSlice(reflect.TypeOf([]int{}), 0, 10) // Создает слайс

fnValue := reflect.ValueOf(fmt.Println) // Получает reflect.Value функции
args := []reflect.Value{reflect.ValueOf("test")}
fnValue.Call(args)                     // Динамический вызов функции

v.IsNil()                              // Проверяет на nil (для указателей, каналов и т.д.)
v.CanSet()                             // Можно ли изменить значение
v.IsValid()                            // Является ли Value валидной

m := reflect.MakeMap(reflect.MapOf(keyType, valType)) // Создание map
m.SetMapIndex(keyVal, valVal)           // Добавление элемента в map
```

## sort
Сортировка слайсов и пользовательских коллекций.
```go
sort.Ints([]int{3, 1, 2})             // Сортировка []int → [1 2 3]
sort.Float64s([]float64{3.2, 1.5})    // Сортировка []float64 → [1.5 3.2]
sort.Strings([]string{"c", "a"})      // Сортировка []string → ["a" "c"]

sort.IntsAreSorted([]int{1, 2})       // true если слайс уже отсортирован
sort.Sort(sort.Reverse(people))       // Сортировка в обратном порядке

sort.Slice(people, func(i, j int) bool { return people[i].Age < people[j].Age })     // Сортировка по полю структуры
sort.SliceStable(people, func(i, j) bool { return people[i].Name < people[j].Name }) // Стабильная сортировка (сохраняет порядок равных элементов)

idx := sort.SearchInts([]int{1, 2, 3}, 2)                         // Бинарный поиск → 1 (индекс элемента)
sort.Search(len(data), func(i int) bool { return data[i] >= 42 }) // Кастомный бинарный поиск

// Сортировка по интерфейсу
type People []struct{Name string; Age int}
func (p People) Len() int { return len(p) } // Требуется для sort.Interface
func (p People) Less(i, j int) bool { return p[i].Age < p[j].Age } // Определяет порядок
func (p People) Swap(i, j int) { p[i], p[j] = p[j], p[i] } // Меняет элементы местами
sort.Sort(people)
```
