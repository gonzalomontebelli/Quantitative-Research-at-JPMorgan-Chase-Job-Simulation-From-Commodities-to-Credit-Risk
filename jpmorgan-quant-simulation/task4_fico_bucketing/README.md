# Task 4 — Optimal FICO Score Bucketing (Dynamic Programming)

## Objective

Find the optimal boundaries to segment FICO scores into 10 rating categories (1 = worst credit, 10 = best credit), maximizing the total Log-Likelihood of the model.

## Algorithm

**Dynamic Programming** with Prefix Sums for O(1) range queries:

```
dp[b][i] = max { dp[b-1][j] + LL(j, i-1) }  for all j < i
```

Where `LL(i, j)` is the log-likelihood of the bucket containing FICO scores between indices `i` and `j`.

## Complexity

- Time: O(N² × B) where N = unique FICO scores, B = number of buckets
- Space: O(N × B)

## Sample Output

```
Rating 10 | FICO Range: 740 to 850 | PD:  4.20%
Rating  9 | FICO Range: 720 to 739 | PD:  6.80%
...
Rating  1 | FICO Range: 550 to 599 | PD: 33.50%
```

## Required Data

`Task 3 and 4_Loan_Data.csv` in the working directory.
