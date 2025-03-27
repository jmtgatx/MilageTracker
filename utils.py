from datetime import datetime, date
import pandas as pd

def calculate_projected_miles(start_date: date, 
                            start_miles: float, 
                            miles_per_year: float) -> float:
    """Calculate projected miles based on lease terms."""
    days_elapsed = (date.today() - start_date).days
    projected_daily_miles = miles_per_year / 365
    return start_miles + (projected_daily_miles * days_elapsed)

def calculate_actual_miles(start_miles: float, 
                         current_miles: float) -> float:
    """Calculate actual miles driven."""
    return current_miles - start_miles

def calculate_average_daily_miles(start_date: date, 
                                start_miles: float, 
                                current_miles: float) -> float:
    """Calculate average daily miles driven."""
    days_elapsed = max(1, (date.today() - start_date).days)  # Ensure minimum 1 day
    actual_miles = current_miles - start_miles
    return actual_miles / days_elapsed if days_elapsed > 0 else 0.0

def calculate_miles_difference(projected_miles: float, 
                             current_miles: float) -> float:
    """Calculate difference between projected and actual miles."""
    return current_miles - projected_miles