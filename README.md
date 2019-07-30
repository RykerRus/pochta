# pochta
----------
Получение письма
```
from pochta import User
with User("al") as user:
    text = user.get_mail()[0].text
```

Отправка
```
from pochta import User
with User("al") as user:
    user.new_mail({"text": "Test", "tittle": "Заголовок"})
    user.mail.add_file("conftest.py")
    user.send("al8594212@gmail.com") # Или user.send(["al8594212@gmail.com", "al8594212@gmail.com"])
```
