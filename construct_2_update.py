import random
import argparse
def parse_instance_file(filename, max_lines=None):
    tp_ins = set()
    tp_body = set()
    ent = set()
    tp_dict = {}
    ins = 0
    with open(filename, 'r') as f:
        for line in f:
            ins += 1
            if ins <= max_lines:
                rule_head = line.strip().split('	<--	')[0].split('\t')[1]
                rule_body1 = line.strip().split('	<--	')[1].split('\\t')[1]
                rule_body2 = line.strip().split('	<--	')[1].split('\\t')[3]
                rule = f'{rule_head}\t{rule_body1}\t{rule_body2}'
                line = line.strip()
                if line:
                    parts = line.split("\t")
                    if len(parts) == 6:
                        rule_head = parts[2]
                        relations = parts[5]
                        relations = relations[2:-2].split("', '")
                        relation = []
                        for subpart in relations:
                            relation1 = subpart.split("\\t")[1]
                            relation.append(relation1)
                        output = f'{rule_head} <-- {relation[0]}, {relation[1]}'
                        for subpart1 in relations:
                            en1, rel, en2 = subpart1.split("\\t")
                            ent.add(en1)
                            ent.add(en2)
                            if rel.startswith('inv_'):
                                tp_ins.add(f"{en2}\t{rel[4:]}\t{en1}")
                                if f"{en2}\t{rel[4:]}\t{en1}" in tp_dict:
                                    tp_dict[f"{en2}\t{rel[4:]}\t{en1}"] += 1
                                else:
                                    tp_dict[f"{en2}\t{rel[4:]}\t{en1}"] = 1
                            else:
                                tp_ins.add(f"{en1}\t{rel}\t{en2}")
                                if f"{en1}\t{rel}\t{en2}" in tp_dict:
                                    tp_dict[f"{en1}\t{rel}\t{en2}"] += 1
                                else:
                                    tp_dict[f"{en1}\t{rel}\t{en2}"] = 1
                        ent.add(parts[1])
                        ent.add(parts[3])
                        if parts[2].startswith('inv_'):
                            tp_ins.add(f'{parts[3]}\t{parts[2][4:]}\t{parts[1]}')
                            tp_body.add(f'{parts[3]}\t{parts[2][4:]}\t{parts[1]}')
                            if f'{parts[2]}\t{parts[1][4:]}\t{parts[0]}' in tp_dict:
                                tp_dict[f'{parts[3]}\t{parts[2][4:]}\t{parts[1]}'] += 1
                            else:
                                tp_dict[f'{parts[3]}\t{parts[2][4:]}\t{parts[1]}'] = 1
                        else:
                            tp_ins.add(f'{parts[1]}\t{parts[2]}\t{parts[3]}')
                            tp_body.add(f'{parts[1]}\t{parts[2]}\t{parts[3]}')
                            if f'{parts[0]}\t{parts[1]}\t{parts[2]}' in tp_dict:
                                tp_dict[f'{parts[1]}\t{parts[2]}\t{parts[3]}'] += 1
                            else:
                                tp_dict[f'{parts[1]}\t{parts[2]}\t{parts[3]}'] = 1
    return tp_dict

def filter_tp_dict(tp_dict, threshold=3):
    return {key: value for key, value in tp_dict.items() if value >= threshold}

