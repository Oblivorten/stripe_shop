# Stripe Shop 🛒

Django-приложение с интеграцией Stripe API для демонстрации покупки товаров через Checkout Session.  

---

## 🔧 Стек технологий

- Python 3.11.3
- Django 5.2.4
- Stripe API (`stripe==12.3.0`)
- PostgreSQL 17
- Docker + Docker Compose
- Gunicorn + Whitenoise
- HTML + JavaScript (Stripe.js)
- Переменные окружения через `python-decouple`

---

## 🚀 Демо

Приложение задеплоено и доступно по адресу:  
🔗 **[https://stripe-shop-kket.onrender.com](https://stripe-shop-kket.onrender.com)**

Доступ к админке:  
`/admin/`  
**Логин:** `Admin`  
**Пароль:** `stripetest`

---

## 📦 Установка и запуск

### Вариант 1: Через Docker 

```bash
git clone https://github.com/Oblivorten/stripe_shop.git
cd stripe_shop

docker-compose up --build
```
### Вариант 2: Ручной запуск

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
## Настроить .env файл:

```
SECRET_KEY=your_secret
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=your_db
DB_USER=your_user
DB_PASSWORD=your_password
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLIC_KEY=pk_test_...
```
## Запустить сервер:
```
python manage.py migrate
python manage.py runserver
```

### 🧩 Основной функционал

## Эндпоинты:
`GET /item/<id> — простая HTML-страница с информацией о товаре и кнопкой "Buy"`

`GET /buy/<id> — создаёт Stripe Checkout Session и возвращает session_id`

`JS скрипт на клиенте делает редирект через stripe.redirectToCheckout(sessionId=...)`

### 💡 Дополнительный функционал:

- Использование Docker

- Поддержка .env и python-decouple

- Просмотр моделей через Django Admin

- Развёртывание на сервере (Render)

- Поддержка разных валют (рубли, доллары, евро)

### ⚙️ Модели
**Item — товар**

**Order — заказ, объединяющий несколько товаров**

**Discount — скидка в %**

**Tax — налог в %**
