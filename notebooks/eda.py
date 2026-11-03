import pandas as pd

df = pd.read_csv("data/raw/cs-training.csv")
print(df.shape)
print(df.head())

print(df.info())
print(df.isnull().sum())
print(df["SeriousDlqin2yrs"].value_counts(normalize=True))

print(df["age"].describe())
print(df["DebtRatio"].describe())
print(df["NumberOfTimes90DaysLate"].max())
print(df["NumberOfDependents"].isnull().sum())