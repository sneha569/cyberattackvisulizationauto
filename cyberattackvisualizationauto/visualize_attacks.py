import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog

# Hide tkinter window
Tk().withdraw()

# Select file
file_path = filedialog.askopenfilename(
    title="Select Firewall Log File",
    filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")]
)

if not file_path:
    print("No file selected")
    exit()

# Read file dynamically
if file_path.endswith(".csv"):
    df = pd.read_csv(file_path)
elif file_path.endswith(".xlsx"):
    df = pd.read_excel(file_path)
else:
    print("Unsupported file format")
    exit()

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# ---- ANALYSIS ----
action_counts = df['action'].value_counts()
attack_counts = df['attack_type'].value_counts()
top_ips = df[df['action'] == 'DENY']['ip'].value_counts().head(5)
time_trend = df.groupby(df['timestamp'].dt.hour).size()

# ---- VISUALIZATION ----
plt.figure(figsize=(14, 10))

# 1️⃣ ALLOW vs DENY
plt.subplot(2, 2, 1)
bars = plt.bar(action_counts.index, action_counts.values)
plt.title("ALLOW vs DENY Traffic")
for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2,
             bar.get_height(),
             int(bar.get_height()),
             ha='center', va='bottom')

# 2️⃣ Attack Type Pie
plt.subplot(2, 2, 2)
plt.pie(attack_counts.values, labels=attack_counts.index, autopct='%1.1f%%')
plt.title("Attack Type Distribution")

# 3️⃣ Top 5 DENY IPs
plt.subplot(2, 2, 3)
colors = ['red' if i == 0 else 'blue' for i in range(len(top_ips))]
bars = plt.bar(top_ips.index, top_ips.values, color=colors)
plt.title("Top 5 DENY IPs")
for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2,
             bar.get_height(),
             int(bar.get_height()),
             ha='center', va='bottom')

# 4️⃣ Attacks Over Time
plt.subplot(2, 2, 4)
plt.bar(time_trend.index, time_trend.values)
plt.title("Attack Trend by Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Attacks")

plt.tight_layout()
plt.show()
