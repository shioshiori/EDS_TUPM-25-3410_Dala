import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# CREATE OUTPUT FOLDERS

os.makedirs("outputs", exist_ok=True)

# LOAD DATASETS

p1_gen = pd.read_csv("data/Plant_1_Generation_Data.csv")
p1_weather = pd.read_csv("data/Plant_1_Weather_Sensor_Data.csv")

p2_gen = pd.read_csv("data/Plant_2_Generation_Data.csv")
p2_weather = pd.read_csv("data/Plant_2_Weather_Sensor_Data.csv")

# RENAME SOURCE KEY TO PREVENT EMPTY MERGE

p1_weather = p1_weather.drop(columns=["SOURCE_KEY"])
p2_weather = p2_weather.drop(columns=["SOURCE_KEY"])

# MERGE DATASETS

plant1 = pd.merge(
    p1_gen,
    p1_weather,
    on=["DATE_TIME", "PLANT_ID"],
    how="inner"
)

plant2 = pd.merge(
    p2_gen,
    p2_weather,
    on=["DATE_TIME", "PLANT_ID"],
    how="inner"
)

# COMBINE BOTH PLANTS

df = pd.concat([plant1, plant2], ignore_index=True)

# CHECK DATASET

print("RAW DATASET SHAPE:")
print(df.shape)

if df.empty:
    raise ValueError("Merged dataframe is empty.")

# CLEANING

original_rows = len(df)

df["DATE_TIME"] = pd.to_datetime(
    df["DATE_TIME"],
    errors="coerce"
)

num_cols = [
    "DC_POWER",
    "AC_POWER",
    "DAILY_YIELD",
    "TOTAL_YIELD",
    "AMBIENT_TEMPERATURE",
    "MODULE_TEMPERATURE",
    "IRRADIATION"
]

# CONVERT NUMERIC

for col in num_cols:
    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

# COUNT MISSING VALUES

missing_filled = df[num_cols].isna().sum().sum()

# FILL MISSING VALUES

for col in num_cols:
    mean_value = df[col].mean()
    df[col] = df[col].fillna(mean_value)

# REMOVE INVALID DATETIME

df = df.dropna(subset=["DATE_TIME"])

# REMOVE DUPLICATES

before_duplicates = len(df)

df = df.drop_duplicates()

duplicates_removed = before_duplicates - len(df)

# SORT VALUES

df = df.sort_values("DATE_TIME")

# RESET INDEX

df = df.reset_index(drop=True)

print("\nCLEANED DATASET SHAPE:")
print(df.shape)

# CLEANING SUMMARY TABLE

cleaning_summary = pd.DataFrame({
    "Process": [
        "Original Rows",
        "Rows After Cleaning",
        "Duplicates Removed",
        "Missing Values Filled"
    ],
    "Result": [
        original_rows,
        len(df),
        duplicates_removed,
        missing_filled
    ]
})

print("\nTABLE 5.1 CLEANING SUMMARY")
print(cleaning_summary)

cleaning_summary.to_csv(
    "outputs/table_5_1_cleaning_summary.csv",
    index=False
)

# DESCRIPTIVE STATISTICS

stats = df.groupby("PLANT_ID")[num_cols].agg([
    "mean",
    "median",
    "std",
    "var"
])

stats = stats.round(2)

print("\nTABLE 5.2 DESCRIPTIVE STATISTICS")
print(stats)

stats.to_csv(
    "outputs/table_5_2_descriptive_statistics.csv"
)

# CORRELATION ANALYSIS

corr = df[num_cols].corr()

corr = corr.round(2)

print("\nTABLE 5.3 CORRELATION MATRIX")
print(corr)

corr.to_csv(
    "outputs/table_5_3_correlation_matrix.csv"
)

# STATIC VISUALIZATION 1
# DC POWER OVER TIME

plt.figure(figsize=(10, 5))

for plant in df["PLANT_ID"].unique():

    temp = df[df["PLANT_ID"] == plant]

    plt.plot(
        temp["DATE_TIME"],
        temp["DC_POWER"],
        label=f"Plant {plant}"
    )

plt.title("DC Power Over Time")
plt.xlabel("Date Time")
plt.ylabel("DC Power")

