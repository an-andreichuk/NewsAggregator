# NewsAggregator
База данных: MongoDB Atlas, бесплатная версия, так что лимит --- 512 мб. NoSQL.
Основной проект на ASP.NET Core (C#, MVC). Из базы данных берется информация, анализируется и отправляется пользователю.

## 1.   База данных.
**Доступ:**
* Read only: `mongodb+srv://reader:reader-pass-123@cluster0-kgt9l.azure.mongodb.net/test?retryWrites=true&w=majority`
* Read & Write: `mongodb+srv://writer:writer-pass-123@cluster0-kgt9l.azure.mongodb.net/test?retryWrites=true&w=majority`

**Название БД:** `News`
Название каждой коллекции соответствует названию (домену) какого-то новостного сайта (например, [pravda.com.ua](pravda.com.ua), [tsn.ua](tsn.ua)).

**BSON:**

    {
        "_id": ObjectId,
        "Title": "string",
        "Text": "string",
        "Tags": [
            "string"
        ],
        "SourceUrl": "string",
        "TimeSourcePublished": BsonDate,
        "EnglishText": "string",
        "KeyWords": [
            "string"
        ],
        "Duplicates": [
            "string"
        ]
    }

Возможно, будет расширяться/изменяться ещё.

`KeyWords`, `Duplicates` --- заполняются только после анализа (если вообще заполняются :) ). В `KeyWords` хранятся ключи текста, в `Duplicates` --- дублирующие новости; всё остальное понятно.

## Парсинг
Основной код каждые 60 минут вызывает скрипт. Скрипт делает парсинг сайтов при запуске, и заносит информацию в БД, каждый сайт в соответствующую коллекцию, по формату выше. Очевидно, если новость уже есть в коллекции, её не добавлять (сравнивать по url например, как минимум).

## Фронтенд
Надо сделать что-то красивенькое из имеющихся данных :)

## Бэкенд
В [`NewsHelper.cs`][NewsHelper.cs] есть заглушка для анализа.  

Планы:
1.  выделять из текста новости ключевые слова  
2.  сравнивая ключевые слова, находить дубликаты в других коллекциях  
3.  ...


[NewsHelper.cs]: https://github.com/an-andreichuk/NewsAggregator/blob/master/NewsAggregator/Models/NewsHelper.cs
