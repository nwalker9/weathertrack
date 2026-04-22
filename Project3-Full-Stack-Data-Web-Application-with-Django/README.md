# Full-Stack Data Web Application with Django
 
## Group Members
 
| Name | Student ID | Role |
|---|---|---|
| Larry Shi | LJS22J | Views & Templates Lead |
| Nicolas Walker | NW24E | Models & Data Lead |
| Harsh Thakor | HJT24B | Frontend Lead |
 
## Project Description
 
This project is a full-stack Django web application that collects, stores, and visualizes daily weather data for three Florida-region cities: Tallahassee, Miami, and Atlanta. It builds on the automated data pipeline from Project 2, integrating the Open-Meteo API into a navigable website with CRUD functionality and an analytics dashboard powered by pandas and Chart.js.
 
The real-world purpose is to simulate how organizations track and analyze weather patterns over time for planning, forecasting, and decision-making.
 
## Links
 
- **Dataset:** Project 2 weather CSV (`data/raw/weather_data.csv`)
- **API Documentation:** https://open-meteo.com/en/docs
- **Archive API Documentation:** https://open-meteo.com/en/docs/historical-weather-api
## Application Features
 
| Page | URL | Description |
|---|---|---|
| Homepage | `/` | Overview of the app with stats and navigation |
| Records list | `/records/` | Paginated table of all weather records |
| Record detail | `/records/<pk>/` | Full detail view for a single record |
| Add record | `/records/add/` | Form to create a new weather record |
| Edit record | `/records/<pk>/edit/` | Form to update an existing record |
| Delete record | `/records/<pk>/delete/` | Confirmation page before deleting |
| Analytics | `/analytics/` | Pandas aggregations with Chart.js charts |
| Admin | `/admin/` | Django admin panel |
## Screenshots

### Homepage
![Homepage](screenshots/homepage.png.png)

### Records
![Records](screenshots/records.png.png)

### Analytics
![Analytics](screenshots/Analytics.png.png)
