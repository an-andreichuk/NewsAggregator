# NewsAggregator

Clone repository and add dependencies:
MongoDB.Driver -Version 2.10.0
HangFire.Core -Version 1.7.7

База данных: MongoDB Atlas, бесплатная версия, так что лимит - 512 мб. NoSQL.
Основной проект на ASP.NET Core (C#, MVC). Из базы данных берется информация, анализируется и отправляется пользователю.

1. База данных.
Доступ:
Read only:      mongodb+srv://reader:reader-pass-123@cluster0-kgt9l.azure.mongodb.net/test?retryWrites=true&w=majority
Read & Write:   mongodb+srv://writer:writer-pass-123@cluster0-kgt9l.azure.mongodb.net/test?retryWrites=true&w=majority

Название БД: News
Название каждой коллекции соответствует названию (домену) какого-то новостного сайта (например, pravda.com.ua, tsn.ua).
BSON:
{
"_id": ObjectId
"Title": "string",
"Text": "string",
"SourceUrl": "string",
"TimeSourcePublished": BsonDate,
"KeyWords": [
    "string"
],
"Duplicates": [
    "string"
]
}

Возможно, будет расширяться/изменяться ещё.
KeyWords, Duplicates -- заполняются только после анализа (если вообще заполняются :) ). В KeyWords хранятся ключи текста, в Duplicates -- дублирующие новости; всё остальное понятно.

2. Парсинг
Основной код каждые t минут вызывает скрипт (ещё не реализовано). Скрипт (его тоже ещё нет) делает парсинг сайтов при запуске, и заносит информацию в БД, каждый сайт в соответствующую коллекцию, по формату выше.
Очевидно, если новость уже ест в коллекции, её не добавлять (сравнивать по url например, как минимум).

3. Фронтенд
Надо сделать что-то красивенькое из имеющихся данных :)

4. Бэкенд
В NewsRepository.cs есть заглушка для анализа.
Планы:
а) выделять из текста новости ключевые слова
б) сравнивая ключевые слова, находить дубликаты в других коллекциях
в) ...
