import ast
import json
import logging
import csv


def save_text_file(obj, file_path):
    """Save 'obj' as text file at 'file_path'."""
    with open(file_path, "w") as file:
        file.write(str(obj))


def read_text_file(file_path, obj_type="list"):
    """Read 'file_path' and return obj_type."""
    with open(file_path, "r") as file:
        obj = file.read()

    literal_types = ["dict", "list"]
    if obj_type in literal_types:
        return ast.literal_eval(obj)
    else:
        return obj




# --------------------------------------------------------------------
# FILE I/O
#  
def pkl_this(filename, obj, protocol=3):
    '''Saves `obj` as `filename`, which must include .pkl extension'''
    with open(filename, 'wb') as picklefile:
        pickle.dump(obj, picklefile, protocol=protocol)

def open_pkl(filename):
    '''Opens pickle file (filename must include .pkl extension). 
       Returns same object as original.
    '''
    with open(filename,'rb') as picklefile:
        return pickle.load(picklefile)


def write_csv(list_obj, filename):
    with open(filename, 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(list_obj)

def read_csv(filename, obj='list'):
    '''Reads csv file; returns object type'''
    data_list = []
    with open(filename, 'r', newline='') as file:
        wr = csv.reader(file)
        for row in wr:
            data_list.append(row)
    return data_list[0]


def open_txt(filename):
    """Reads text file; returns list"""
    result = []
    with open(filename, 'r') as file:
        for line in file:
            result.append(line.strip())
    return result

def write_text(filename, list_obj):
    """Write list_obj to text file"""

    with open(filename, 'w') as file:
        for line in list_obj:
            file.write(line + '\n')


    def write_text_file_json(dict_obj, filename):
        # dict_copy = dict_obj.copy()
        for k, v in dict_obj.items():
            if isinstance(v, np.float64):
                dict_obj[k] = float(v)
            elif isinstance(v, np.int64):
                dict_obj[k] = int(v)

        with open(filename, "w") as f:
            json.dump(dict_obj, f)


def json_read_text_file(filename):
	with open(filename, "r") as f:
		return json.load(f)