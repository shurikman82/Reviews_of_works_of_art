# reviews_of_works_of_art

Урезаная версия блоггинг-сервиса с добавленным интерфейсом API. Документация представлена в формате Redoc.

Сервис предоставляет возможность делиться своими отзывами на различные произведения музыки, кинематографа, литературы с другими людьми и ставить им заслуженную оценку, а они, в свою очередь, имеют возможность восхититься (или наоборот) вашими соображениями!
## Запуск проекта
Склонируйте репозиторий:
```bash
git clone https://github.com/shurikman82/Reviews_of_work_of_art.git
```
Установите и активируйте виртуальное окружение:
```bash
python3 -m venv venv
```
```bash
python3 source venv/bin/activate
```
Установите зависимости в окружение и сделайте миграции:
```bash
pip install -r requirements.txt
```
```bash
cd api_yamdb
```
```bash
python3 manage.py migrate
```
Создайте суперпользователя:
```bash
python3 manage.py createsuperuser
```
Запустите проект:
```bash
python3 manage.py runserver
```
Когда вы запустите проект, по адресу  http://127.0.0.1:8000/redoc/ будет доступна документация для API.

## Авторы:

Александр Русанов, shurik.82rusanov@yandex.ru,<br>
Дарья Линецкая,<br>
Григорий Землянский
