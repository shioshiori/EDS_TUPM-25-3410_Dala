# Solar Photovoltaic Engineering Data Analytics Pipeline

## Project Overview

This project presents a Python-based engineering data analytics pipeline for the statistical analysis and visualization of solar photovoltaic (PV) power generation data. The system processes solar generation datasets and weather sensor datasets from multiple photovoltaic plants to evaluate relationships between environmental variables and power output.

The pipeline performs automated data ingestion, preprocessing, statistical analysis, correlation modeling, visualization, animation generation, and snapshot extraction using Python numerical and visualization libraries.

---

## Objectives

The project aims to:

1. Analyze the statistical properties of solar photovoltaic datasets.
2. Evaluate relationships between environmental conditions and solar power generation.
3. Generate static and animated visualizations for engineering interpretation.
4. Demonstrate a modular Python-based data analytics workflow.

---

## Features

* Data ingestion and merging
* Missing value handling
* Duplicate removal
* Statistical analysis
* Correlation analysis
* Histogram visualization
* Scatter plot visualization
* Heatmap generation
* Time-series visualization
* Animated DC power trend generation
* Freeze-frame snapshot extraction

---

## Dataset Files

Place the following CSV files inside the `data/` folder:

* `Plant_1_Generation_Data.csv`
* `Plant_1_Weather_Sensor_Data.csv`
* `Plant_2_Generation_Data.csv`
* `Plant_2_Weather_Sensor_Data.csv`

---

## Required Libraries

Install dependencies using:

```bash
pip install -r requirements.txt
```

Required libraries:

* pandas
* numpy
* matplotlib
* pillow
* plotly
* seaborn

---

## Project Structure

```text
project_folder/
│
├── data/
│   ├── Plant_1_Generation_Data.csv
│   ├── Plant_1_Weather_Sensor_Data.csv
│   ├── Plant_2_Generation_Data.csv
│   └── Plant_2_Weather_Sensor_Data.csv
│
├── outputs/
│
├── main.py
├── requirements.txt
└── README.md
```

---

## Running the Project

Run the pipeline using:

```bash
python main.py
```

or inside Jupyter Notebook:

```python
run main.py
```

---

## Generated Outputs

The program automatically generates:

### Tables

* Cleaning Summary Table
* Descriptive Statistics Table
* Correlation Matrix Table

### Figures

* DC Power Over Time
* Irradiation Histogram
* Temperature vs DC Power
* Correlation Heatmap

### Animations

* Animated DC Power Trend

### Snapshots

* Freeze-frame visualizations extracted from the animation

All generated files are saved inside the `outputs/` folder.

---

## Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Plotly
* Seaborn

---

## Researchers
Sandrex Dala

Bachelor of Science in Electronics and Communications Engineering (ECE)

TUPM-25-3410

---

## License

This project is intended for academic and educational purposes only.
