import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# 1. Load and sort the historical data
df = pd.read_csv('Nat_Gas.csv')
df['Dates'] = pd.to_datetime(df['Dates'])
df = df.sort_values('Dates')

# Define the base date (day 0) for our time frame
start_date = df['Dates'].min()

# 2. Feature Engineering
# Convert time to a continuous "Years" variable (t)
df['Days'] = (df['Dates'] - start_date).dt.days
df['Years'] = df['Days'] / 365.25

# Use trigonometric transformations to capture the annual cycle (1 year seasonality)
X = pd.DataFrame()
X['t'] = df['Years']
X['sin_t'] = np.sin(2 * np.pi * df['Years'])
X['cos_t'] = np.cos(2 * np.pi * df['Years'])

y = df['Prices']

# 3. Fit the Quantitative Model
model = LinearRegression()
model.fit(X, y)

# 4. Estimation Function (Core Deliverable)
def estimate_price(date_str):
    """
    Takes a date string (e.g., '2023-05-15') and returns the estimated price.
    Works for interpolating past dates and extrapolating future dates.
    """
    target_date = pd.to_datetime(date_str)
    
    # Calculate time delta in years (t)
    delta_days = (target_date - start_date).days
    t_years = delta_days / 365.25
    
    # Create the feature vector for prediction
    features = pd.DataFrame({
        't': [t_years],
        'sin_t': [np.sin(2 * np.pi * t_years)],
        'cos_t': [np.cos(2 * np.pi * t_years)]
    })
    
    # Predict and return the price
    predicted_price = model.predict(features)[0]
    return predicted_price

# --- EXECUTION AND TESTING ---
print(f"Estimated mid-month price (past) 2022-01-15: ${estimate_price('2022-01-15'):.2f}")
print(f"Projected future price (extrapolated) 2025-01-15: ${estimate_price('2025-01-15'):.2f}")

# 5. Continuous Visualization (Optional for analysis)
end_date = df['Dates'].max() + pd.DateOffset(years=1)
daily_dates = pd.date_range(start=start_date, end=end_date, freq='D')
prices_estimated = [estimate_price(d) for d in daily_dates]

plt.figure(figsize=(12, 6))
plt.plot(df['Dates'], df['Prices'], marker='o', linestyle='', color='black', label='Historical Monthly Data')
plt.plot(daily_dates, prices_estimated, color='blue', label='Continuous Price Model')
plt.axvspan(df['Dates'].max(), end_date, color='yellow', alpha=0.3, label='Extrapolation Window (1 Year)')

plt.title('Natural Gas Price Extrapolation Model', fontsize=14)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Price (USD)', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.5)
plt.tight_layout()
plt.show()
