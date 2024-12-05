import random
import argparse

def parse_instance_file(instance_file):
    tp_dict = {}
    with open(instance_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split("\t")
                if len(parts) == 6:
                    relations = parts[5][2:-2].split("', '")
                    for rel_entry in relations:
                        en1, rel, en2 = rel_entry.split("\\t")
                        key = f"{en2}\t{rel[4:]}\t{en1}" if rel.startswith('inv_') else f"{en1}\t{rel}\t{en2}"
                        tp_dict[key] = tp_dict.get(key, 0) + 1
    return tp_dict


def filter_tp_dict(tp_dict, threshold=3):
    return {key: value for key, value in tp_dict.items() if value >= threshold}


def sample_tp(instance_file):
    tp2 = set()
    ins = {}
    with open(instance_file, 'r') as f:
        for line in f:
            conf = float(line.split(' (')[0])
            ins[line.strip()] = conf
    sorted_ins = dict(sorted(ins.items(), key=lambda x: x[1], reverse=True))

    for instance in sorted_ins:
        parts = instance.split("\t")
        n = random.randint(0, 1)
        if n == 1:
            if parts[2].startswith('inv_'):
                tp2.add(f"{parts[3]}\t{parts[2][4:]}\t{parts[1]}")
            else:
                tp2.add(f"{parts[1]}\t{parts[2]}\t{parts[3]}")
        body = parts[5][2:-2].split("', '")
        for body_entry in body:
            en1, rel, en2 = body_entry.split("\\t")
            key = f"{en2}\t{rel[4:]}\t{en1}" if rel.startswith('inv_') else f"{en1}\t{rel}\t{en2}"
            tp2.add(key)
    return tp2

def tp_new_ent(tp, entities_count=8812,top_n=2600, sample_num=645):
    ent = set()
    for line in tp:
        ent.add(line.split('\t')[0])
        ent.add(line.split('\t')[2])
    tp = list(tp)
    ent_sel = random.sample(ent, entities_count)
    keys_list = set()
    for line in tp:
        if line.strip().split('\t')[0] in ent_sel and line.strip().split('\t')[2] in ent_sel:
            keys_list.add(line.strip())

    tp_all = []
    with open('../data/FB15k-237/train.txt', 'r') as f:
        for line in f:
            tp_all.append(line.strip())
    with open('../data/FB15k-237/test.txt', 'r') as f:
        for line in f:
            tp_all.append(line.strip())
    with open('../data/FB15k-237/valid.txt', 'r') as f:
        for line in f:
            tp_all.append(line.strip())

    ent_stat = {}
    for line in tp_all:
        parts = line.strip().split('\t')
        if parts[0] in ent_sel:
            if parts[0] in ent_stat:
                ent_stat[parts[0]] += 1
            else:
                ent_stat[parts[0]] = 1
        if parts[2] in ent_sel:
            if parts[2] in ent_stat:
                ent_stat[parts[2]] += 1
            else:
                ent_stat[parts[2]] = 1
    ent_sorted_dict = dict(sorted(ent_stat.items(), key=lambda x: x[1]))
    ent_sorted = list(ent_sorted_dict.keys())[:top_n]
    new_ent = random.sample(ent_sorted, sample_num)

    tp_has_new_ent = []
    for line in tp_all:
        parts = line.strip().split('\t')
        if parts[0] in new_ent or parts[2] in new_ent:
            tp_has_new_ent.append(line.strip())

    tp_has_ent = []
    for line in tp_all:
        parts = line.strip().split('\t')
        if parts[0] in ent_sel and parts[2] in ent_sel:
            tp_has_ent.append(line.strip())

    keys_list = set(tp_has_new_ent).union(set(keys_list))
    tp_remain = set(tp_has_ent) - set(keys_list)
    tp_random = random.sample(tp_remain, 62023 * 2 - len(keys_list))
    tp_s1 = set(tp_random).union(set(keys_list))

    s1 = tp_s1
    s0 = set(tp_all) - set(s1)

    r_final = set()
    e_final = set()
    for line in s0:
        parts = line.strip().split('\t')
        r_final.add(parts[1])
        e_final.add(parts[0])
        e_final.add(parts[2])

    all_rel = set()
    with open("../data/FB15k-237/relations.dict", 'r') as f:
        for line in f:
            all_rel.add(line.strip().split('\t')[1])
    n_rel = all_rel - r_final

    add_s0_rel = []
    for line in s1:
        if line.split('\t')[1] in n_rel:
            add_s0_rel.append(line)

    add_s0 = random.sample(add_s0_rel, int(len(add_s0_rel) * 0.6))
    s1_new = set(s1) - set(add_s0)
    add_s1 = random.sample(s0, int(len(add_s0_rel) * 0.6))
    s1_new = set(s1_new).union(set(add_s1))
    s0_new = set(tp_all) - set(s1_new)

    r_final = set()
    e_final = set()
    for line in s0_new:
        parts = line.strip().split('\t')
        r_final.add(parts[1])
        e_final.add(parts[0])
        e_final.add(parts[2])

    all_ent = set()
    with open("../data/FB15k-237/entities.dict", 'r') as f:
        for line in f:
            all_ent.add(line.strip().split('\t')[1])
    return s0_new, s1_new

def split_data(s0,s1,data_name):
    rel_dict = set()
    ent_dict = set()
    train = random.sample(s0, int(len(s0) * 3 / 5))
    for line in train:
        parts = line.strip().split('\t')
        rel_dict.add(parts[1])
        ent_dict.add(parts[0])
        ent_dict.add(parts[2])

    ent = set()
    rel = set()
    for tp in s0:
        parts = tp.strip().split('\t')
        ent.add(parts[0])
        ent.add(parts[2])
        rel.add(parts[1])

    ent_miss = [e for e in ent if e not in ent_dict]
    rel_miss = [r for r in rel if r not in rel_dict]

    tp_miss = []
    for tp in s0:
        parts = tp.strip().split('\t')
        if parts[0] in ent_miss or parts[2] in ent_miss:
            tp_miss.append(tp.strip())
        if parts[1] in rel_miss:
            tp_miss.append(tp.strip())

    while (1):
        train1 = train + tp_miss
        rel_dict = set()
        ent_dict = set()
        for tp in train1:
            parts = tp.strip().split('\t')
            rel_dict.add(parts[1])
            ent_dict.add(parts[0])
            ent_dict.add(parts[2])
        if len(ent_dict) == len(ent) and len(rel_dict) == len(rel):
            train = train1
            break
    remain = [t for t in s0 if t not in train]
    random.shuffle(remain)
    valid = remain[:int(len(s0) / 5)]
    test = remain[int(len(s0) / 5):]


    with open('../data/{}/0/train.txt'.format(data_name), 'w') as f:
        for tp in train:
            f.write(tp + '\n')
    with open('../data/{}/0/valid.txt'.format(data_name), 'w') as f:
        for tp in valid:
            f.write(tp + '\n')
    with open('../data/{}/0/test.txt'.format(data_name), 'w') as f:
        for tp in test:
            f.write(tp + '\n')

    ent = set()
    with open('../data/{}/0/train.txt'.format(data_name), 'r') as f:
        for line in f:
            ent.add(line.strip().split('\t')[0])
            ent.add(line.strip().split('\t')[2])
    all_ent = set()
    with open("../data/FB15k-237/entities.dict", 'r') as f:
        for line in f:
            all_ent.add(line.strip().split('\t')[1])
    new_ent = all_ent - ent

    rel_dict = set()
    ent_dict = set()
    train = random.sample(s1, int(len(s1) * 3 / 5))
    for line in train:
        parts = line.strip().split('\t')
        rel_dict.add(parts[1])
        ent_dict.add(parts[0])
        ent_dict.add(parts[2])
    ent_miss = [e for e in new_ent if e not in ent_dict]

    tp_miss = []
    for tp in s1:
        parts = tp.strip().split('\t')
        if parts[0] in ent_miss or parts[2] in ent_miss:
            tp_miss.append(tp.strip())
    while (1):
        to_del = random.sample(train, len(tp_miss))
        train1 = [t for t in train if t not in to_del]
        train1 = train1 + tp_miss
        rel_dict = set()
        ent_dict = set()
        for tp in train1:
            parts = tp.strip().split('\t')
            rel_dict.add(parts[1])
            ent_dict.add(parts[0])
            ent_dict.add(parts[2])
        if ent_dict.intersection(new_ent) == new_ent:
            train = train1
            break

    remain = [t for t in s1 if t not in train]
    random.shuffle(remain)
    valid = remain[:int(len(s1) / 5)]
    test = remain[int(len(s1) / 5):]


    with open('../data/{}/1/train.txt'.format(data_name), 'w') as f:
        for tp in train:
            f.write(tp + '\n')
    with open('../data/{}/1/valid.txt'.format(data_name), 'w') as f:
        for tp in valid:
            f.write(tp + '\n')
    with open('../data/{}/1/test.txt'.format(data_name), 'w') as f:
        for tp in test:
            f.write(tp + '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--instance_file', type=str, help="File name of rule instances")
    parser.add_argument('--data_name', type=str, help="Dataset name")
    args = parser.parse_args()
    instance_file = args.instance_file
    data_name = args.data_name
    tp_dict = parse_instance_file(instance_file)

    new_dict = filter_tp_dict(tp_dict, threshold=3)
    tp1 = list(new_dict.keys())
    tp2 = sample_tp(instance_file)
    tp = set(tp1).union(tp2)

    s0, s1 = tp_new_ent(tp)

    split_data(s0,s1,data_name)


if __name__ == "__main__":
    main()

