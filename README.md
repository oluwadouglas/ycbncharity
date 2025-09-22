
# 🌍 YCBF Charity – Django Web Application

A fully functional Django web application for a charity organization, converted from a premium HTML template. The application features a modern responsive design, SEO-friendly routing, and Django’s best practices for templates and static file management.

---

## ✨ Features

* **Responsive Design** – Mobile-first layout that works on all devices
* **Multiple Pages** – Home, About, Contact, Blog, Donations, Team, Shop, Gallery, FAQ, and more
* **Static File Management** – Properly configured CSS, JS, and image assets
* **Template Inheritance** – Clean Django template structure with a base template
* **URL Routing** – SEO-friendly URLs for all pages
* **Navigation** – Dynamic navigation menu with URL reversing
* **Contact Form** – Includes CSRF protection (backend processing required)
* **Modern UI** – Charity-themed design with animations and effects

---

## 📂 Project Structure

```bash
ycbf_charity/
├── ycbf_charity/        # Django project settings
├── charity/             # Main Django app
│   ├── views.py         # View functions for all pages
│   ├── urls.py          # URL patterns
│   └── ...
├── templates/           # Django templates
│   └── charity/
│       ├── base.html    # Base template
│       ├── includes/    # Reusable template components
│       │   ├── header.html
│       │   ├── footer.html
│       │   └── mobile_menu.html
│       ├── index.html   # Home page
│       ├── about.html   # About page
│       ├── contact.html # Contact page
│       └── ... (other pages)
├── static/              # Static files
│   └── assets/          # CSS, JS, images
└── manage.py            # Django management script
```

---

## ⚙️ Installation & Setup

### Prerequisites

* Python **3.8+**
* pip (Python package manager)

### Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/ycbf_charity.git
   cd ycbf_charity
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Database setup**

   ```bash
   python manage.py migrate
   ```

4. **Create superuser (optional)**

   ```bash
   python manage.py createsuperuser
   ```

5. **Run development server**

   ```bash
   python manage.py runserver
   ```

   Visit: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 📑 Available Pages

* **Home** (`/`) – Landing page with hero section
* **About Us** (`/about/`) – Information about the charity
* **Contact** (`/contact/`) – Contact form and details
* **Blog** (`/blog/`) – Blog listing page
* **Donations** (`/donations/`) – Donation campaigns
* **Team** (`/team/`) – Team/volunteer info
* **Shop** (`/shop/`) – Merchandise store
* **Gallery** (`/gallery/`) – Photo gallery
* **FAQ** (`/faq/`) – Frequently asked questions

---

## 🎨 Customization

1. **Text Content** – Edit files in `templates/charity/`.
2. **Contact Info** – Update in `templates/charity/includes/header.html` and `footer.html`.
3. **Organization Name** – Replace `"YCBF Charity"` with your organization’s name.

### Adding New Pages

1. Create a view in `charity/views.py`
2. Add a URL in `charity/urls.py`
3. Create a template in `templates/charity/`

---

## 🚀 Deployment (Production)

1. Set `DEBUG = False` in `ycbf_charity/settings.py`
2. Configure `ALLOWED_HOSTS` with your domain
3. Use PostgreSQL (recommended for production)
4. Collect static files with:

   ```bash
   python manage.py collectstatic
   ```
5. Deploy with Gunicorn + Nginx (or another WSGI server)

---

## 🎨 Template Credits

Converted from the **Donat Premium HTML Template**.

---

## 📌 Repository Info

* **Stars**: ⭐ 0
* **Watchers**: 👀 0
* **Forks**: 🍴 0
* **Languages**:

  * Python (76.3%)
  * CSS (16.1%)
  * HTML (4.3%)
  * JavaScript (3.2%)

---

