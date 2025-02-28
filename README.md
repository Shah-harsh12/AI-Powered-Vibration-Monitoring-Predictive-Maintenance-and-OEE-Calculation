# AI-Powered-Vibration-Monitoring-Predictive-Maintenance-and-OEE-Calculation
## **Project Description:**  
Industrial machinery often exhibits early warning signs before failure, such as abnormal vibration patterns, inconsistent performance, and reduced efficiency. To prevent unplanned downtime, reduce maintenance costs, and optimize equipment performance, this project leverages **Machine Learning (ML) and Artificial Intelligence (AI)** to monitor vibration data, predict failures, and calculate **Overall Equipment Effectiveness (OEE).**  

### **Key Objectives:**  
1. **Vibration Monitoring & Anomaly Detection:**  
   - Analyze real-time vibration sensor data to detect unusual patterns.  
   - Train an ML model to identify potential equipment failures before they occur.  

2. **Predictive Maintenance:**  
   - Develop a predictive maintenance model that forecasts potential breakdowns.  
   - Enable proactive scheduling of maintenance activities, reducing downtime.  

3. **OEE Calculation & Prediction:**  
   - Compute OEE using **Availability, Performance, and Quality** metrics.  
   - Build a predictive model to estimate future OEE based on operational data.  

### **Implementation Approach:**  
- **Data Collection & Preprocessing:** Utilize real-world datasets from sources like Kaggle to clean, preprocess, and prepare data for model training.  
- **Model Development:** Use ML algorithms such as **Random Forest, XGBoost, Isolation Forest, Autoencoders, and Regression Models** to predict failures and OEE scores.  
- **Model Evaluation:** Assess the model’s accuracy using performance metrics like **F1-score, RMSE, and cross-validation.**  
- **Deployment & Integration:** Implement a **Flask/FastAPI-based API** to integrate with industrial IoT systems for real-time predictions. Optionally, develop a simple **web interface** for visualization.  

### **Expected Impact:**  
- **Reduce unplanned downtime** by accurately predicting machine failures.  
- **Optimize maintenance schedules** to lower operational costs.  
- **Improve production efficiency** by continuously monitoring OEE metrics.  

### **Technology Stack:**  
- **Programming Language:** Python  
- **Libraries & Frameworks:** Pandas, NumPy, Scikit-learn, XGBoost, TensorFlow (optional), Matplotlib, Seaborn, Flask/FastAPI  
- **Deployment:** Local server, Heroku (optional)  

This project is designed to provide a **scalable, AI-driven solution for industrial equipment monitoring**, making manufacturing processes more **efficient, reliable, and cost-effective.**

# Project Setup Guide

## Backend Setup (Flask)

1. Create a folder named `flask` and navigate to it.
2. Set up a virtual environment:
   ```sh
   py -m venv .env
   ```
3. Activate the virtual environment:
   ```sh
   .env\Scripts\activate
   ```
   **Note:** If activation fails, use the following command:
   ```sh
   Set-ExecutionPolicy Unrestricted -Scope Process
   ```
4. Install Flask:
   ```sh
   pip install flask
   ```
5. Save dependencies:
   ```sh
   pip freeze > requirements.txt
   ```
6. Create the main application file:
   ```sh
   app.py  # Create this file inside the flask folder
   ```

## Frontend Setup

1. Inside the `flask` folder:
   - Create a folder named `static` to store CSS files.
   - Create a folder named `templates` to store HTML files.
   - Store JavaScript files directly in the `flask` folder.
   - /my_project
   - ├── app.py
   - ├── index.html
   - ├── script.js  ✅ (Make sure it's here)
   - ├── static/
     │  ├── style.css  (Tailwind compiled CSS)
   - └── templates/
   - |- ├── index.html
     
## Model Training Steps

1. **Data Collection**
2. **Exploratory Data Analysis (EDA)**
3. **Model Training**

   *All tasks are performed using Jupyter Notebook.*

## Website Integration

- I use **QM42VT2** sensor and **Modbus** for data collection.
- Modify your code based on your **Modbus** measurements.
- Used **Postman** for backend API testing.

---

This setup ensures a structured approach for development, model training, and integration.
