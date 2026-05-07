# BPOMS - BPO Marketplace System

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)

**BPOMS** is a professional, LinkedIn-inspired professional ecosystem and marketplace designed for the Business Process Outsourcing (BPO) industry. It bridges the gap between clients, vendors, and agents by providing a transparent, metrics-driven platform for hiring and project management.

---

## 🌟 Key Features

### 🏢 Professional Marketplace
- **Vendor Discovery**: Browse a diverse list of service providers and individual agents.
- **Detailed Profiles**: Modern, professional profiles showcasing skills, work history, and performance metrics.
- **Hire Workflows**: Seamless interface for clients to submit hire requests and for vendors to manage proposals.

### 📱 Professional Social Feed
- **Success Stories**: A LinkedIn-style activity feed where vendors share professional achievements and project success stories.
- **Project Metrics**: Visual representation of project efficiency, CSAT scores, and completion timelines within feed posts.
- **Engagement**: Interactive feed with following systems and professional networking capabilities.

### 📊 Comprehensive Dashboards
- **Admin Portal**: Centralized management of users, tickets, and platform-wide analytics.
- **Vendor/Agent Dashboard**: Dedicated space for tracking assigned tasks, project progress, and performance KPIs.
- **Client Hub**: A unified project tracking dashboard with real-time updates and rating systems.

### 🛠️ Project Management & Analytics
- **Live Tracking**: Visual progress bars and task checklists for active projects.
- **KPI Visualization**: Real-time analytics on operational efficiency and service quality.
- **Ticketing System**: Integrated support and task management framework.

---

## 🚀 Tech Stack

- **Backend**: Python / Flask
- **Database**: SQLAlchemy (SQLite)
- **Authentication**: Flask-JWT-Extended
- **Frontend**: HTML5, Vanilla CSS3 (Modern UI), JavaScript
- **Templating**: Jinja2

---

## 🔧 Getting Started

### Prerequisites
- Python 3.8 or higher
- `pip` (Python package installer)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/bpoms.git
   cd bpoms
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/Scripts/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Database Initialization & Seeding

BPOMS comes with powerful simulation scripts to populate the platform with realistic data:

1. **Initialize the database**:
   ```bash
   python init_db.py
   ```

2. **Seed simulation data** (Marketplace, Users, Feeds):
   ```bash
   python seed_simulation.py
   ```

3. **(Optional) Seed large datasets**:
   ```bash
   python seed_large_data.py
   ```

### Running the Application

Start the Flask development server:
```bash
python run.py
```
The application will be accessible at `http://127.0.0.1:5000`.

---

## 📂 Project Structure

```text
├── app/
│   ├── routes/          # API & Web route definitions
│   ├── templates/       # HTML templates (Dashboards, Public Pages)
│   ├── static/          # CSS, Images, and Frontend JS
│   ├── models.py        # SQLAlchemy database models
│   └── __init__.py      # Flask app factory
├── seed_*.py            # Data simulation & seeding scripts
├── run.py               # Application entry point
├── requirements.txt      # Project dependencies
└── bpoms.sqlite         # Local SQLite database (ignored by git)
```

---

## 🎨 Screenshots

> [!NOTE]
> *Replace these placeholders with actual screenshots from your running application.*

| Feature | Description |
| :--- | :--- |
| **Public Marketplace** | A clean, modern list of available BPO vendors. |
| **Professional Feed** | LinkedIn-inspired updates with project success metrics. |
| **Client Dashboard** | Real-time project tracking and progress visualization. |
| **Agent Workspace** | Integrated task management and performance tracking. |

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Contributors

- **Priyanshu j jain **

---

*Wowed by the design? Star the repo! ⭐*
