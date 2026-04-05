# 🏎️ Rocket League Pro Analytics Hub

A full-stack Data Engineering and Analytics platform that transforms raw Rocket League telemetry into actionable insights. This project features a complete data pipeline from **Web Scraping** to **Machine Learning** and **Interactive Visualization**.

---

## 🌟 Key Features
* **Automated Data Pipeline:** Custom scrapers to collect player stats, integrated with a **SQL (SQLite)** database for high-performance data management.
* **AI Playstyle Clustering:** Unsupervised learning (**K-Means**) to categorize players into distinct playstyles (Striker, Anchor, All-Around).
* **Performance Forecasting:** Predictive modeling using **Linear Regression** to forecast future player ranks and match performance.
* **Live Dashboard:** A neon-themed, interactive web interface built with **Streamlit** and **Plotly** for real-time telemetry exploration.

---

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Data Engineering:** SQL (SQLite), Pandas, NumPy
* **Machine Learning:** Scikit-Learn
* **Web Scraping:** BeautifulSoup4, Requests
* **Visualization:** Streamlit, Plotly
* **Deployment:** GitHub, Streamlit Cloud

---

## 📂 Project Structure
* `main.py`: The core Streamlit application and UI logic.
* `migrate_to_sql.py`: Script to migrate raw CSV data into the SQLite relational database.
* `data/`: Directory containing the SQLite database and raw telemetry files.
* `requirements.txt`: List of Python dependencies.

---

## 🚀 Getting Started

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/RocketLeagueAnalytics.git](https://github.com/YOUR_USERNAME/RocketLeagueAnalytics.git)
   cd RocketLeagueAnalytics

Install dependencies:

Bash
pip install -r requirements.txt
Initialize the Database:

Bash
python migrate_to_sql.py
Run the Dashboard:

Bash
streamlit run main.py
📊 Methodology
This project follows a professional data lifecycle:

Extraction: Scraping telemetry from esports trackers.

Transformation: Cleaning and feature engineering with Pandas.

Loading: Storing structured data in an optimized SQL environment.

Analysis: Applying AI models to derive playstyles and trends.

Created as a portfolio project to demonstrate Full-Stack Data Engineering capabilities.


<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/8ca93309-3ddc-4961-8e0a-57b22ed26337" />

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/69bb9fe4-8bd9-43d1-95cb-f93f1b338e4e" />

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/5782e414-9332-4f35-9af4-571fe5d4be31" />

<img width="1918" height="1077" alt="image" src="https://github.com/user-attachments/assets/13827051-6826-4e7d-b4ce-46a4758955fe" />

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/b77136e0-a4a1-465e-9a62-130aadb79efb" />

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/ef7a6fda-29dd-4d8c-bca3-df6ddde2c66b" />





