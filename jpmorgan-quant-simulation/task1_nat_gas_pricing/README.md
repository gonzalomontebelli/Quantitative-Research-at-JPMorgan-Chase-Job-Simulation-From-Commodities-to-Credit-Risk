# Task 1 — Natural Gas Price Extrapolation Model

## Objective

Build a function that estimates the natural gas price for **any date** — past (interpolation) or future (extrapolation up to 1 year ahead) — from monthly historical data.

## Approach

Linear regression with **harmonic features** to simultaneously capture the long-term trend and annual seasonality:

```
Price(t) = β₀ + β₁·t + β₂·sin(2πt) + β₃·cos(2πt)
```

## Usage

```python
from nat_gas_model import estimate_price

# Interpolation (past date)
price = estimate_price('2022-06-15')
print(f"Estimated price: ${price:.2f}")

# Extrapolation (future date)
price = estimate_price('2025-09-01')
print(f"Projected price: ${price:.2f}")
```

## Required Data

`Nat_Gas.csv` with columns `Dates` and `Prices` in the working directory (or `../data/`).