def sample_tp(instance_file,max_lines=None):
    tp2 = set()
    ins = {}
    with open(instance_file, 'r') as f:
        a = 0
        for line in f:
            a += 1
            if a <= max_lines+1:
                conf = float(line.split(' (')[0])
                ins[line.strip()] = conf
    sorted_dict1 = dict(sorted(ins.items(), key=lambda x: x[1], reverse=True))
    for instance in sorted_dict1:
        parts = instance.split("\t")
        n = random.randint(0, 1)
        if n == 1:
            if parts[2].startswith('inv_'):
                tp2.add(f'{parts[3]}\t{parts[2][4:]}\t{parts[1]}')
            else:
                tp2.add(f'{parts[1]}\t{parts[2]}\t{parts[3]}')
        relations = parts[5]
        relations = relations[2:-2].split("', '")
        en1, rel, en2 = relations[0].split("\\t")
        if rel.startswith('inv_'):
            tp2.add(f"{en2}\t{rel[4:]}\t{en1}")
        else:
            tp2.add(f"{en1}\t{rel}\t{en2}")
        en1, rel, en2 = relations[1].split("\\t")
        if rel.startswith('inv_'):
            tp2.add(f"{en2}\t{rel[4:]}\t{en1}")
        else:
            tp2.add(f"{en1}\t{rel}\t{en2}")
    return tp2