plt.legend()

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "outputs/figure_5_1_dc_power_over_time.png"
)

plt.close()

# STATIC VISUALIZATION 2
# IRRADIATION HISTOGRAM

plt.figure(figsize=(8, 5))

plt.hist(
    df["IRRADIATION"],
    bins=30
)

plt.title("Distribution of Solar Irradiation")
plt.xlabel("Irradiation")
plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig(
    "outputs/figure_5_2_irradiation_histogram.png"
)

plt.close()

# STATIC VISUALIZATION 3
# TEMPERATURE VS POWER

plt.figure(figsize=(8, 5))

plt.scatter(
    df["MODULE_TEMPERATURE"],
    df["DC_POWER"],
    alpha=0.5
)

plt.title("Module Temperature vs DC Power")
plt.xlabel("Module Temperature")
plt.ylabel("DC Power")

plt.tight_layout()

plt.savefig(
    "outputs/figure_5_3_temperature_vs_power.png"
)

plt.close()

# STATIC VISUALIZATION 4
# CORRELATION HEATMAP

plt.figure(figsize=(10, 8))

heatmap = plt.imshow(
    corr.values,
    interpolation="nearest"
)

plt.colorbar(heatmap)

plt.xticks(
    range(len(num_cols)),
    num_cols,
    rotation=90
)

plt.yticks(
    range(len(num_cols)),
    num_cols
)

plt.title("Correlation Heatmap")

plt.tight_layout()

plt.savefig(
    "outputs/figure_5_4_correlation_heatmap.png"
)

plt.close()

# ANIMATION

fig, ax = plt.subplots(figsize=(10, 5))

plants = df["PLANT_ID"].unique()

y_min = df["DC_POWER"].min()
y_max = df["DC_POWER"].max()

if not np.isfinite(y_min):
    y_min = 0

if not np.isfinite(y_max):
    y_max = 1

ax.set_xlim(0, 200)
ax.set_ylim(y_min, y_max)

ax.set_title("Animated DC Power Trend")
ax.set_xlabel("Time Index")
ax.set_ylabel("DC Power")

lines = {}

x_data = {}
y_data = {}

for plant in plants:

    line, = ax.plot([], [], label=f"Plant {plant}")

    lines[plant] = line

    x_data[plant] = []
    y_data[plant] = []

ax.legend()

plant_data = {}

for plant in plants:

    temp = df[df["PLANT_ID"] == plant]

    temp = temp.reset_index(drop=True)

    plant_data[plant] = temp

min_frames = min(
    len(plant_data[p])
    for p in plants
)

frames_to_use = min(min_frames, 200)

def update(frame):

    for plant in plants:

        temp = plant_data[plant]

        x_data[plant].append(frame)

        y_data[plant].append(
            temp["DC_POWER"].iloc[frame]
        )

        lines[plant].set_data(
            x_data[plant],
            y_data[plant]
        )

    return list(lines.values())

ani = animation.FuncAnimation(
    fig,
    update,
    frames=frames_to_use,
    interval=50,
    blit=False
)

ani.save(
    "outputs/animated_dc_power.gif",
    writer="pillow"
)

plt.close()

# SNAPSHOTS

plants = df["PLANT_ID"].unique()

if len(plants) > 0:

    plant_id = plants[0]

    plant_data = df[
        df["PLANT_ID"] == plant_id
    ].reset_index(drop=True)

    max_len = len(plant_data)

    if max_len > 0:

        frames = [
            int(max_len * 0.25),
            int(max_len * 0.50),
            int(max_len * 0.75)
        ]

        for i, f in enumerate(frames):

            plt.figure(figsize=(10, 5))

            plt.plot(
                plant_data["DATE_TIME"].iloc[:f],
                plant_data["DC_POWER"].iloc[:f]
            )

            plt.title(
                f"Snapshot {i+1}"
            )

            plt.xlabel("Time")
            plt.ylabel("DC Power")

            plt.xticks(rotation=45)

            plt.tight_layout()

            plt.savefig(
                f"outputs/figure_5_5_snapshot_{i+1}.png"
            )

            plt.close()

print("\nALL OUTPUTS GENERATED SUCCESSFULLY")