'''import pandas as pd
import numpy as np

print("Loading dataset...")

# Load combined dataset
df = pd.read_csv("combined_dataset.csv")

print("Dataset loaded successfully")
print("Total columns:", len(df.columns))

# ===============================
# IMPORTANT FEATURES FOR PROJECT
# ===============================

features = [
    "Flow Duration",
    "Total Fwd Packets",
    "Total Backward Packets",
    "Total Length of Fwd Packets",
    "Total Length of Bwd Packets",
    "Flow Bytes/s",
    "Flow Packets/s",
    "Fwd IAT Mean",
    "Bwd IAT Mean",
    "Packet Length Mean",
    "Packet Length Std",
    "SYN Flag Count",
    "ACK Flag Count",
    "RST Flag Count"
]

# Select only required columns
df = df[features]

print("Selected important features")

# ===============================
# DATA CLEANING (VERY IMPORTANT)
# ===============================

# Replace infinite values
df.replace([np.inf, -np.inf], np.nan, inplace=True)

# Fill missing values
df.fillna(0, inplace=True)

print("Data cleaned successfully")

# Save cleaned dataset
df.to_csv("clean_dataset.csv", index=False)

print("Clean dataset saved as clean_dataset.csv")

import pandas as pd
import numpy as np

print("Loading dataset...")

df = pd.read_csv("combined_dataset.csv")

# ⭐ Remove extra spaces from column names
df.columns = df.columns.str.strip()

print("Columns cleaned")
print(df.columns.tolist())

# ===============================
# IMPORTANT FEATURES
# ===============================

features = [
    "Flow Duration",
    "Total Fwd Packets",
    "Total Backward Packets",
    "Total Length of Fwd Packets",
    "Total Length of Bwd Packets",
    "Flow Bytes/s",
    "Flow Packets/s",
    "Fwd IAT Mean",
    "Bwd IAT Mean",
    "Packet Length Mean",
    "Packet Length Std",
    "SYN Flag Count",
    "ACK Flag Count",
    "RST Flag Count"
]

# Select features
df = df[features]

# ===============================
# CLEAN DATA
# ===============================

df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.fillna(0, inplace=True)

df.to_csv("clean_dataset.csv", index=False)

print("Clean dataset saved successfully")'''


import pandas as pd
import numpy as np

print("Loading dataset...")

df = pd.read_csv("combined_dataset.csv")

# Remove extra spaces from column names
df.columns = df.columns.str.strip()

print("Columns cleaned")
print("Available columns:")
print(df.columns.tolist())

# ===============================
# IMPORTANT FEATURES
# ===============================

features = [
    "Flow Duration",
    "Total Fwd Packets",
    "Total Backward Packets",
    "Total Length of Fwd Packets",
    "Total Length of Bwd Packets",
    "Flow Bytes/s",
    "Flow Packets/s",
    "Fwd IAT Mean",
    "Bwd IAT Mean",
    "Packet Length Mean",
    "Packet Length Std",
    "SYN Flag Count",
    "ACK Flag Count",
    "RST Flag Count"
]

# ===============================
# SAFE FEATURE SELECTION
# ===============================

# Check which features exist
available_features = [f for f in features if f in df.columns]
missing_features = [f for f in features if f not in df.columns]

print("\nAvailable selected features:", available_features)

if missing_features:
    print("\nWARNING: Missing features detected:")
    print(missing_features)

# Select only available columns (prevents crash)
df = df[available_features]

# ===============================
# CLEAN DATA
# ===============================

df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.fillna(0, inplace=True)

# Save clean dataset
df.to_csv("clean_dataset.csv", index=False)

print("\nClean dataset saved successfully")
print("Final shape:", df.shape)

