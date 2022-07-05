import ast


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
