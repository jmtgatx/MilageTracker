import streamlit as st
import pandas as pd
from datetime import datetime, date
from utils import (
    calculate_projected_miles,
    calculate_actual_miles,
    calculate_average_daily_miles,
    calculate_miles_difference
)

def initialize_session_state():
    if 'miles_per_year' not in st.session_state:
        st.session_state.miles_per_year = 12000
    if 'start_date' not in st.session_state:
        st.session_state.start_date = date.today()
    if 'start_miles' not in st.session_state:
        st.session_state.start_miles = 0
    if 'current_miles' not in st.session_state:
        st.session_state.current_miles = 0
    if 'show_configuration' not in st.session_state:
        st.session_state.show_configuration = True

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
            "🛞 Starting odometer",
            min_value=0,
            value=int(st.session_state.start_miles),
            step=1,
            format="%d"
        )

        if st.form_submit_button("✅ Save"):
            st.session_state.miles_per_year = miles_per_year
            st.session_state.start_date = start_date
            st.session_state.start_miles = start_miles
            st.session_state.show_configuration = False
            st.success("Configuration saved!")
            st.rerun()

def main_screen():
    st.header("📈 Lease Mileage Tracker")

    current_miles = st.number_input(
        "📍 Current odometer reading",
        min_value=st.session_state.start_miles,
        value=max(st.session_state.current_miles, st.session_state.start_miles),
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
        st.metric("Miles Over/Under", f"{int(delta):,}",
                  delta=f"{delta:+,}", delta_color="inverse")

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
