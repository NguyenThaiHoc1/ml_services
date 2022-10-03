import os


def create_path(path_dir):
    if os.path.exists(path_dir):
        pass
    else:
        os.mkdir(path_dir)


def upload_file_bytes(file_bytes, path):
    "write type binary"
    f = open(path, "wb")
    f.write(file_bytes)
    f.close()
