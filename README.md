# 🧬 Genotype-Based Hematological Analysis with ANOVA

## Project Overview

This project performs statistical analysis on hematological parameters across different genotypes (**AA, AS, SS**). It computes:

* Mean and Standard Deviation
* One-Way ANOVA (F-value and P-value)

The output is a well-structured table suitable for academic reports and research work.

---

## Features

* Automated calculation of **mean ± standard deviation**
* Performs **One-Way ANOVA** for each parameter
* Handles missing genotype groups gracefully
* Outputs clean, publication-ready tables

---

## Parameters Analyzed

* Hemoglobin (Hb)
* Packed Cell Volume (PCV)
* Mean Corpuscular Volume (MCV)
* Mean Corpuscular Hemoglobin (MCH)
* Mean Corpuscular Hemoglobin Concentration (MCHC)
* Red Blood Cell Count (RBC)
* Total White Blood Cell Count (TWBC)
* Platelet Count

---

## 📊 Methodology

### 1. Data Loading

Dataset is loaded using Pandas.

### 2. Grouping

Data is grouped by genotype:

* AA
* AS
* SS

### 3. Statistical Analysis

* Mean and standard deviation computed for each group
* One-way ANOVA performed using SciPy

---

## 📈 ANOVA Interpretation

* **F-value**: Measures variance between groups
* **P-value**:

  * p < 0.05 → Significant difference
  * p ≥ 0.05 → No significant difference

---

## 🛠️ Installation

```bash
pip install pandas scipy
```

---

## Usage

```python
from analysis import genotype_analysis

result = genotype_analysis("data.csv")
print(result)
```

---

## Example Output

| Parameters | AA           | AS           | SS          | F-value | P-value |
| ---------- | ------------ | ------------ | ----------- | ------- | ------- |
| Hb         | 13.50 ± 1.20 | 12.30 ± 1.10 | 9.80 ± 1.50 | 8.2345  | 0.0012  |

---

## Dependencies

* pandas
* scipy

---

## Use Cases

* Medical research
* Academic projects
* Hematological data analysis
* Final year projects 

---

## Author

Chizurum Chiemela

---