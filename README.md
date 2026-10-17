# MUTITECH

AI-integrated websites for every budget, from KES 15,000 to KES 50,000.
This repository is the MUTITECH website: a Django site with Tailwind CSS styling.

## What's on the site

- Home, About, Packages, Process and Contact pages
- Three packages (Starter, Growth, Pro) with a comparison table and FAQ
- Contact form that saves every inquiry to the database and emails a notification
- Terms of Service on the About page, with an "I agree" checkbox on the contact form
- Keyword-based chatbot and a WhatsApp button
- Django admin for reading and managing inquiries

## Tech stack

- Python 3.12 and Django 5.2
- SQLite database
- Tailwind CSS 3.4 (standalone CLI, no Node needed)
- Plain JavaScript for the menu and chatbot
- WhiteNoise for static files

## Project layout
├── manage.py
├── requirements.txt
├── tailwind.config.js
├── tailwind/
│ └── input.css Tailwind source and all site styles
└── portfolio_site/
├── portfolio_site/ settings, urls, wsgi
├── main/ views, models, forms, admin, migrations
├── templates/ base.html and the page templates
└── static/css/output.css built CSS (committed, see Deploying)

Run every `python manage.py ...` command from the repository root.

## Running it locally

1. Create and activate a virtual environment, then install the requirements:

```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
```

2. Create your settings file and fill in the values:

```bash
   cp .env.example .env
```

3. Set up the database and an admin user:

```bash
   python manage.py migrate
   python manage.py createsuperuser
```

4. Download the Tailwind CLI once (Linux x64 shown; other platforms are on the
   [Tailwind releases page](https://github.com/tailwindlabs/tailwindcss/releases/tag/v3.4.17)):

```bash
   curl -sLo tailwindcss https://github.com/tailwindlabs/tailwindcss/releases/download/v3.4.17/tailwindcss-linux-x64
   chmod +x tailwindcss
```

5. In one terminal, keep the CSS rebuilding while you work:

```bash
   ./tailwindcss -i tailwind/input.css -o portfolio_site/static/css/output.css --watch
```

6. In a second terminal, start the site and open http://127.0.0.1:8000:

```bash
   python manage.py runserver
```

## Settings (`.env`)

Never commit `.env`. See `.env.example` for the variable names.

| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` locally, `False` in production |
| `ALLOWED_HOSTS` | Comma-separated hostnames |
| `CSRF_TRUSTED_ORIGINS` | Comma-separated origins, with `https://` |
| `EMAIL_HOST_USER` | Gmail address that sends inquiry notifications |
| `EMAIL_HOST_PASSWORD` | Gmail app password |
| `DATABASE_URL` | Optional database URL (defaults to SQLite) |

## Changing the design

All styles live in `tailwind/input.css`, written against the ids and classes in the
templates. Colours, fonts and spacing are set in `tailwind.config.js`.

## Deploying (PythonAnywhere)

PythonAnywhere does not run the Tailwind program, so build the CSS locally and commit it:

```bash
./tailwindcss -i tailwind/input.css -o portfolio_site/static/css/output.css --minify
git add portfolio_site/static/css/output.css
git commit -m "Rebuild CSS"
git push
```

Then, in a Bash console on PythonAnywhere:

```bash
cd <your-repo-folder>
git pull
source <your-virtualenv>/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

Finally, press **Reload** on the Web tab. The Web tab also needs a static files entry
mapping `/static/` to the `staticfiles` folder, and a correct WSGI configuration file.

## Notes

- Migrations `0007` and `0008` import `cloudinary`, so that package stays in
  `requirements.txt` even though Cloudinary is no longer used.
