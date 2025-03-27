from streamlit_cookies_manager import EncryptedCookieManager
import streamlit as st
import pandas as pd
from datetime import datetime, date
import os
from utils import (
    calculate_projected_miles,
    calculate_actual_miles,
    calculate_average_daily_miles,
    calculate_miles_difference
)

# Initialize cookies
cookies = EncryptedCookieManager(
    prefix="milagetracker_",
    password="my-secret-key-123"  # Optional: update with env var or config for security
)

if not cookies.ready():
    st.stop()

def save_config():
    cookies["miles_per_year"] = st.session_state.miles_per_year
    cookies["start_miles"] = st.session_state.start_miles
    cookies["start_date"] = st.session_state.start_date.isoformat()
    cookies.save()

def load_config():
    st.session_state.miles_per_year = int(cookies.get("miles_per_year") or 12000)
    st.session_state.start_miles = int(cookies.get("start_miles") or 0)
    try:
        st.session_state.start_date = date.fromisoformat(cookies.get("start_date") or str(date.today()))
    except:
        st.session_state.start_date = date.today()

def initialize_session_state():
    if 'initialized' not in st.session_state:
        load_config()
        st.session_state.current_miles = st.session_state.start_miles
        st.session_state.show_configuration = True
        st.session_state.initialized = True

def configuration_screen():
    st.header("🚘 Lease Configuration")
    st.markdown("Use this form to set your lease details.")

    with st.form("configuration_form"):
        miles_per_year = st.number_input(
            "📅 Miles per year",
            min_value=0,
            value=int(st.session_state.miles_per_year),
            step=1000,
            format="%d"
        )

        start_date = st.date_input(
            "📆 Lease start date",
            value=st.session_state.start_date,
            max_value=date.today(),
            format="MM/DD/YYYY"
        )

        start_miles = st.number_input(
            "🚾 Starting odometer",
            min_value=0,
            value=int(st.session_state.start_miles),
            step=1,
            format="%d"
        )

        if st.form_submit_button("✅ Save"):
            st.session_state.miles_per_year = miles_per_year
            st.session_state.start_date = start_date
            st.session_state.start_miles = start_miles
            save_config()
            st.session_state.show_configuration = False
            st.success("Configuration saved!")
            st.rerun()

def main_screen():
    st.header("📈 Lease Mileage Tracker")

    current_miles = st.number_input(
        "📍 Current odometer reading",
        min_value=st.session_state.start_miles,
        value=max(st.session_state.get("current_miles", st.session_state.start_miles), st.session_state.start_miles),
        step=1,
        format="%d"
    )
    st.session_state.current_miles = current_miles

    # Calculations
    projected = calculate_projected_miles(st.session_state.start_date, st.session_state.start_miles, st.session_state.miles_per_year)
    actual = calculate_actual_miles(st.session_state.start_miles, current_miles)
    avg_daily = calculate_average_daily_miles(st.session_state.start_date, st.session_state.start_miles, current_miles)
    delta = calculate_miles_difference(projected, current_miles)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Projected Miles", f"{int(projected):,}")
        st.metric("Actual Miles", f"{int(actual):,}")
    with col2:
        st.metric("Avg. Daily Miles", f"{int(avg_daily):,}")
        st.metric("Miles Over/Under", f"{int(delta):,}", delta=f"{delta:+,}", delta_color="inverse")

    if st.button("⚙️ Edit Configuration"):
        st.session_state.show_configuration = True
        st.rerun()

def main():
    st.set_page_config(
        page_title="Lease Mileage Tracker",
        page_icon="🚗",
        layout="wide"
    )

    st.title("🚗 Lease Mileage Tracker")
    st.markdown("_Track your lease mileage and stay within contract limits._")

    initialize_session_state()

    if st.session_state.show_configuration:
        configuration_screen()
    else:
        main_screen()

if __name__ == "__main__":
    main()
