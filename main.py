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
    """Initialize session state variables if they don't exist."""
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
    """Render the configuration screen."""
    st.header("Lease Configuration")

    with st.form("configuration_form"):
        miles_per_year = st.number_input(
            "Miles per year in lease contract",
            min_value=0,
            value=int(st.session_state.miles_per_year),
            step=1000,
            format="%d",
            help="Enter the annual mileage limit from your lease agreement"
        )

        start_date = st.date_input(
            "Lease start date",
            value=st.session_state.start_date,
            max_value=date.today(),
            help="Select the start date of your lease",
            format="MM/DD/YYYY"
        )

        start_miles = st.number_input(
            "Starting odometer reading",
            min_value=0,
            value=int(st.session_state.start_miles),
            step=1,
            format="%d",
            help="Enter the initial mileage reading when lease started"
        )

        if st.form_submit_button("Save Configuration"):
            st.session_state.miles_per_year = miles_per_year
            st.session_state.start_miles = start_miles
            st.session_state.start_date = start_date
            st.session_state.show_configuration = False
            st.success("Configuration saved successfully!")
            st.rerun()

def main_screen():
    """Render the main screen."""
    st.header("Lease Mileage Tracker")

    # Current mileage input
    current_miles = st.number_input(
        "Current odometer reading",
        min_value=st.session_state.start_miles,
        value=max(st.session_state.current_miles, st.session_state.start_miles),
        step=1,
        format="%d",
        help="Enter your current odometer reading"
    )
    st.session_state.current_miles = current_miles

    # Calculations
    projected_miles = calculate_projected_miles(
        st.session_state.start_date,
        st.session_state.start_miles,
        st.session_state.miles_per_year
    )

    actual_miles = calculate_actual_miles(
        st.session_state.start_miles,
        current_miles
    )

    avg_daily_miles = calculate_average_daily_miles(
        st.session_state.start_date,
        st.session_state.start_miles,
        current_miles
    )

    miles_difference = calculate_miles_difference(
        projected_miles,
        current_miles
    )

    # Display results
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Projected Miles",
            f"{int(projected_miles):,}",
            help="Expected mileage based on lease terms"
        )
        st.metric(
            "Actual Miles Driven",
            f"{int(actual_miles):,}",
            help="Total miles driven since lease start"
        )

    with col2:
        st.metric(
            "Average Daily Miles",
            f"{int(avg_daily_miles):,}",
            help="Average miles driven per day"
        )
        st.metric(
            "Miles Above/Below Projection",
            f"{int(miles_difference):,}",
            delta=f"-{int(abs(miles_difference)):,}" if miles_difference < 0 else f"+{int(abs(miles_difference)):,}",
            delta_color="inverse",  # Inverse will show red for negative and green for positive
            help="Green means you're under projection, Red means you're over"
        )

    # Configuration button
    if st.button("Edit Configuration"):
        st.session_state.show_configuration = True
        st.rerun()

def main():
    """Main application entry point."""
    st.set_page_config(
        page_title="Lease Mileage Calculator",
        page_icon="🚗",
        layout="wide"
    )

    initialize_session_state()

    if st.session_state.show_configuration:
        configuration_screen()
    else:
        main_screen()

if __name__ == "__main__":
    main()