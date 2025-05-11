
# 🚀 TechPerson – IT Education Platform

An online platform designed to help you learn modern IT technologies 🖥️! Built with Django, this web project offers a complete system with courses, mentors, user management, and SMS-based registration.

---

## 🔑 Key Features

* 📚 **Course catalog** – with filtering and detailed course pages.
* 👩‍🏫 **Mentor listings** – view profiles and leave reviews.
* 📱 **OTP-based registration** – via SMS to your phone number.
* 🧑‍💻 **User profile management** – easily update personal info.
* ✉️ **Contact form** – for quick questions or feedback.
* 🔍 **Search** – find courses by name or topic.

---

## 🛠️ Technologies Used

* **Backend:** `Python 3.10+`, `Django 5.x`
* **Frontend:** `HTML5`, `CSS3`, `JavaScript` (optionally with `Bootstrap 5`)
* **Database:** `SQLite3` (for development), `PostgreSQL` (recommended for production)
* **SMS Service:** [Twilio API](https://www.twilio.com/)
* **Libraries:** `python-decouple`, `Pillow`, `django-crispy-forms`

---

## ⚙️ Local Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
   cd YOUR_REPOSITORY_NAME
   ```

2. **Create a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   # venv\Scripts\activate    # Windows
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file:**

   ```ini
   SECRET_KEY='your_secret_key'
   DEBUG=True
   TWILIO_ACCOUNT_SID='ACxxxxxxxxxxxxxx'
   TWILIO_AUTH_TOKEN='xxxxxxxxxxxxxxx'
   TWILIO_PHONE_NUMBER='+1xxxxxxxxxx'
   ```

5. **Apply database migrations:**

   ```bash
   python3 manage.py migrate
   ```

6. **Create a superuser:**

   ```bash
   python3 manage.py createsuperuser
   ```

7. **Start the development server:**

   ```bash
   python3 manage.py runserver
   ```

   👉 Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

---

## 📁 Project Structure

```
education_core/    # Main project settings and configuration
learning_hub/      # App for courses, mentors, contact, etc.
users/             # App for authentication and user profiles
static/            # Global static files
mediafiles/        # User-uploaded media (ignored in version control)
```

---

✨ Showcase (or Screenshots)

Here's a sneak peek of what TechPerson looks like:

<p align="center">
  <img src="readme_assets/screenshot_homepage.png" alt="TechPerson Homepage Screenshot" width="700">
  <em>Homepage of the TechPerson Platform</em>
</p>

<br>

<p align="center">
  <img src="readme_assets/screenshot_courses.png" alt="TechPerson Courses Page Screenshot" width="700">
  <em>Course Listing Page</em>
</p>

## 👩‍💻 Author

**Akmatova Nazira** ❤️

> Our goal – to help everyone step into the world of IT with ease!
