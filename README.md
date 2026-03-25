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

## 8. Using CRUD in the Admin Site

After logging in, you will be redirected to the admin dashboard:

![Admin Dashboard](image.png)

---

### ➕ Create Data
To create new data:
1. Click the **"Add"** button.
2. Fill in the required fields.
3. Click **"Save"** at the bottom.

![Create Data](image-4.png)

---

### 📖 Read Data
To view existing data:
- Click on a table name such as:
  - **Librarys**
  - **Prompts**
  - **Songs**
  - **Users**

![Read Data](image-1.png)

---

### ✏️ Update Data
To update existing data:
1. Click **"Change"**.
2. Select the row you want to edit.
3. Modify the information.
4. Click **"Save"**.

![Update Data](image-2.png)

---

### ❌ Delete Data
To delete data:
1. Click on a table name:
   - **Librarys**
   - **Prompts**
   - **Songs**
   - **Users**
2. Select the row you want to delete.
3. Click **"Delete"** at the bottom right.

![Delete Data](image-3.png)

## 8.1 Alternative CREATE & READ (Template Views)

In addition to the Admin site, you can use the **template-based frontend** to create and search data directly in the browser.

### 🔧 Setup

Run the development server as usual:

```bash
python manage.py runserver
```

### 🔗 Available Routes

The URL format follows: `http://127.0.0.1:8000/<operation>-<table>/`

| Operation | Table | URL |
|-----------|-------|-----|
| **Create** | User | [/create-user/](http://127.0.0.1:8000/create-user/) |
| **Search** | User | [/search-user/](http://127.0.0.1:8000/search-user/) |
| **Create** | Song | [/create-song/](http://127.0.0.1:8000/create-song/) |
| **Search** | Song | [/search-song/](http://127.0.0.1:8000/search-song/) |
| **Create** | Library | [/create-library/](http://127.0.0.1:8000/create-library/) |
| **Search** | Library | [/search-library/](http://127.0.0.1:8000/search-library/) |
| **Create** | Prompt | [/create-prompt/](http://127.0.0.1:8000/create-prompt/) |
| **Search** | Prompt | [/search-prompt/](http://127.0.0.1:8000/search-prompt/) |

---

### 📝 Create Example

Fill in the form fields and click **"Submit"** to create a new record.

![alt text](image-7.png)

---

### 🔍 Search Example

Use the search bar to filter records by name (e.g. username, song name). Leave it empty to view all records.

![Search Table Example](image-6.png)

> **Note:** For the **Search** pages, you can type a keyword to filter results (e.g. username, song name).  
> For the **Create** pages, simply fill in the fields and submit the form.

###  Delete row
Use the bin icon on the left and click it then click ok

###  Update row

Click on pencil icon and you will be redirect to update page
Enter all updated information there
![alt text](image-5.png)