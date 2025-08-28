📅 Plannerly – Event Planning Web App

Plannerly is a full-stack event planning web application built with Python and Flask.
It allows users to create accounts, manage events and tasks, invite guests, and visualize responses.
Originally designed as a class project, it demonstrates practical web development concepts by integrating backend logic with dynamic HTML templates.

🚀 Features

🔐 User Authentication – Secure sign up and login system

📆 Event Management – Create, update, and delete events (meetings, parties, etc.)

✅ Task Tracking – Add and update tasks tied to specific events

🧑‍🤝‍🧑 Guest Invitations – Invite guests and track RSVP responses

📊 Visual Analytics – Charts summarizing guest responses and gender distribution

🧩 Modular Code – Clean separation of routes, templates, and logic for scalability

🛠️ Tech Stack

Backend: Python, Flask

Frontend: HTML, CSS, Jinja2

Data Visualization: FusionCharts

Version Control: Git + GitHub

Database: Azure SQL (hosted by Virginia Tech)

📁 Project Structure
Plannerly/
├── app/
│   ├── __init__.py          
│   ├── auth.py              
│   ├── views.py             
│   ├── routes.py            
│   ├── models.py            
│   ├── templates/           
│   │   ├── layouts/         
│   │   ├── includes/        
│   │   └── *.html           
│   └── static/              
├── run.py                   
├── requirements.txt         
└── README.md                

📖 Detailed File Overview

**__init__.py**

Initializes the Flask app and sets up the connection to the Azure database (hosted by Virginia Tech).

**views.py**

Handles rendering HTML templates and processing user input. When users submit forms (via POST/GET), this file runs the necessary logic or formulas, then returns the correct page view.

**auth.py**

Manages user authentication (sign up, login, session handling). Ensures only authorized users can access their dashboards and event data.

**routes.py**

Defines the URL paths (routes) for the application, mapping user navigation (e.g., /login, /createEvent) to functions in views.py and auth.py.

**models.py**

Contains the data models for events, tasks, and guests. These models interact with the Azure database to store and retrieve information.

**templates/layouts/**

Houses the HTML templates used throughout the app. Key pages include:

**createAccount.html**
 → Create a user account

**createEvent.html**
 → Define a new event

**addGuest.html**
 → Add guests and manage RSVP invitations

**genderVisualization.html**
 → Display event guest gender statistics

**eventOverview.html**
 → Overview of event details and tasks

page-403.html
, page-404.html
, page-500.html
 → Error handling pages

**static/**

Contains all CSS, JavaScript, and image files used by the templates.

**run.py**

Entry point for starting the application. Runs the Flask development server.
