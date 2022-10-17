## Journal 360                  
[switch to Eng](README.md)

![python version](https://img.shields.io/badge/python-3.9.5-brightgreen)
![languages](https://img.shields.io/github/languages/top/geekk0/Journal_360)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/3cc6c94a88dd41be9b84faf38e378752)](https://www.codacy.com/gh/geekk0/Golden_League_site/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=geekk0/BRIO_assistant&amp;utm_campaign=Badge_Grade)
![last-commit](https://img.shields.io/github/last-commit/geekk0/Journal_360)

<br>Онлайн журнал для передачи информации между сменами.

## Live demo
https://www.journaldemo.tk

Учетная запись для отдела инженеров: 
<br>login: a.andreev
<br>password: 1234567Qe

Учетная запись для отдела IT: 
<br>login: d.dmitriev
<br>password: 1234567Qe

Учетная запись для Администратора: 
<br>login: Administrator
<br>password: 1234567Qe


## Описание
Сайт позволяет составлять и публиковать отчеты в автоматизированном режиме.   
<br>В данный момент он настроен для испльзования двумя подразделениями "Инженеры" и "IT", в каждом отделе по 4 группы (смены).
<br>Группа "Администраторы" имеет доступ к обоим отделам.
<br>Для отдела "Инженеры" система отчетов работает следующим образом:
<br>- В течение суток смена составляет отчет, который в 9.10 следующего дня публикуется и становится виден отделу.
<br>- До вечера опубликованный отчет доступен для редактирования, созданная запись обновляется каждые 20 минут.
<br>- В 11.00 происходит рассылка отчета на почту, а также в Telegram-бот.
<br>Для отдела "IT" отправка отчета происходит вручную, с привязанной рассылкой по почте.

## Особенности
 
- Формирование отчетов с использованием загружаемых изображений и "тегов" - пресетов для типовых ситуаций.
- Публикация и изменение статуса отчетов, настроенные под текущее расписание работы.
- Поиск по отделу, автору, дате и тексту отчета.
- Отправка отчетов на почту и в Telegram-bot по "подписке", используя Django REST framework.
- Разовые и регулярные задания с различным периодом.
- Комментарии для отчетов и заданий.
- Секция со скачиваемыми схемами, документами и мануалами.
- Секция учета местонахождения оборудования
- В Production-версии используется авторизация LDAP сервера.
- Postgres база данных.
- Адаптирован для мобильных устройств.



## Библиотеки и технологии

Django, Django REST Framework.
<br>django-apscheduler, psycopg2, ldap3, Request, Messages, Pillow, json, smtplib, logging, MIMEMultipart, io,
itertools, api.serializer, environ.
