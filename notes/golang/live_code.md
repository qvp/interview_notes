# Live Codding

## Развернуть порядок элементов массива
```go
a := [...]int{1, 3, 5}

for i, j := 0, len(a)-1; i < j; i, j = i+1, j-1 {
    a[i], a[j] = a[j], a[i]
}
```

## Удаление из середины среза без изменения левой части
Оператор `[start:stop]` создает новый срез, по умолчанию `[0:len]`.  
```go
copy(s[i:], s[i+1:])
```

## Возвести элементы в квадрат
Исходный список отсортирован. Требуемая сложность О(n).
```go
// Алгоритм "два указателя" Two Pointers
func sortedSquares(nums []int) []int {
	n := len(nums)
	result := make([]int, n)
	left, right := 0, n-1

	for i := n - 1; i >= 0; i-- {
		if abs(nums[left]) > abs(nums[right]) {
			result[i] = nums[left] * nums[left]
			left++
		} else {
			result[i] = nums[right] * nums[right]
			right--
		}
	}
	return result
}

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}
```

## Минимальное количество комнат
Есть журнал заселения отеля, в которых есть пары чисел - дата заселения и дата выселения,
например [[1, 2], [4, 10], [3, 7]], надо узнать сколько комнат надо
```go
func minRooms(bookings [][]int) int {
	n := len(bookings)
	if n == 0 {
		return 0
	}

	checkIns := make([]int, n)
	checkOuts := make([]int, n)

	for i, booking := range bookings {
		checkIns[i] = booking[0]
		checkOuts[i] = booking[1]
	}

	sort.Ints(checkIns)
	sort.Ints(checkOuts)

	rooms, maxRooms := 0, 0
	i, j := 0, 0

	for i < n {
		if checkIns[i] < checkOuts[j] {
			rooms++
			if rooms > maxRooms {
				maxRooms = rooms
			}
			i++
		} else {
			rooms--
			j++
		}
	}

	return maxRooms
}
```

## Функция котора объединяет данные из нескольких каналов
```go
func mergeChannels(channels ...<-chan int) <-chan int {
    merged := make(chan int)

    // Для каждого канала запускаем горутину, которая читает данные и отправляет в merged
    for _, ch := range channels {
        go func(c <-chan int) {
            for v := range c {
                merged <- v
            }
        }(ch)
    }

    // Закрываем merged, когда все исходные каналы закрыты
    go func() {
        wg := sync.WaitGroup{}
        wg.Add(len(channels))
        
        for _, ch := range channels {
            go func(c <-chan int) {
                defer wg.Done()
                for range c {} // Читаем до закрытия канала
            }(ch)
        }
        
        wg.Wait()
        close(merged)
    }()

    return merged
}
```

## ТЗ таск менеджер
простое, но расширяемое решение для управления долгими I/O bound задачами с HTTP API. Решение будет хранить все данные в памяти. Учесть расширяемость.

## Что выведет данный код
```go
a1 := make([]int, 10)
a1 = append(a1, []int{1, 2, 3, 4, 5}...)
a2 := append(a1, 6)
a3 := append(a1, 7)
fmt.Println(a1, a2, a3) // [1 2 3 4 5] [1 2 3 4 5 7] [1 2 3 4 5 7]
```
Все три среза (a1, a2, a3) используют один и тот же базовый массив (так как ёмкость исходного среза была достаточна для всех операций append).  
`a2 := append(a1, 6)` - добавление элемента 6 в массив на позицию с индексом 5 (так как длина a1 была 5)/ Создание нового среза a2 с длиной 6.  
`a3 := append(a1, 7)` - a1 всё ещё имеет длину 5, Элемент 7 записывается на ту же позицию с индексом 5 в базовом массиве, перезаписывая 6.  

Чтобы избежать такого поведения, нужно либо создавать копии срезов перед append, либо использовать append по-другому, например:  
```go
a2 := append(append([]int{}, a1...), 6)
a3 := append(append([]int{}, a1...), 7)
```

## Верни ошибку без использования сторонних пакетов
Если метод интерфейса реализован для указателя (*T), то только указатель удовлетворяет интерфейсу. Если он реализован для значения (T), то и значение, и указатель будут работать.
```go
func handle() error {
	return &myError{"text here"}
}

type myError struct {
	text string
}

func (m *myError) Error() string {
	return m.text
}
```
```go
func handle() error {
	return myError{"text here"} // &myError{"text here"} тоже сработает
}

type myError struct {
	text string
}

func (m myError) Error() string {
	return m.text
}
```
Оба варианта рабочие, выбор зависит от того, хотите ли вы, чтобы myError был изменяемым (используйте указатель) или неизменяемым (используйте значение).