def time_split(tp,tp_dict,filename, max_lines=None,top_n=1500, sample_num=700):
    ent = set()
    for line in tp:
        ent.add(line.split('\t')[0])
        ent.add(line.split('\t')[2])
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

    s0 = set(tp_dict.keys()) - tp

    tp_ins = set()
    tp_body = set()
    ent = set()
    tp_dict = {}
    ins = 0
    with open(filename, 'r') as f:
        for line in f:
            ins += 1
            if ins > max_lines:
                rule_head = line.strip().split('	<--	')[0].split('\t')[1]
                rule_body1 = line.strip().split('	<--	')[1].split('\\t')[1]
                rule_body2 = line.strip().split('	<--	')[1].split('\\t')[3]
                line = line.strip()
                if line:
                    parts = line.split("\t")
                    if len(parts) == 6:
                        relations = parts[5]
                        relations = relations[2:-2].split("', '")
                        relation = []
                        for subpart in relations:
                            relation1 = subpart.split("\\t")[1]
                            relation.append(relation1)
                        for subpart1 in relations:
                            en1, rel, en2 = subpart1.split("\\t")
                            ent.add(en1)
                            ent.add(en2)
                            if rel.startswith('inv_'):
                                tp_ins.add(f"{en2}\t{rel[4:]}\t{en1}")
                                if f"{en2}\t{rel[4:]}\t{en1}" in tp_dict:
                                    tp_dict[f"{en2}\t{rel[4:]}\t{en1}"] += 1
                                else:
                                    tp_dict[f"{en2}\t{rel[4:]}\t{en1}"] = 1
                            else:
                                tp_ins.add(f"{en1}\t{rel}\t{en2}")
                                if f"{en1}\t{rel}\t{en2}" in tp_dict:
                                    tp_dict[f"{en1}\t{rel}\t{en2}"] += 1
                                else:
                                    tp_dict[f"{en1}\t{rel}\t{en2}"] = 1
                        ent.add(parts[1])
                        ent.add(parts[3])
                        if parts[2].startswith('inv_'):
                            tp_ins.add(f'{parts[3]}\t{parts[2][4:]}\t{parts[1]}')
                            tp_body.add(f'{parts[3]}\t{parts[2][4:]}\t{parts[1]}')
                            if f'{parts[2]}\t{parts[1][4:]}\t{parts[0]}' in tp_dict:
                                tp_dict[f'{parts[3]}\t{parts[2][4:]}\t{parts[1]}'] += 1
                            else:
                                tp_dict[f'{parts[3]}\t{parts[2][4:]}\t{parts[1]}'] = 1
                        else:
                            tp_ins.add(f'{parts[1]}\t{parts[2]}\t{parts[3]}')
                            tp_body.add(f'{parts[1]}\t{parts[2]}\t{parts[3]}')
                            if f'{parts[0]}\t{parts[1]}\t{parts[2]}' in tp_dict:
                                tp_dict[f'{parts[1]}\t{parts[2]}\t{parts[3]}'] += 1
                            else:
                                tp_dict[f'{parts[1]}\t{parts[2]}\t{parts[3]}'] = 1
    sorted_dict = dict(sorted(tp_dict.items(), key=lambda x: x[1], reverse=True))
    new_dict = {key: value for key, value in sorted_dict.items() if value >= 3}
    tp1 = list(new_dict.keys())
    tp2 = set()
    ins = {}
    with open(filename, 'r') as f:
        a = 0
        for line in f:
            a += 1
            if a > max_lines:
                conf = float(line.split(' (')[0])
                ins[line.strip()] = conf
    sorted_dict1 = dict(sorted(ins.items(), key=lambda x: x[1], reverse=True))
    for instance in sorted_dict1:
        parts = instance.split("\t")
        n = random.randint(0, 1)
        if n == 1:
            if parts[2].startswith('inv_'):
                tp2.add(f'{parts[3]}\t{parts[2][4:]}\t{parts[1]}')
            else:
                tp2.add(f'{parts[1]}\t{parts[2]}\t{parts[3]}')
        relations = parts[5]
        relations = relations[2:-2].split("', '")
        en1, rel, en2 = relations[0].split("\\t")
        if rel.startswith('inv_'):
            tp2.add(f"{en2}\t{rel[4:]}\t{en1}")
        else:
            tp2.add(f"{en1}\t{rel}\t{en2}")
        en1, rel, en2 = relations[1].split("\\t")
        if rel.startswith('inv_'):
            tp2.add(f"{en2}\t{rel[4:]}\t{en1}")
        else:
            tp2.add(f"{en1}\t{rel}\t{en2}")
    tp1 = set(tp1).union(tp2)

    ent = set()
    for line in tp1:
        ent.add(line.split('\t')[0])
        ent.add(line.split('\t')[2])

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
        # if parts[0] in ent_sel:
        if parts[0] in ent_stat:
            ent_stat[parts[0]] += 1
        else:
            ent_stat[parts[0]] = 1
        # if parts[0] in ent_sel:
        if parts[2] in ent_stat:
            ent_stat[parts[2]] += 1
        else:
            ent_stat[parts[2]] = 1
    ent_sorted_dict = dict(sorted(ent_stat.items(), key=lambda x: x[1]))
    ent_sorted = list(ent_sorted_dict.keys())[:top_n]
    new_ent1 = random.sample(ent_sorted, sample_num)
    tp_has_new_ent1 = []
    for line in tp_all:
        parts = line.strip().split('\t')
        if parts[0] in new_ent1 or parts[2] in new_ent1:
            tp_has_new_ent1.append(line.strip())
    s2 = set(tp_has_new_ent1).union(tp1)
    s1 = tp
    s0 = s0 - s1
    s2 = s2 - s1
    s2 = s2 - s0

    tp_to_01 = set(tp_dict.keys()) - tp1
    tp_to_01 = tp_to_01 - s0
    tp_to_01 = tp_to_01 - s1
    tp_to_01 = tp_to_01 - s2
    s0_add = set(random.sample(tp_to_01, int(len(tp_to_01) * 0.5)))
    s1_add = tp_to_01 - s0_add
    s1 = s1.union(s1_add)
    s0 = s0.union(s0_add)

    tp_remain = set(tp_all) - s0 - s1 - s2
    s1_ent = set()
    for line in s1:
        parts = line.strip().split('\t')
        s1_ent.add(parts[0])
        s1_ent.add(parts[2])
    s2_ent = set()
    for line in s2:
        parts = line.strip().split('\t')
        s2_ent.add(parts[0])
        s2_ent.add(parts[2])
    tp_has_ent1 = []
    for line in tp_remain:
        parts = line.strip().split('\t')
        if parts[0] in s1_ent and parts[2] in s1_ent:
            tp_has_ent1.append(line.strip())
    tp_random = random.sample(tp_has_ent1, 62023 - len(s1))
    s1 = set(tp_random).union(s1)
    tp_remain = tp_remain - set(tp_random)

    tp_has_ent2 = []
    for line in tp_remain:
        parts = line.strip().split('\t')
        if parts[0] in s2_ent and parts[2] in s2_ent:
            tp_has_ent2.append(line.strip())
    tp_random = random.sample(tp_has_ent2, 62023 - len(s2))
    s2 = set(tp_random).union(s2)
    tp_remain = tp_remain - set(tp_random)

    s0 = set(tp_remain).union(s0)
    r_final = set()
    e_final = set()
    for line in s0:
        parts = line.strip().split('\t')
        r_final.add(parts[1])
        e_final.add(parts[0])
        e_final.add(parts[2])

    all_rel = set()
    with open("../data/FB15k-237/relations.dict",'r') as f:
        for line in f:
            all_rel.add(line.strip().split('\t')[1])
    n_rel = all_rel - r_final
    add_s0_rel1 = []
    for line in s1:
        if line.split('\t')[1] in n_rel:
            add_s0_rel1.append(line)
    add_s0_rel2 = []
    for line in s2:
        if line.split('\t')[1] in n_rel:
            add_s0_rel2.append(line)

    add_s0 = random.sample(add_s0_rel1,int(len(add_s0_rel1)*0.5))
    s1 = s1 - set(add_s0)
    add_s1 = random.sample(s0,int(len(add_s0_rel1)*0.5))
    s1 = s1.union(set(add_s1))
    s0 = s0 - set(add_s1)
    s0 = s0.union(set(add_s0))

    add_s0 = random.sample(add_s0_rel2,int(len(add_s0_rel2)*0.5))
    s2 = s2 - set(add_s0)
    add_s2 = random.sample(s0,int(len(add_s0_rel1)*0.5))
    s2 = s2.union(set(add_s2))
    s0 = s0 - set(add_s2)
    s0 = s0.union(set(add_s0))
    return s0, s1, s2

