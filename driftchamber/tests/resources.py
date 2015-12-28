from os.path import realpath, dirname, join

def resource_path(filename):
    current_dir = dirname(realpath(__file__))
    return join(current_dir, 'resources', filename)
