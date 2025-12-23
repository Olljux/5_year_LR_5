# Glossary gRPC Service
Глоссарий терминов с доступом через gRPC и Protocol Buffers.

## Описание
Сервис хранит термины и их описания. Позволяет:
- Добавлять новые термины
- Получать термин по имени
- Изменять описание термина
- Удалять термин

Сервис реализован на Python, использует gRPC и SQLite.

## Установка и запуск

1. Клонировать репозиторий:
```bash
git clone https://github.com/Olljux/5_year_LR_5.git
cd prog5_LR_5
```
2. Собрать Docker образ:
```
docker build -t grpc-glossary .
```
3. Запустить контейнер (пример с портом 50052):
```
docker run -p 50052:50051 grpc-glossary
```
Теперь сервис доступен на порту 50052.

---

## Использование клиента


Пример работы с сервисом:
```python
import grpc
import glossary_pb2
import glossary_pb2_grpc

channel = grpc.insecure_channel('localhost:50052')
stub = glossary_pb2_grpc.GlossaryStub(channel)

# Получение термина
response = stub.GetTerm(glossary_pb2.TermRequest(term="Python"))
print(response)

# Добавление нового термина
response = stub.AddTerm(glossary_pb2.TermReply(term="gRPC", description="Протокол удалённых вызовов"))
print(response)
```
Примечание: при попытке добавить существующий термин, будет ошибка ALREADY_EXISTS.

## Зависимости
- Python 3.11
- grpcio
- grpcio-tools
- sqlite3 (входит в стандартную библиотеку Python)