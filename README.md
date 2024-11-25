* * *


# Game Store Website

This repository hosts the source code of [reza-taheri.ir](https://reza-taheri.ir)(temporary unavailable) a website built using Django, The site serves as a gaming store.

![Prince of Persia](https://github.com/user-attachments/assets/adc80554-142e-46a8-a94a-1a7534d25ad1)

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Configuration](#configuration)

## Features

- eCommerce stores with all functionalities
- Restful 
- Contact form for reaching out directly
- Fully responsive design
- Multi language support
- Dark mode
- Customizability
- Button in footer to change language

## Technologies

- **Backend:** Django 5.1.1 (Python 3.11)
- **Frontend:** HTML5, CSS3, JavaScript (jQuery, Bootstrap)
- **Database:** SQLite (default), MySQL (for production)
- **Multi language:** Use django.utils.translation and rosetta

## Installation

### 1. Clone the repository:

```bash
git clone https://github.com/RezaTaheri01/game-store.git
cd game-store
```

### Create a virtual environment and activate it:

```
python -m virtualenv venv
source venv/bin/activate
```

### 3. Install the dependencies:

```
pip install -r requirements.txt
```
### 4. There is a default superuser:

```
user : adminadmin
password : adminadmin
```

### 4. Alternatively remove db.sqlite3, apply migrations and create a superuser:

```
python manage.py migrate
python manage.py createsuperuser
```

### 5. Run the server:

```
python manage.py runserver
```

Access the site at http://127.0.0.1:8000/<br>
Django Admin at http://127.0.0.1:8000/admin<br>
Rosetta at http://127.0.0.1:8000/rosetta<br>
Api at http://127.0.0.1:8000/api/schema/swagger (use superuser user and password)<br>

## Configuration

- **SECRET_KEY**: Django secret key
- **DEBUG**: Set to False in production
- **ALLOWED_HOSTS**: Set the domain name for production
 ### To get activation code and reset password, complete below:
- **EMAIL_HOST**: SMTP server for sending emails
- **EMAIL_HOST_USER**: SMTP username
- **EMAIL_HOST_PASSWORD**: SMTP password

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/RezaTaheri01/game-store/edit/main/LICENSE) file for details.


* * *
