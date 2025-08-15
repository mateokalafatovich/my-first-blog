# Django Blog Website

A Django-based blogging platform that allows users to read, search, and interact with posts.
Built to explore full-stack web development with Python, Django, HTML, CSS, and Bootstrap.

## 🌐 Live Website  
🔗 **[Visit the Blog](https://makala.pythonanywhere.com/)**

---

## ✨ Features
- Secure Django admin panel for managing blog posts.
- Create and edit blog entries.
- Readers can leave comments on posts.
- Users can like and unlike posts.
- Search posts by title or content.
- Optimized for mobile and desktop.
- Django-powered backend with SQLite (default).

## 🛠️ Tech Stack
- **Backend:** Django (Python)
- **Database:** SQLite (default, can be replaced with PostgreSQL/MySQL)
- **Frontend:** HTML, CSS, Bootstrap
- **Hosting:** PythonAnywhere

---

## Project Structure
```bash
my-first-blog/
├── blog/                # Main blog app
│   ├── migrations/      # Database migrations
│   ├── static/          # CSS, JS, and images
│   ├── templates/       # HTML templates
│   ├── admin.py         # Admin interface
│   ├── models.py        # Database models
│   ├── urls.py          # URL routing
│   └── views.py         # View logic
├── mysite/              # Project configuration
├── manage.py            # Django management script
└── README.md            # Project README
```

---

## 🚀 Getting Started Locally  

**1. Clone the Repository**

```bash
git clone https://github.com/mateokalafatovich/my-first-blog.git
cd my-first-blog
```

**2. Create a Virtual Environment**

```bash
python -m venv .venv
source .venv/bin/activate  # On Mac/Linux
.\.venv\Scripts\activate   # On Windows
```

**3. Install Dependencies**

```bash
pip install -r requirements.txt
```

**4. Apply Migrations**

```bash
python manage.py migrate
```

**5. Run the Server**

```bash
python manage.py runserver
```

**6.** Open your browser and go to http://127.0.0.1:8000
