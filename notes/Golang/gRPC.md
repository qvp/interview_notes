# gRPC

## Что такое gRPC
<!-- middle 3525480 -->
Это современный фреймворк для удалённого вызова процедур (RPC), разработанный Google. Он использует:
* **HTTP/2** – для быстрой передачи данных с мультиплексированием.
* **Protocol Buffers (protobuf)** – бинарный формат для описания API и сериализации данных.
* **Автогенерацию кода** – из .proto файлов генерируются клиент и сервер.

## Преимущества перед REST
<!-- middle 3525480 -->
* Высокая скорость (бинарный protobuf + HTTP/2).
* Строгая типизация (все методы и модели описаны в .proto).
* Поддержка стриминга (можно передавать поток данных).
* Кросс-языковая совместимость (клиент и сервер могут быть на разных языках).

## Protocol Buffers (protobuf)
<!-- middle 3525480 -->
Protobuf не сохраняет имена полей в бинарном формате – вместо этого используются номера полей. Это делает данные компактнее и быстрее для обработки.
```protobuf
// Указываем версию синтаксиса (proto3 рекомендуется)
syntax = "proto3";

// Импорт других .proto файлов (например, стандартных типов Google)
import "google/protobuf/timestamp.proto";

// Опционально: задаём пространство имён для генерации кода
package example.advanced;

// Можно определить перечисление (enum)
enum UserRole {
  // Варианты enum должны начинаться с 0
  ROLE_UNSPECIFIED = 0;  // Значение по умолчанию
  ROLE_USER = 1;
  ROLE_ADMIN = 2;
  ROLE_MODERATOR = 3;
}

// Сообщение (аналог структуры/класса)
message User {
  // Поля имеют уникальные числовые теги (1, 2, ...)
  string id = 1;                  // Строка
  string username = 2;            // Обязательное поле (по умолчанию)
  optional string email = 3;      // Опциональное поле (может быть null)
  int32 age = 4;                  // 32-битное целое
  UserRole role = 5;              // Используем enum
  repeated string permissions = 6; // Массив строк (может быть пустым)
  google.protobuf.Timestamp created_at = 7; // Используем импортированный тип
  map<string, string> metadata = 8; // Ассоциативный массив (ключ-значение)
}

// Сообщение для запроса
message GetUserRequest {
  string user_id = 1;
}

// Сообщение для ответа
message GetUserResponse {
  User user = 1;
}

// Сообщение для стриминга
message ChatMessage {
  string sender = 1;
  string text = 2;
}

// Определяем gRPC-сервис
service UserService {
  // Простой запрос-ответ (Unary RPC)
  rpc GetUser (GetUserRequest) returns (GetUserResponse);

  // Стриминг от сервера (Server Streaming)
  rpc SubscribeToNotifications (GetUserRequest) returns (stream ChatMessage);

  // Стриминг от клиента (Client Streaming)
  rpc UploadUserDocuments (stream ChatMessage) returns (GetUserResponse);

  // Двунаправленный стриминг (Bidirectional Streaming)
  rpc Chat (stream ChatMessage) returns (stream ChatMessage);
}

// Опциональные настройки (например, для оптимизации)
option go_package = "github.com/example/advanced/proto"; // Для Go
option java_multiple_files = true;                      // Для Java
```  

## Типы gRPC-вызовов
<!-- middle 3525480 -->
| Тип | Описание | Пример использования |  
|-----|----------|----------------------|  
| **Unary** | Запрос → Ответ | Получение пользователя по ID |  
| **Server Streaming** | Запрос → Поток ответов | Лента новостей, live-данные |  
| **Client Streaming** | Поток запросов → Ответ | Загрузка файла |  
| **Bidirectional Streaming** | Двунаправленный поток | Чат, онлайн-игры |

https://realpython.com/python-microservices-grpc/#performance

## Websockets
<!-- middle 3525480 -->

## Sockets
<!-- middle 3525480 -->
