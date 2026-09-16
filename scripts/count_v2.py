import glob, os

classes = [
    'Beaker', 'Buchner_Funnel', 'Burette_Stands', 'Calorimeter',
    'Conical_Flask', 'Funnel', 'Glass_Rod', 'Measuring_Cylinder',
    'Mechanical_Balance_Scale', 'Nessler_Reagent_Bottle', 'Pipette',
    'Porcelain_Mortar_Pestle', 'Precision_Weight_Scale', 'Reagent_Bottle',
    'Round_Bottom_Flask_Borosilicate_Glass_1_Neck',
    'Round_Bottom_Flask_Borosilicate_Glass_2_Neck',
    'Round_Bottom_Flask_Borosilicate_Glass_3_Neck',
    'Separating_Funnel', 'Spirit_Lamp', 'TestTube_Holder', 'Test_Tube',
    'Volumetric_Flask', 'Volumetric_Pipet', 'Wash_Bottle', 'Weighing_Bottle'
]
counts = {c: {'train': 0, 'valid': 0, 'test': 0} for c in classes}

for split in ['train', 'valid', 'test']:
    for p in glob.glob(f'Dataset/ChemEq25_training_verified_v2/{split}/labels/*.txt'):
        with open(p, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 1:
                    cls_id = int(parts[0])
                    counts[classes[cls_id]][split] += 1

out = 'Class | Train | Valid | Test\n'
out += '---|---|---|---\n'
mins, maxs = float('inf'), 0
for c in classes:
    insts = counts[c]['train'] + counts[c]['valid'] + counts[c]['test']
    mins = min(mins, insts)
    maxs = max(maxs, insts)
    out += f"{c} | {counts[c]['train']} | {counts[c]['valid']} | {counts[c]['test']}\n"

out += f'\nTotal Instances Range: Min={mins} Max={maxs}\n'
out += f'Max/Min Imbalance Ratio: {maxs/mins:.2f}\n'
with open('outputs/dataset_audit/v2_class_dist.txt', 'w') as f:
    f.write(out)
