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
🌐 Access the Admin site:
Admin url:
http://127.0.0.1:8000/admin/

Log in using the superuser credentials you created earlier.

## 8. Using CRUD in admin site
After you login you will be in this pagr
![alt text](image.png)

# to CREATE data in table click on the add button then insert data you want then click save on the bottom left

![alt text](image-4.png)
# to READ click on the table name: Librarys, Prompts, Songs and Users

![alt text](image-1.png)
# to UPDATE click change then choose the row to be edited and enter new information

![alt text](image-2.png)
# to DELETE click on the table name: Librarys, Prompts, Songs and Users then click the row that will be deleted then go to bottm right and click delete

![alt text](image-3.png)