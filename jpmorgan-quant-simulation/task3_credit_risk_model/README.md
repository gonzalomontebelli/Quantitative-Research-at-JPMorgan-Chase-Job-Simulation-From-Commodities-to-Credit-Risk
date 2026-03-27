# Task 3 — Credit Risk Model & Expected Loss Calculator

## Objective

Predict the Probability of Default (PD) of individual borrowers and compute the Expected Loss (EL) under the Basel II/III regulatory framework.

## Formula

```
EL = PD × EAD × LGD
```

- **PD:** Estimated by Logistic Regression (AUC: 1.00)
- **EAD:** Outstanding loan amount
- **LGD:** 90% (recovery rate = 10%)

## Usage

```python
from loan_expected_loss import calculate_expected_loss

el, pd_prob = calculate_expected_loss(
    credit_lines_outstanding = 5,
    loan_amt_outstanding     = 10_000,
    total_debt_outstanding   = 25_000,
    income                   = 35_000,
    years_employed           = 2,
    fico_score               = 550
)

print(f"PD: {pd_prob*100:.2f}%")
print(f"Expected Loss: ${el:,.2f}")
```

## Required Data

`Task 3 and 4_Loan_Data.csv` in the working directory.
