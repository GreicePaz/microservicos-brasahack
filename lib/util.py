import io, csv, json

def csv_to_json(data):
    try:
        file_contents = io.StringIO(data.read().decode('UTF8'))
    
        reader = csv.DictReader
        reader = csv.DictReader(file_contents)

        out = json.dumps([row for row in reader])
        out = json.loads(out)
    except:
        out = {}
    
    return out

def dict_to_new_dict(data):
    new_dict = {}
    for k, v in data.items():
        new_dict[k] = v
    
    return new_dict