## Что выведет данный код и почему
```go
f := []int{1, 2, 3}
	s := make([]*int, len(f))
	for i, v := range f {
		s[i] = &v
	}
	fmt.Println(*s[0], *s[1]) // 1 2
```
Начиная с версии го 1.22 переменная в цикле каждый раз создается новая, поэтому код работает корректно, но все же лучше написать `s[i] = &f[i]`.

## Вызов функции с таймаутом
```go
func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()

	data, err := loadDataWithContext(ctx)
	if err != nil {
		fmt.Println("Error", err)
	} else {
		fmt.Println(data)
	}
}

func loadData() int {
	time.Sleep(1 * time.Second)
	return 1
}

func loadDataWithContext(ctx context.Context) (int, error) {
	resCh := make(chan int, 1)

	go func() {
		resCh <- loadData()
	}()

	select {
	case res := <-resCh:
		return res, nil
	case <-ctx.Done():
		return 0, errors.New("timeout")
	}
}
```

## Что выведет данный код
Слайсы передаются по значению, но они содержат указатель на массив
```go
func foo(src []int) {
	src = append(src, 5)
}

arr := []int{1, 2, 3}
src := arr[:1]
foo(src)

fmt.Println(src) // [1]
fmt.Println(arr) // [1 5 3]
```
Чтобы изменить исходный слайс нужно передать ссылку на него:
```go
func foo(src *[]int) {
	*src = append(*src, 5)
	fmt.Println(src) // &[1 5]
}

arr := []int{1, 2, 3}
src := arr[:1]
foo(&src)

fmt.Println(&src) // &[1 5]
fmt.Println(src) // [1 5]
fmt.Println(arr) // [1 5 3]
```

## Ограничение одновременно запускаемых горутин
С пулом горутин и семафором

## Как отменить группу горутин при ошибке в одной из них ???

## отличие var wg sync.WaitGroup vs wg := &sync.WaitGroup{} ???

## Что выведет данный код
Код поработает некоторое время пока го не заметит конкурентную работу с картой и не прервет программу с ошибкой: `fatal error: concurrent map read and map write`.
```go
var m = map[string]int{"a": 1}

func main() {
	go read()
	time.Sleep(time.Second)
	go write()
	time.Sleep(time.Second)
}

func read() {
	for {
		fmt.Println(m["a"])
	}
}

func write() {
	for {
		m["a"] = 2
	}
}
```

## Что выведет данный код
Будет ошибка `panic: send on closed channel`.  
Так как канал не буферизированный, то горутина будет заблокирована пока ничкто не читает из канала, а когда попробует записать, то канал будет уже закрыт.  
Чтобы ее исправить нужно закрыть канал внутри горутины или сделать его буферизированным.
```go
c := make(chan int)
go func() {
    c <- 1
}()

time.Sleep(time.Millisecond * 500)
close(c)

for v := range c {
    fmt.Println(v)
}

time.Sleep(time.Millisecond * 100)
```

## Бинарный поиск
```go
func BinarySearch(in []int, searchFor int) (int, bool) {
  if len(in) == 0 {
    return 0, false
  }

  var first, last = 0, len(in) - 1

  for first <= last {
    var mid = ((last - first) / 2) + first

    if in[mid] == searchFor {
      return mid, true
    } else if in[mid] > searchFor { // нужно искать в "левой" части слайса
      last = mid - 1
    } else if in[mid] < searchFor { // нужно искать в "правой" части слайса
      first = mid + 1
    }
  }

  return 0, false
}
```

## Что выведет данный код
Так как у слайса `test1` `cap=5` то `test1[3:]` не вызовет паники
```go
test1 := []int{1, 2, 3, 4, 5}  // len=5, cap=5
test1 = test1[:3]               // len=3, cap=5
test2 := test1[3:]              // len=2, cap=2
fmt.Println(test2[:2])          // [4, 5]
```

## Fibonacci
https://uproger.com/go-100-voprosov-zadanij-s-sobesedovanij-podgotovka-k-sobesedovaniyu-golang/#38
