# pochta
----------
Получение письма
```
from pochta import User
with User("al") as user:
    for mail in user.get_mail():
    text = mail.text
```

Отправка
```
from pochta import User
with User("al") as user:
    user.new_mail({"text": "Test", "tittle": "Заголовок"})
    user.mail.add_file("conftest.py")
    user.send("al8594212@gmail.com") # Или user.send(["al8594212@gmail.com", "al8594212@gmail.com"])
```
