import pandas as pd
import numpy as np

# 1. Load Data
df = pd.read_csv('Task 3 and 4_Loan_Data.csv')

# Group by FICO score to get total defaults (k) and total records (n) per unique score
grouped = df.groupby('fico_score')['default'].agg(k='sum', n='count').reset_index()
grouped = grouped.sort_values('fico_score').reset_index(drop=True)

fico_arr = grouped['fico_score'].values
k_arr = grouped['k'].values
n_arr = grouped['n'].values
N = len(fico_arr)

# 2. Dynamic Programming Pre-computation (Prefix Sums for O(1) range queries)
pref_k = np.zeros(N + 1, dtype=int)
pref_n = np.zeros(N + 1, dtype=int)

for i in range(N):
    pref_k[i+1] = pref_k[i] + k_arr[i]
    pref_n[i+1] = pref_n[i] + n_arr[i]

# 3. Define the Objective Function: Log-Likelihood
def log_likelihood(i, j):
    """
    Calculates the Log-Likelihood of a bucket containing FICO indices from i to j.
    LL = k * ln(p) + (n - k) * ln(1 - p)
    """
    n_val = pref_n[j+1] - pref_n[i]
    k_val = pref_k[j+1] - pref_k[i]
    
    if n_val == 0:
        return 0.0
    
    p = k_val / n_val
    
    ll = 0.0
    # Avoid log(0) errors if probability is exactly 0 or 1
    if p > 0:
        ll += k_val * np.log(p)
    if p < 1:
        ll += (n_val - k_val) * np.log(1 - p)
        
    return ll

# 4. Initialize Dynamic Programming Tables
num_buckets = 10

# dp[b][i] stores the max log-likelihood for the first 'i' FICO scores using 'b' buckets
dp = np.full((num_buckets + 1, N + 1), -np.inf)
dp[0][0] = 0.0

# backtrack table to reconstruct the optimal boundaries at the end
backtrack = np.zeros((num_buckets + 1, N + 1), dtype=int)

# 5. Execute Dynamic Programming Algorithm
for b in range(1, num_buckets + 1):
    for i in range(b, N + 1):       # i is the end of the current bucket
        for j in range(b - 1, i):   # j is the start of the current bucket
            cost = log_likelihood(j, i - 1)
            # If this cut improves the likelihood, save it
            if dp[b-1][j] + cost > dp[b][i]:
                dp[b][i] = dp[b-1][j] + cost
                backtrack[b][i] = j

# 6. Reconstruct the Optimal Boundaries
boundaries_idx = []
curr = N
for b in range(num_buckets, 0, -1):
    curr = backtrack[b][curr]
    boundaries_idx.append(curr)
boundaries_idx.reverse()

# --- EVALUATION AND RESULTS ---
print("--- Optimal FICO Buckets (Log-Likelihood Maximization) ---")
print("Mapping FICO scores to Rating Categories (1 = Worst PD, 10 = Best PD)\n")

for i in range(len(boundaries_idx)):
    start_idx = boundaries_idx[i]
    end_idx = boundaries_idx[i+1]-1 if i+1 < len(boundaries_idx) else N-1
    
    start_fico = fico_arr[start_idx]
    end_fico = fico_arr[end_idx]
    n_b = pref_n[end_idx+1] - pref_n[start_idx]
    k_b = pref_k[end_idx+1] - pref_k[start_idx]
    p_b = k_b / n_b if n_b > 0 else 0
    
    rating = 10 - i  # Lower rating = better credit score
    print(f"Rating {rating} | FICO Range: {start_fico:3d} to {end_fico:3d} | Defaults: {k_b:4d} / {n_b:4d} | Probability of Default: {p_b:.2%}")
