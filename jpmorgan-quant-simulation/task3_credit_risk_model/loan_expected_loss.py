import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score

# 1. Load the Loan Data
df = pd.read_csv('Task 3 and 4_Loan_Data.csv')

# 2. Define Features and Target
features = [
    'credit_lines_outstanding', 
    'loan_amt_outstanding', 
    'total_debt_outstanding', 
    'income', 
    'years_employed', 
    'fico_score'
]
X = df[features]
y = df['default']

# Split data for comparative analysis
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ==========================================
# 3. Comparative Analysis (LR vs RF)
# ==========================================

# Model A: Random Forest (Great for non-linear, but harder to interpret)
rf_model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
rf_model.fit(X_train, y_train)
rf_auc = roc_auc_score(y_test, rf_model.predict_proba(X_test)[:, 1])

# Model B: Logistic Regression (Highly interpretable, requires feature scaling)
# We use a Pipeline to ensure data is always scaled before prediction
lr_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('logreg', LogisticRegression(max_iter=1000))
])
lr_pipeline.fit(X_train, y_train)
lr_auc = roc_auc_score(y_test, lr_pipeline.predict_proba(X_test)[:, 1])

print(f"--- Model Comparison (AUC Score) ---")
print(f"Random Forest AUC: {rf_auc:.4f}")
print(f"Logistic Regression AUC: {lr_auc:.4f}\n")

# Given the perfect linearity in the dataset, Logistic Regression is the best fit.
# We will train the final pipeline on the ENTIRE dataset for production.
final_model = Pipeline([
    ('scaler', StandardScaler()),
    ('logreg', LogisticRegression(max_iter=1000))
])
final_model.fit(X, y)

# ==========================================
# 4. Expected Loss Valuation Function
# ==========================================

def calculate_expected_loss(
    credit_lines_outstanding, 
    loan_amt_outstanding, 
    total_debt_outstanding, 
    income, 
    years_employed, 
    fico_score
):
    """
    Calculates the Expected Loss (EL) of a loan based on customer characteristics.
    EL = PD (Probability of Default) * EAD (Exposure at Default) * LGD (Loss Given Default)
    """
    # Create a DataFrame for the single input row
    input_data = pd.DataFrame([[
        credit_lines_outstanding, 
        loan_amt_outstanding, 
        total_debt_outstanding, 
        income, 
        years_employed, 
        fico_score
    ]], columns=features)
    
    # Calculate PD: The probability that the borrower will default (class 1)
    pd_prob = final_model.predict_proba(input_data)[0][1]
    
    # Basel II/III Parameters
    recovery_rate = 0.10
    lgd = 1.0 - recovery_rate      # 90% Loss Given Default
    ead = loan_amt_outstanding     # Exposure at Default
    
    # Calculate Expected Loss
    expected_loss = pd_prob * ead * lgd
    
    return expected_loss, pd_prob

# --- TEST CASE ---
print("--- Retail Risk Valuator ---")

# Example: A high-risk customer (High debt, low income, low FICO, low years employed)
loan_amount = 10000.0
el, pd_prob = calculate_expected_loss(
    credit_lines_outstanding=5,
    loan_amt_outstanding=loan_amount,
    total_debt_outstanding=25000,
    income=35000,
    years_employed=2,
    fico_score=550
)

print(f"Customer Loan Amount (EAD): ${loan_amount:,.2f}")
print(f"Calculated Probability of Default (PD): {pd_prob * 100:.2f}%")
print(f"Expected Loss (EL) to reserve: ${el:,.2f}")
