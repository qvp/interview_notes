# Errors

## Примеры работы с ошибками
<!-- junior 3525480 -->
`panic` только для ситуаций, когда программа действительно не может продолжать работу, и эта ситуация является неожиданной и невосстановимой. Во всех остальных случаях возвращайте ошибки.

```go
errors.New("описание ошибки") // Создание ошибки
fmt.Errorf("ошибка при обработке %s: %v", input, err) // Форматированные ошибки

// Кастомные типы ошибок (для более сложной обработки)
type MyError struct {
Code    int
Message string
}

func (e *MyError) Error() string {
return fmt.Sprintf("Код %d: %s", e.Code, e.Message)
}

// Использование
return &MyError{Code: 404, Message: "Не найдено"}

// Проверка типов ошибок
var myErr *MyError
if errors.As(err, &myErr) {
    // Обработка конкретного типа ошибки
    fmt.Println("Код ошибки:", myErr.Code)
}
```

## Recover \ panic
<!-- junior 3525480 -->
Функция которую можно вызвать, как исключение, и тогда функция recover() вернет ошибку.
```go
func x() (res int, err error) {
	defer func() {
		if p := recover(); p != nil {
			err = fmt.Errorf("ERR %v", p)
		}
	}()

	panic("la la la")
	return
}
```
1. recover работает только внутри отложенных функций (defer)
2. recover перехватывает только паники, возникшие в той же goroutine
3. Не следует злоупотреблять recover - это не замена обычной обработке ошибок
4. После recover выполнение продолжается с места после паники, а не с места где она возникла

Лучшая практика - использовать recover только для:
1. Логирования критических ошибок
2. Очистки ресурсов
3. Предотвращения падения сервиса в критически важных местах

## Middleware восстановления (для веб-серверов):
<!-- junior 3525480 -->
```go
func recoveryMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        defer func() {
            if err := recover(); err != nil {
                w.WriteHeader(http.StatusInternalServerError)
                log.Printf("panic: %v", err)
            }
        }()
        next.ServeHTTP(w, r)
    })
}
```

## fmt.Errorf
<!-- junior 3525480 -->
Функция fmt.Errorf в Go используется для создания форматированных ошибок. Она работает аналогично fmt.Printf, но вместо вывода текста возвращает ошибку.  
Начиная с Go 1.13, fmt.Errorf получил специальный глагол %w, который позволяет оборачивать ошибки, сохраняя исходную ошибку для последующего анализа.  
Без %w (простая форматированная ошибка).  
```go
var ErrBase = errors.New("base error")
err := fmt.Errorf("дополнительный контекст: %w", ErrBase)
errors.Is(err, ErrBase) // true
```

При использовании %w Go создаёт структуру, реализующую интерфейс:
```go
type wrapError struct {
    msg string
    err error
}

func (e *wrapError) Error() string {
    return e.msg
}

func (e *wrapError) Unwrap() error {
    return e.err
}
```

## Стек вызова функций
<!-- junior 3525480 -->
Не логируйте стек для всех ошибок - только для важных или неожиданных.  
```go
log.Printf("Error: %v\nStack trace:\n%s", err, debug.Stack()) // import runtime/debug
log.Printf("%+v", errors.Wrap(err, "process failed")) // import github.com/pkg/errors
```
