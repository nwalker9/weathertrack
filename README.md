# DataTrack

A full-stack data analytics web application built with Django. DataTrack collects, stores, and visualizes real-world datasets through interactive dashboards — currently featuring live weather data and FIFA 2017 player statistics.

## Live Demo

> Run locally — see setup instructions below.

## Tech Stack

- **Backend:** Python, Django 6, pandas
- **Frontend:** Bootstrap 5, Chart.js, Bootstrap Icons
- **Database:** SQLite
- **APIs:** Open-Meteo Weather API
- **Deployment ready:** gunicorn, whitenoise, python-decouple

## Features

### Weather Dataset
- Live daily weather data for Tallahassee, Miami, and Atlanta via the Open-Meteo API
- Automated data pipeline (`fetch_data` management command) fetches 4 weeks of data in paginated chunks
- Full CRUD — create, view, edit, and delete weather records
- Search by city name
- Analytics dashboard with line, bar, and doughnut charts powered by pandas aggregations

### FIFA 2017 Players Dataset
- 17,583 player records with 16 attributes (rating, speed, strength, dribbling, ball control, etc.)
- Search by name, filter by position and player level
- Detail page with progress bar stats for each attribute
- Analytics dashboard with 4 Chart.js charts:
  - Speed and strength trends by age (line chart)
  - Average speed by position (bar chart)
  - Player level distribution (doughnut chart)
  - Dribbling vs ball control relationship (scatter chart)

### Platform
- Responsive Bootstrap 5 navbar with mobile hamburger
- Django admin panel with customized list display, search, and filters
- Paginated list views (25 records per page)
- Split settings for development and production (`base.py`, `dev.py`, `prod.py`)
- Environment variables managed via `.env` and `python-decouple`

## Screenshots

### Homepage
![Homepage](Project3-Full-Stack-Data-Web-Application-with-Django/screenshots/homepage.png)

### Weather Records
![Records](Project3-Full-Stack-Data-Web-Application-with-Django/screenshots/records.png)

### Analytics Dashboard
![Analytics](Project3-Full-Stack-Data-Web-Application-with-Django/screenshots/Analytics.png)

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/nwalker9/weathertrack.git
cd weathertrack/Project3-Full-Stack-Data-Web-Application-with-Django

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create a .env file with:
# SECRET_KEY=your-secret-key-here
# DEBUG=True
# ALLOWED_HOSTS=localhost,127.0.0.1

# 4. Run migrations
python manage.py migrate

# 5. Load weather data
python manage.py seed_data

# 6. Load FIFA player data
python manage.py seed_players

# 7. Start the server
python manage.py runserver
```

Open `http://127.0.0.1:8000` in your browser.

## Data Pipeline

Fetch fresh weather data from the Open-Meteo API:

```bash
python manage.py fetch_data
```

Fetches 4 weeks of daily weather data for all 3 cities in 7-day chunks using `update_or_create` to avoid duplicates. Can be scheduled with cron:

```
0 6 * * * python manage.py fetch_data
```

## Project Structure

```
Project3-Full-Stack-Data-Web-Application-with-Django/
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── prod.py
│   ├── urls.py
│   └── wsgi.py
├── myapp/
│   ├── management/commands/
│   │   ├── seed_data.py
│   │   ├── seed_players.py
│   │   └── fetch_data.py
│   ├── templates/myapp/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── data/raw/
│   └── weather_data.csv
├── requirements.txt
├── Procfile
└── manage.py
```

## Developer

**Nicolas Walker**  
Computer Science — Florida State University  
GitHub: [nwalker9](https://github.com/nwalker9)
