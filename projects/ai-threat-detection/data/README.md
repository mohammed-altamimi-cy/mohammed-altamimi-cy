# Data

The dataset is not stored in this repository.

1. Download **UNSW-NB15** from the [UNSW Canberra Cyber site](https://research.unsw.edu.au/projects/unsw-nb15-dataset) (the `UNSW_NB15_testing-set.csv` partition, 82,332 records).
2. Preprocess it (categorical encoding and standard scaling of numeric features; `attack_ttp` mapped from `attack_cat`) and save it here as `UNSW-NB15-processed.csv`.
3. Optional: save the MITRE ATT&CK Enterprise bundle as `enterprise-attack.json` for technique lookups ([attack-stix-data](https://github.com/mitre-attack/attack-stix-data)).
