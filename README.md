# Benchmarking Continual Knowledge Graph Embedding with Pattern Shifts
### Dataset


```
FACT
├── FACT-3_2
├── FACT-4_1
├── FACT-3_1_1

PS-CKGE
├── PS-CKGE-3_2
├── PS-CKGE-4_1
├── PS-CKGE-3_1_1


```
### Generation process

```sh
python split_3_2.py --instance_name <instance_file> --data_name <dataset_name>

```
```sh
python split_4_1.py --instance_name <instance_file> --data_name <dataset_name>

```
```sh
python split_3_1_1.py --instance_name <instance_file> --data_name <dataset_name>

```
In our experiment, the three Python files each represent different dynamic scenarios.`<dataset_name>` represents the name of the dataset folder you want to create. Inside this folder, you should create subfolders named `0`, `1`  and `2` (taking a three-phase update as an example).`<instance_file>` we provide is generated based on rules of length 2 extracted using NCRL on the FB15K-237 dataset (including train, valid and test). The file is named `FB15k-237_merge_50_2_instance.txt`.


