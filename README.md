# 🎵 SongGTP CRUD Application

A Django-based CRUD (Create, Read, Update, Delete) web application for managing SongGTP data.  
This project demonstrates backend development using Django and Django Admin for rapid data management.

---

## 🚀 Getting Started

Follow the steps below to run the project locally.

---

## 1. Clone the Repository

```bash
git clone https://github.com/JirakornChaitanaporn/songGTP_CRUD.git
cd songGTP_CRUD
```
## 2. Create a Virtual Environment
macOS / Linux:
```bash
python3 -m venv .env
```
Windows:
```bash
python -m venv .env
```
## 3. Activate the Virtual Environment
macOS / Linux:
```bash
source .env/bin/activate
```
Windows
```bash
.env\Scripts\activate
```
## 4. Install Dependencies
```bash
pip install -r requirements.txt
```
## 5. Apply Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
## 6. Create a Superuser
```bash
python manage.py createsuperuser
```

Enter your preferred username, email, and password when prompted.

## 7. Run the Development Server
python manage.py runserver
🌐 Access the Application:
Main application:
http://127.0.0.1:8000/
Admin panel:
http://127.0.0.1:8000/admin/

Log in using the superuser credentials you created earlier.