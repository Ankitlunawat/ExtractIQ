

def csv_safe(value):
    value=str(value)
    return "'"+value if value.lstrip().startswith(("=","+","-","@")) else value
