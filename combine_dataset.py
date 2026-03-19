import pandas as pd
import glob

files = glob.glob("MachineLearningCVE.csv")

df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)

df.to_csv("combined_dataset.csv", index=False)

print("Dataset combined")
