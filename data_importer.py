import csv

def import_from_csv(filename):
    data = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        header = []
        is_header = True
        for row in reader:
            if is_header:
                header = row
                is_header = False
                continue
            obj = {}
            for k, v in zip(header, row):
                try:
                    if v.isdigit():
                        obj[k] = int(v)
                    else:
                        obj[k] = float(v)
                except:
                    obj[k] = v
            data.append(obj)
    return data