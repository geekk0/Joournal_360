## Journal 360                  
[switch to Rus](README.rus.md)

![python version](https://img.shields.io/badge/python-3.9.5-brightgreen)
![languages](https://img.shields.io/github/languages/top/geekk0/Journal_360)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/3cc6c94a88dd41be9b84faf38e378752)](https://www.codacy.com/gh/geekk0/Golden_League_site/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=geekk0/BRIO_assistant&amp;utm_campaign=Badge_Grade)
![last-commit](https://img.shields.io/github/last-commit/geekk0/Journal_360)

<br>Online journal to communicate information between shifts.

## Live demo
https://www.journaldemo.tk

account for "engineer" department: 
<br>login: a.andreev
<br>password: 1234567Qe

account for "engineer" department: 
<br>login: d.dmitriev
<br>password: 1234567Qe

account for Administrator: 
<br>login: Administrator
<br>password: 1234567Qe


## Description
The site allows you to compile and publish reports in an automated mode.   
<br>At the moment it is configured for use by two departments "Engineers" and "IT", in each department there are 4 groups (shifts).
<br>The Administrators group has access to both departments.
<br>For the "Engineers" department, the reporting system works as follows:
<br>- During the day, the shift draws up a report, which is published at 9.10 the next day and becomes visible to the department.
<br>- Until the evening, the published report is available for editing, the created record is updated every 20 minutes.
<br>- At 11.00, the report is sent to the mail, as well as to the Telegram bot.
<br>For the "IT" department, the report is sent manually, with an attached distribution by mail.

## Features
 
- Formation of reports using downloadable images and "tags" - presets for typical situations.- Публикация и изменение статуса отчетов, настроенные под текущее расписание работы.
- Search by department, author, date and report text.
- Sending reports to mail and Telegram-bot by "subscription" using Django REST framework.- Разовые и регулярные задания с различным периодом.
- Comments for reports and assignments.
- Section with downloadable schemes, documents and manuals.
- Equipment location recording section
- The Production version uses LDAP server authorization.
- PostgreSQL database.
- Adapted for mobile devices.



## Libs

Django, Django REST Framework.
<br>django-apscheduler, psycopg2, ldap3, Request, Messages, Pillow, json, smtplib, logging, MIMEMultipart, io,
itertools, api.serializer, environ.
