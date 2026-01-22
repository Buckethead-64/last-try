import streamlit as st
import requests
from datetime import datetime
import pandas as pd

# Backend URL
BASE_URL = "http://localhost:8000"

st.title("Attendance Tracking System")

# Sidebar for navigation
page = st.sidebar.selectbox("Choose a page", ["Create User", "Check In/Out", "Daily Logs", "Monthly Report"])

if page == "Create User":
    st.header("Create New User")
    name = st.text_input("Name")
    email = st.text_input("Email")
    if st.button("Create User"):
        if name and email:
            response = requests.post(f"{BASE_URL}/users/", json={"name": name, "email": email})
            if response.status_code == 200:
                st.success("User created successfully!")
                st.json(response.json())
            else:
                st.error("Failed to create user")
        else:
            st.error("Please fill all fields")

elif page == "Check In/Out":
    st.header("Check In or Check Out")
    user_id = st.number_input("User ID", min_value=1, step=1)
    action = st.selectbox("Action", ["Check In", "Check Out"])
    if st.button("Submit"):
        if action == "Check In":
            check_in_time = datetime.now().isoformat()
            response = requests.post(f"{BASE_URL}/checkin/", json={"user_id": int(user_id), "check_in": check_in_time})
            if response.status_code == 200:
                st.success("Checked in successfully!")
                st.json(response.json())
            else:
                st.error("Failed to check in")
        else:
            check_out_time = datetime.now().isoformat()
            response = requests.post(f"{BASE_URL}/checkout/", json={"user_id": int(user_id), "check_out": check_out_time})
            if response.status_code == 200:
                st.success("Checked out successfully!")
                st.json(response.json())
            else:
                st.error("Failed to check out")

elif page == "Daily Logs":
    st.header("Daily Logs")
    date = st.date_input("Select Date")
    if st.button("Get Logs"):
        date_str = date.strftime("%Y-%m-%d")
        response = requests.get(f"{BASE_URL}/daily_logs/{date_str}")
        if response.status_code == 200:
            logs = response.json()
            if logs:
                df = pd.DataFrame([{
                    "User ID": log["user"]["id"],
                    "Name": log["user"]["name"],
                    "Email": log["user"]["email"],
                    "Check In": log["check_in"],
                    "Check Out": log["check_out"]
                } for log in logs])
                st.dataframe(df)
            else:
                st.info("No logs for this date")
        else:
            st.error("Failed to fetch logs")

elif page == "Monthly Report":
    st.header("Monthly Report")
    year = st.number_input("Year", min_value=2020, max_value=2030, value=2026)
    month = st.number_input("Month", min_value=1, max_value=12, value=1)
    if st.button("Get Report"):
        response = requests.get(f"{BASE_URL}/monthly_report/{int(year)}/{int(month)}")
        if response.status_code == 200:
            reports = response.json()
            if reports:
                df = pd.DataFrame(reports)
                st.dataframe(df)
            else:
                st.info("No data for this month")
        else:
            st.error("Failed to fetch report")