def split_data(s0,s1,s2,data_name):
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
    for line in s0:
        parts = line.strip().split('\t')
        ent.add(parts[0])
        ent.add(parts[2])
        rel.add(parts[1])

    ent_miss = [e for e in ent if e not in ent_dict]
    rel_miss = [r for r in rel if r not in rel_dict]
    tp_miss = []
    for line in s0:
        parts = line.strip().split('\t')
        if parts[0] in ent_miss or parts[2] in ent_miss:
            tp_miss.append(line.strip())
        if parts[1] in rel_miss:
            tp_miss.append(line.strip())
    while (1):
        train1 = train + tp_miss
        rel_dict = set()
        ent_dict = set()
        for line in train1:
            parts = line.strip().split('\t')
            rel_dict.add(parts[1])
            ent_dict.add(parts[0])
            ent_dict.add(parts[2])
        if len(ent_dict) == len(ent) and len(rel_dict) == 237:
            train = train1
            break

    remain = [t for t in s0 if t not in train]
    random.shuffle(remain)
    valid = remain[:int(len(s0) / 5)]
    test = remain[int(len(s0) / 5):]

    with open('../data/{}/0/train.txt'.format(data_name), 'w') as f:
        for line in train:
            f.write(line + '\n')
    with open('../data/{}/0/valid.txt'.format(data_name), 'w') as f:
        for line in valid:
            f.write(line + '\n')
    with open('../data/{}/0/test.txt'.format(data_name), 'w') as f:
        for line in test:
            f.write(line + '\n')

    ent1 = set()
    for line in s1:
        ent1.add(line.strip().split('\t')[0])
        ent1.add(line.strip().split('\t')[2])

    ent = set()
    with open('../data/{}/0/train.txt'.format(data_name), 'r') as f:
        for line in f:
            ent.add(line.strip().split('\t')[0])
            ent.add(line.strip().split('\t')[2])
    all_ent = set()
    with open("../data/FB15k-237/entities.dict", 'r') as f:
        for line in f:
            all_ent.add(line.strip().split('\t')[1])
    new_ent = ent1 - ent

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
    for line in s1:
        parts = line.strip().split('\t')
        if parts[0] in ent_miss or parts[2] in ent_miss:
            tp_miss.append(line.strip())

    random_tp_miss = random.sample(tp_miss, int(len(tp_miss) * 1))

    while (1):
        to_del = random.sample(train, len(random_tp_miss))
        train1 = [t for t in train if t not in to_del]
        train1 = train1 + random_tp_miss
        rel_dict = set()
        ent_dict = set()
        for line in train1:
            parts = line.strip().split('\t')
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
        for line in train:
            f.write(line + '\n')
    with open('../data/{}/1/valid.txt'.format(data_name), 'w') as f:
        for line in valid:
            f.write(line + '\n')
    with open('../data/{}/1/test.txt'.format(data_name), 'w') as f:
        for line in test:
            f.write(line + '\n')

    ent = set()
    with open('../data/{}/0/train.txt'.format(data_name), 'r') as f:
        for line in f:
            ent.add(line.strip().split('\t')[0])
            ent.add(line.strip().split('\t')[2])
    all_ent = set()
    with open("../data/FB15k-237/entities.dict", 'r') as f:
        for line in f:
            all_ent.add(line.strip().split('\t')[1])
    ent1 = set()
    for line in s1:
        ent1.add(line.strip().split('\t')[0])
        ent1.add(line.strip().split('\t')[2])
    new_ent = all_ent - ent1
    new_ent = new_ent - ent

    rel_dict = set()
    ent_dict = set()
    train = random.sample(s2, int(len(s2) * 3 / 5))
    for line in train:
        parts = line.strip().split('\t')
        rel_dict.add(parts[1])
        ent_dict.add(parts[0])
        ent_dict.add(parts[2])

    ent_miss = [e for e in new_ent if e not in ent_dict]
    print(len(ent_miss))

    tp_miss = []
    for line in s2:
        parts = line.strip().split('\t')
        if parts[0] in ent_miss or parts[2] in ent_miss:
            tp_miss.append(line.strip())

    random_tp_miss = random.sample(tp_miss, int(len(tp_miss) * 1))

    while (1):
        to_del = random.sample(train, len(random_tp_miss))
        train1 = [t for t in train if t not in to_del]
        train1 = train1 + random_tp_miss
        rel_dict = set()
        ent_dict = set()
        for line in train1:
            parts = line.strip().split('\t')
            rel_dict.add(parts[1])
            ent_dict.add(parts[0])
            ent_dict.add(parts[2])
        if ent_dict.intersection(new_ent) == new_ent:
            train = train1
            break
    remain = [t for t in s2 if t not in train]
    random.shuffle(remain)
    valid = remain[:int(len(s2) / 5)]
    test = remain[int(len(s2) / 5):]

    with open('../data/{}/2/train.txt'.format(data_name), 'w') as f:
        for line in train:
            f.write(line + '\n')
    with open('../data/{}/2/valid.txt'.format(data_name), 'w') as f:
        for line in valid:
            f.write(line + '\n')
    with open('../data/{}/2/test.txt'.format(data_name), 'w') as f:
        for line in test:
            f.write(line + '\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--instance_file', type=str, help="File name of rule instances")
    parser.add_argument('--data_name', type=str, help="Dataset name")
    args = parser.parse_args()
    instance_file = args.instance_file
    data_name = args.data_name
    tp_dict = parse_instance_file(instance_file, max_lines=66736)
    new_dict = filter_tp_dict(tp_dict, threshold=3)
    tp1 = list(new_dict.keys())
    tp2 = sample_tp(instance_file,max_lines=66736)
    tp = set(tp1).union(tp2)
    s0, s1, s2 = time_split(tp, tp_dict, instance_file, max_lines=None)
    split_data(s0, s1, s2, data_name)

if __name__ == "__main__":
    main()
