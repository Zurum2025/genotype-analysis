# 🧬 Genotype-Based Hematological Analysis with ANOVA and Pairwise T-Tests

## 📌 Project Overview

This project performs comprehensive statistical analysis on hematological parameters across different genotypes (**AA, AS, SS**).

It implements a complete statistical pipeline that includes:

* Descriptive statistics (**mean ± standard deviation**)
* One-Way ANOVA (**F-value and P-value**)
* Automatic **pairwise independent t-tests** between genotype groups

The output is structured into clean, publication-ready tables suitable for academic research and reports.

---

## ⚙️ Features

* Automated computation of **mean ± standard deviation**
* Performs **One-Way ANOVA** across all genotype groups
* Automatically generates **pairwise t-tests**:

  * AA vs AS
  * AA vs SS
  * AS vs SS
* Uses **Welch’s t-test** (robust to unequal variances)
* Handles missing or incomplete genotype groups gracefully
* Produces structured outputs ready for export or reporting

---

## 🧪 Parameters Analyzed

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

The dataset is loaded from a CSV file using **pandas**.

### 2. Grouping

Data is grouped based on genotype:

* AA
* AS
* SS

### 3. Descriptive Statistics

For each parameter and genotype:

* Mean and standard deviation are computed
* Results are formatted as: **mean ± standard deviation**

### 4. One-Way ANOVA

* Conducted across all available genotype groups
* Tests the null hypothesis that all group means are equal

### 5. Pairwise T-Tests

* Automatically performed for all genotype combinations
* Uses **independent two-sample t-test (Welch’s correction)**
* Identifies where specific differences occur between groups

---

## 📈 Statistical Interpretation

### ANOVA

* **F-value**: Measures variance between group means
* **P-value**:

  * p < 0.05 → Statistically significant difference exists
  * p ≥ 0.05 → No significant difference

### T-Test

* **T-value**: Magnitude and direction of difference between two groups
* **P-value**:

  * p < 0.05 → Significant difference between the two groups
  * p ≥ 0.05 → No significant difference

> ⚠️ Note: Multiple pairwise comparisons may increase Type I error.
> Consider applying correction methods (e.g., Bonferroni) for rigorous studies.

---

## 🛠️ Installation

```bash
pip install pandas scipy
```

---

## 🚀 Usage

```python
from analysis import full_statistical_analysis

results = full_statistical_analysis("data.csv")

# ANOVA results
print(results["ANOVA"])

# Pairwise t-tests
for name, table in results["T-TESTS"].items():
    print(f"\n{name}")
    print(table)
```

---

## 📂 Output Structure

### 1. ANOVA Table

| Parameters | AA           | AS           | SS          | F-value | P-value |
| ---------- | ------------ | ------------ | ----------- | ------- | ------- |
| Hb         | 13.50 ± 1.20 | 13.14 ± 1.17 | 8.12 ± 0.51 | 8.2345  | 0.0012  |

---

### 2. Pairwise T-Test Tables

Each comparison (e.g., **AA_vs_SS**) produces:

| Parameters | Group 1      | Group 2     | T-test | P-value |
| ---------- | ------------ | ----------- | ------ | ------- |
| Hb         | 13.50 ± 1.20 | 9.80 ± 1.50 | -17.81 | 0.0000  |

---

## 📦 Dependencies

* pandas
* scipy

---

## 🎯 Use Cases

* Medical and clinical research
* Hematological data analysis
* Academic and final year projects
* Statistical comparison of grouped datasets

---

## 👤 Author

Chizurum Chiemela

---

## 📄 License

This project is intended for educational and research purposes.
