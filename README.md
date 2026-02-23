# 🛒 DjangoKart — Full-Stack E-Commerce Platform

DjangoKart is a modular e-commerce web application built using **Django** that implements a complete online shopping workflow including authentication, product browsing, cart management, and order processing. The project follows a scalable multi-app architecture inspired by real-world backend systems.

---

## 🚀 Features

* 🔐 User authentication and account management
* 🛍️ Product catalog with category-based browsing
* 🧺 Dynamic shopping cart with session management
* 📦 Order creation and checkout workflow
* 🗂️ Modular Django apps for scalable architecture
* ⚡ Server-side rendered templates with responsive UI

---

## 🧠 System Architecture

The project is designed using a **modular Django structure**, separating business logic into independent apps:

```
accounts  → authentication & user profiles
store     → products & categories
cart      → cart logic and state handling
orders    → order processing & checkout
```

This separation improves maintainability and mirrors production-level backend design.

---

## 🛠️ Tech Stack

* **Backend:** Django, Python
* **Database:** SQLite (can be switched to PostgreSQL/MySQL)
* **Frontend:** HTML, CSS, JavaScript
* **ORM:** Django ORM
* **Authentication:** Django Auth System

---

## 📂 Project Structure

```
DjangoKart/
│
├── accounts/
├── cart/
├── category/
├── orders/
├── store/
├── templates/
├── static/
└── manage.py
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/udaykiranreddyvangala/DjangoKart.git
cd DjangoKart
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv env
env\Scripts\activate   # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run Migrations

```bash
python manage.py migrate
```

### 5️⃣ Start Development Server

```bash
python manage.py runserver
```

Open:

```
http://127.0.0.1:8000/
```

---

## 💡 Key Design Highlights

* Designed reusable Django apps for scalability.
* Implemented cart state using session-based logic.
* Structured relational models using Django ORM.
* Clean separation between business logic and presentation layer.

---

## 📈 Future Improvements

* Payment gateway integration
* REST API version using Django REST Framework
* Redis-based cart storage
* Docker deployment
* Admin analytics dashboard

---

## 👨‍💻 Author

**Uday Kiran Reddy Vangala**
BTech Data Science — NIT Jalandhar
