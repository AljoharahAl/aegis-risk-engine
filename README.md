# Aegis Risk Engine

End-to-end machine learning system that predicts the probability of a borrower
defaulting within two years, based on the Give Me Some Credit dataset (150K records).

## Project Status
- [x] Exploratory data analysis
- [ ] Database design
- [ ] Preprocessing pipeline
- [ ] Modeling
- [ ] API and deployment

## Dataset
Public dataset from the Kaggle competition "Give Me Some Credit":
historical credit data on 150,000 borrowers. The target is `SeriousDlqin2yrs`
(1 = serious delinquency within two years, 0 = none).
The file `cs-training.csv` is not included in the repo. Download it from Kaggle
and place it in `data/raw/`.

## Project Structure
```
data/raw/     raw data (not tracked by Git)
db/           SQL files
notebooks/    exploratory data analysis
src/          source code
```

## Setup
```
pip install -r requirements.txt
```
Then open `notebooks/eda.aegis_risk_engine.ipynb` and run all cells.

## Key Findings from EDA
- Only 6.7% of borrowers defaulted, so accuracy is misleading. ROC-AUC and Recall will be used.
- Default rate drops with age: 11.6% under 30, 2.3% over 70.
- MonthlyIncome is missing for 19.8% of rows.
- 269 rows have 96 or 98 late payments and default at 54.6%.