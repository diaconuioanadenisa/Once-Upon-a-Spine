# Once Upon a Spine

A Django prototype for a small bookshop selling new books, pre-owned books, bookmarks and reading accessories. The P2 build includes a database-backed catalogue, search and category filters, product detail pages, registration, login, and Django admin.

## Run it in Visual Studio Code

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and start it.
2. Open this repository folder in Visual Studio Code.
3. Copy `.env.example` to `.env` if you want to customize local settings. The included development defaults work for a local demo.
4. In VS Code, open **Terminal → New Terminal** and run:

   ```powershell
   docker compose up --build
   ```

5. Open [http://localhost:8000](http://localhost:8000). The first start applies database migrations and loads the sample catalogue.

To stop the app, press **Ctrl+C** in the terminal, then run `docker compose down`. Use `docker compose down -v` only when you want to delete the local database and its data.

### Demo account

- Username: `reader`
- Password: `ReadingRoom!2026`

You can also create an account using **Join the book club**. For Django admin, create a local administrator with `docker compose exec web python manage.py createsuperuser`, then visit `/admin/`.

## Local Python run (without Docker)

Use Python 3.12 or newer. From this folder:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_catalog
python manage.py runserver
```

Without `DATABASE_URL`, Django uses a local SQLite file. Docker Compose uses PostgreSQL 16.

## Sample data

Run `python manage.py seed_catalog` to load 32 sample products across four categories: new books (12), pre-owned books (10), bookmarks (5), and accessories (5). The seed command preserves existing records and creates the demo reader account on first run.

## Project structure

- `config/` — Django settings and application entry points
- `store/` — catalogue models, views, admin, migration, and seed command
- `templates/` and `static/` — English-language shop interface and styling
- `docker-compose.yml` — PostgreSQL and Django services

## Technology and current scope

- Python 3.12, Django 5.2, Bootstrap 5, PostgreSQL 16, Docker Compose, pytest
- Login and registration use Django's built-in authentication and password validation.
- Stripe test credentials are placeholders in `.env.example`. Checkout and payment processing are planned for the next milestone and are not enabled in this P2 catalogue prototype.
- This project was created with AI assistance. Generated sample catalogue copy and seed data are illustrative; review and adapt them before a final submission or commercial use.

## Tests

Run the test suite inside the web container with `docker compose exec web pytest`. Django's built-in system checks run with `docker compose exec web python manage.py check`.
