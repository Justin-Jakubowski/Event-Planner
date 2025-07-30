# 📅 Plannerly – Event Planning Web App

Plannerly is a full-stack event planning web application built using Python and Flask. It allows users to create accounts, manage events and tasks, invite guests, and visualize guest responses. Designed as a class project, it showcases practical web development concepts and integrates backend logic with dynamic HTML templates.

---

## 🚀 Features

- 🔐 **User Authentication** – Sign up and log in to access your dashboard
- 📆 **Event Management** – Create, modify, or delete events (e.g., meetings, parties)
- ✅ **Task Tracking** – Add and update tasks related to specific events
- 🧑‍🤝‍🧑 **Guest Invitations** – Invite guests to events and track RSVP responses
- 📊 **Visual Analytics** – View charts summarizing guest responses and gender distribution
- 🧩 **Modular Code** – Clean separation of routes, templates, and logic for scalability

---

## 🛠️ Technologies Used

- **Python** – Application logic and server-side functionality
- **Flask** – Lightweight web framework for routing and templates
- **HTML/CSS** – Front-end layout and styling
- **Jinja2** – Template engine for dynamic content rendering
- **FusionCharts**  – Data visualization for event analytics
- **Git / GitHub** – Version control and collaboration

---

## 📁 Project Structure
Plannerly/
├── app/
│   ├── __init__.py
│   ├── auth.py                  # Authentication logic
│   ├── routes.py                # Route definitions
│   ├── models.py                # Data models
│   ├── templates/               # All HTML templates
│   │   ├── includes/            # Reusable components (e.g., navbars, modals)
│   │   ├── layouts/             # Base layouts and template inheritance
│   │   ├── addGuest.html
│   │   ├── availability.html
│   │   ├── createAccount.html
│   │   ├── createEvent.html
│   │   ├── createtask.html
│   │   ├── eventOverview.html
│   │   ├── exploreresponses.html
│   │   ├── form.html
│   │   ├── genderVisualization.html
│   │   ├── graphResponses.html
│   │   ├── guestHome.html
│   │   ├── home.html
│   │   ├── index.html
│   │   ├── loginPage.html
│   │   ├── managescheduling.html
│   │   ├── modify.html
│   │   ├── modifyEvent.html
│   │   ├── modifytask.html
│   │   ├── page-403.html
│   │   ├── page-404.html
│   │   ├── page-500.html
│   │   ├── page-blank.html
│   │   ├── taskdetails.html
│   │   ├── userSetting.html
│   │   └── visualizeMeetings.html
│   └── static/                  # CSS, JS, and image files
├── run.py                       # Application entry point
├── requirements.txt             # Project dependencies
└── README.md                    # Project overview (this file)


