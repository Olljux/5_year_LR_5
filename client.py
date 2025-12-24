import grpc
import glossary_pb2
import glossary_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
stub = glossary_pb2_grpc.GlossaryStub(channel)

# Добавляем термин
response = stub.AddTerm(glossary_pb2.TermReply(term="Python", description="Язык программирования"))
print(response)

response = stub.AddTerm(glossary_pb2.TermReply(term="FastAPI", description="Современный веб-фреймворк для создания API с автоматической генерацией документации."))
print(response)

response = stub.AddTerm(glossary_pb2.TermReply(term="Pydantic", description="Библиотека для валидации данных и управления настройками с использованием аннотаций типов Python."))
print(response)

response = stub.AddTerm(glossary_pb2.TermReply(term="SQLite", description="Встраиваемая реляционная база данных, хранящая всю базу в одном файле."))
print(response)

response = stub.AddTerm(glossary_pb2.TermReply(term="Swagger UI", description="Инструмент визуализации OpenAPI-спецификации, предоставляющий интерактивную документацию API."))
print(response)

response = stub.AddTerm(glossary_pb2.TermReply(term="Docker", description="Платформа для контейнеризации приложений, позволяющая упаковать приложение и его зависимости в изолированную среду."))
print(response)



# Получаем термин
response = stub.GetTerm(glossary_pb2.TermRequest(term="SQLite"))
print(response)

# Обновляем описание
response = stub.UpdateTerm(glossary_pb2.TermReply(term="Python", description="Популярный язык программирования"))
print(response)

# Удаляем термин
response = stub.DeleteTerm(glossary_pb2.TermRequest(term="Docker"))
print(response)