import pandas as pd
from dateutil.relativedelta import relativedelta

def price_storage_contract(
    injection_dates, 
    withdrawal_dates, 
    injection_volumes,
    withdrawal_volumes,
    purchase_prices, 
    sale_prices, 
    max_volume,
    max_rate,
    storage_cost_per_month,
    injection_cost_per_mmbtu=0.0,
    withdrawal_cost_per_mmbtu=0.0
):
    """
    Prices a generalized natural gas storage contract based on schedules, physical constraints, and cash flows.
    
    Parameters:
    - injection_dates (list): Dates of injection ('YYYY-MM-DD')
    - withdrawal_dates (list): Dates of withdrawal ('YYYY-MM-DD')
    - injection_volumes (list): Gas to inject per date (MMBtu)
    - withdrawal_volumes (list): Gas to withdraw per date (MMBtu)
    - purchase_prices (list): Price per MMBtu on injection dates
    - sale_prices (list): Price per MMBtu on withdrawal dates
    - max_volume (float): Maximum capacity of the storage facility
    - max_rate (float): Maximum volume that can be injected/withdrawn per event
    - storage_cost_per_month (float): Fixed monthly cost
    - injection_cost_per_mmbtu (float): Variable injection cost
    - withdrawal_cost_per_mmbtu (float): Variable withdrawal cost
    """
    
    # 1. Combine all events into a single chronological timeline
    events = []
    for d, v, p in zip(injection_dates, injection_volumes, purchase_prices):
        events.append({'date': pd.to_datetime(d), 'type': 'inject', 'volume': v, 'price': p})
        
    for d, v, p in zip(withdrawal_dates, withdrawal_volumes, sale_prices):
        events.append({'date': pd.to_datetime(d), 'type': 'withdraw', 'volume': v, 'price': p})
        
    # Sort events by date
    events = sorted(events, key=lambda x: x['date'])
    
    current_volume = 0.0
    total_cash_flow = 0.0
    
    if not events:
        return 0.0
        
    start_date = events[0]['date']
    end_date = events[-1]['date']
    
    # 2. Process each event simulating the physical storage balance
    for event in events:
        vol = event['volume']
        event_date = event['date'].strftime('%Y-%m-%d')
        
        # Enforce rate constraints (flow limit)
        if vol > max_rate:
            print(f"Warning: Scheduled volume {vol} on {event_date} exceeds max rate {max_rate}. Capping volume.")
            vol = max_rate
            
        if event['type'] == 'inject':
            # Enforce maximum storage capacity constraint
            if current_volume + vol > max_volume:
                allowed_vol = max_volume - current_volume
                print(f"Warning: Injection on {event_date} exceeds capacity. Capping volume to {allowed_vol}.")
                vol = allowed_vol
                
            current_volume += vol
            # Cash outflow for purchasing the commodity + variable injection cost
            total_cash_flow -= (vol * event['price']) + (vol * injection_cost_per_mmbtu)
            
        elif event['type'] == 'withdraw':
            # Enforce physical limit (cannot withdraw more gas than what is stored)
            if vol > current_volume:
                print(f"Warning: Withdrawal on {event_date} exceeds current stored volume. Capping volume to {current_volume}.")
                vol = current_volume
                
            current_volume -= vol
            # Cash inflow from selling the commodity - variable withdrawal cost
            total_cash_flow += (vol * event['price']) - (vol * withdrawal_cost_per_mmbtu)
            
    # 3. Calculate fixed storage costs over the entire contracted period
    delta = relativedelta(end_date, start_date)
    months_stored = delta.years * 12 + delta.months
    
    # Add a partial month if there are remaining days (standard industry practice)
    if delta.days > 0 or months_stored == 0:
        months_stored += 1
        
    total_storage_cost = months_stored * storage_cost_per_month
    total_cash_flow -= total_storage_cost
    
    return total_cash_flow

# ==========================================
# TEST CASE: Multi-Date Contract Valuation
# ==========================================
print("--- JPMC Storage Contract Valuator 2.0 ---")

# Client wants to inject over two summer months, and withdraw over two winter months
in_dates = ['2024-06-01', '2024-07-01']
out_dates = ['2024-12-01', '2025-01-01']

in_vols = [500000, 500000]   # 1M MMBtu total
out_vols = [500000, 500000]

prices_in = [2.0, 2.1]       # Prices rise slightly in late summer
prices_out = [3.5, 3.8]      # Peak prices in winter

# Facility Constraints
max_vol = 1000000            # Can store 1M MMBtu max
max_r = 600000               # Can move up to 600k MMBtu per event
storage_cost = 50000         # $50K per month rental fee

# Calculate Value
contract_value = price_storage_contract(
    injection_dates=in_dates, 
    withdrawal_dates=out_dates, 
    injection_volumes=in_vols, 
    withdrawal_volumes=out_vols, 
    purchase_prices=prices_in, 
    sale_prices=prices_out, 
    max_volume=max_vol, 
    max_rate=max_r, 
    storage_cost_per_month=storage_cost
)

print(f"Calculated Contract Value (Fair Value): ${contract_value:,.2f}")
