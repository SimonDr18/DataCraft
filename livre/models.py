import yaml, os.path

Books = yaml.load(open(os.path.join(os.path.dirname(__file__),"data.yml")))

def get_sample():
    return Books[0:10]
