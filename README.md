# Benchmarking Continual Knowledge Graph Embedding with Pattern Shifts
### Dataset
```
FACT*
├── FACT-3_2
├── FACT-4_1
├── FACT-3_1_1

PS-CKGE
├── PS-CKGE-3_2
├── PS-CKGE-4_1
├── PS-CKGE-3_1_1
```
We restructured the FACT dataset and refer to it as FACT*. For both FACT* and our dataset, we set up three dynamic scenarios with data ratios of 3:2, 4:1 and 3:1:1 respectively.
### Generation of PS-CKGE

```sh
python construct_1_update.py --instance_name <instance_file> --data_name <dataset_name> --ratio <data_ratio>

```
```sh
python construct_2_update.py --instance_name <instance_file> --data_name <dataset_name>

```
In our experiments, the two Python files above are used to construct datasets for the single-update and double-update scenarios, respectively. `<instance_file>` represents the file name of the rule instances. The instances we provide are generated based on rules of length 2 extracted using NCRL on the FB15K-237 dataset (including train, valid and test). The file is named `FB15k-237_merge_50_2_instance.txt`. `<dataset_name>` represents the name of the dataset folder you want to create. Inside this folder, you should create subfolders named `0`, `1` and `2` (taking a three-phase update as an example). `<data_ratio>` represents the ratio of the number of triples in the initial snapshot and the number of newly added triples during each update which can be set to `4:1` or `3:2`.
### Reproduction of experimental results
To reproduce the experimental results of CKGE method LKGE, the souce code of [LKGE](https://github.com/nju-websoft/LKGE) can be directly used.
