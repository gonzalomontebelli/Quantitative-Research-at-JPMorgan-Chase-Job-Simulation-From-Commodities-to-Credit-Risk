# Task 2 — Natural Gas Storage Contract Pricer

## Objective

Value natural gas storage contracts considering multiple injection/withdrawal dates, physical facility constraints, and all cost components.

## Main Function

```python
from storage_contract_pricer import price_storage_contract

value = price_storage_contract(
    injection_dates    = ['2024-06-01', '2024-07-01'],
    withdrawal_dates   = ['2024-12-01', '2025-01-01'],
    injection_volumes  = [500_000, 500_000],
    withdrawal_volumes = [500_000, 500_000],
    purchase_prices    = [2.0, 2.1],
    sale_prices        = [3.5, 3.8],
    max_volume         = 1_000_000,
    max_rate           = 600_000,
    storage_cost_per_month = 50_000
)

print(f"Contract Fair Value: ${value:,.2f}")
```

## Modeled Constraints

- Maximum storage capacity
- Maximum flow rate per event
- Cannot withdraw more than what is stored
- Fixed monthly costs with correct partial month handling
