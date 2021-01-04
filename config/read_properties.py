from jproperties import Properties

def read(path):
    with open(path, "r+b") as file:
        props = Properties()
        props.load(file, "utf-8")
        return props