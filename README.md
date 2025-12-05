# Data-Center Energy Use in the AI Era

This project provides a simple, transparent model of global **data-center electricity consumption** and **CO₂ emissions**, with a focus on how rapidly growing **AI workloads** influence total energy demand. The goal is not to produce a precise forecast, but to create a **clear visual narrative** suitable for presentations, academic work, and exploratory analysis.

---

## 📁 Repository Contents

| File / Folder | Description |
|---------------|-------------|
| `DataCenter_AI_Energy.ipynb` | Main Jupyter Notebook containing code, analysis, and visualizations. |
| `data_center_ai_raw.csv` | Raw dataset used by the notebook (energy, AI share, emissions inputs). |
| `figures/` | Folder where generated PNG charts are saved. |
| `README.md` | Documentation and instructions for running the project. |

---

## 🧰 Requirements

This project requires **Python 3.7+** and the following libraries:

- `numpy`
- `pandas`
- `matplotlib`
- `notebook` (to run Jupyter)

Install everything with:

```
pip install -r requirements.txt
```

---

## 🖥️ How to Run the Python Script (.py)

### 1. Navigate to the project folder

```
cd data-center-ai-energy
```

### 2. Run the script

```
python data_center_ai_energy.py
```

### This will automatically:

- Load historical + projected energy data  
- Calculate carbon intensities and emissions  
- Compute AI vs non-AI energy use  
- Generate and save figures to the `figures/` folder  
