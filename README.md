## Проект "bbjob_ready" - инновационное решение для прогнозирования увольнения сотрудников. Этот проект объединяет в себе веб-приложение (backend и frontend), модель машинного обучения и Telegram бота для удобного мониторинга.
## Установка
Установите Docker на свой компьютер. Инструкции по установке Docker.

Склонируйте репозиторий проекта:

```bash
git clone https://github.com/alotzte/bbjob_ready.git
cd bbjob_ready
```
Постройте Docker образы:



```
docker-compose build
```
Запуск
Запустите приложение с помощью Docker Compose:

```
docker-compose up
```
Дополнительные шаги (по необходимости)
В некоторых случаях может потребоваться выполнить дополнительные шаги:

```
# Сборка основного сервиса
cd /root/bbjob_ready && docker build -t bbjob_serv:0.0.1 .

# Сборка Telegram бота
cd /root/bbjob_ready/app/telegram_bot && docker build -t bbjob_bot:0.0.1 -f Dockerfile_bot .

# Сборка уведомителя о пользователях
cd /root/bbjob_ready/app/telegram_bot && docker build -t bbjob_un:0.0.1 -f Dockerfile_user_notifier .
```
Эти шаги могут понадобиться в случае возникновения проблем или специфических требований.
 

Важно 
Убедитесь, что все необходимые зависимости установлены, и порты, используемые приложением, доступны.

Приложение теперь должно быть доступно по указанному адресу. Проверьте логи контейнеров, чтобы убедиться, что все успешно запущено.

## Инструкция для пользователя
Добро пожаловать в систему прогнозирования увольнения сотрудников. 

Вход в систему
Откройте веб-браузер и перейдите по адресу[http://178.170.192.197:8000/auth/].

Введите следующие учетные данные:
```
Логин: test
Пароль: test
```
Нажмите кнопку "Войти".

### Главная страница
После успешного входа вы окажетесь на главной странице системы. Здесь представлена информация о сотрудниках из отдела номер 1, так как вы вошли под учетной записью тестового аккаунта, который принадлежит данному отделу.

На главной странице вы увидите следующую информацию:


* Список сотрудников отдела 1: Перечислены имена работников, находящихся в отделе номер 1.

* Вероятность увольнения в процентах: Рядом с именем каждого сотрудника указана вероятность их увольнения в процентах.
* Подробная информация


Чтобы получить дополнительные детали о сотруднике, выполните следующие шаги:

* На главной странице найдите сотрудника, о котором вы хотели бы получить подробную информацию.

* Нажмите кнопку "Подробнее" рядом с именем выбранного сотрудника.

* После нажатия на кнопку "Подробнее" вы перейдете на страницу с интерактивным графиком, отображающим дополнительные характеристики выбранного сотрудника. Здесь вы сможете более подробно изучить информацию и прогнозы.

### Загрузка данных
Чтобы обновить данные в системе с использованием нового файла, выполните следующие шаги:

1) На главной странице системы найдите раздел для загрузки данных.

2) Нажмите кнопку "Выбрать файл" и выберите файл test_data_server.csv на вашем компьютере.

3) Нажмите кнопку "Загрузить". Система автоматически добавит данные из файла в базу данных, пересчитает вероятности увольнения и отобразит обновленную информацию на экране.

### Экспорт данных
Чтобы сохранить текущие данные системы в формате CSV, выполните следующие шаги:

1) На главной странице системы найдите раздел для экспорта данных.

2) Нажмите кнопку "Скачать CSV".

3) Выберите путь сохранения файла на вашем компьютере.

4) Нажмите "Сохранить". Файл с данными будет загружен на ваш компьютер.

Благодарим за использование "BBJOB_READY"! Если у вас возникнут вопросы или у вас есть предложения по улучшению системы, пожалуйста, обратитесь к администратору системы.