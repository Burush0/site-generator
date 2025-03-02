import os, shutil

def move_files(source, destination):
    if not os.path.exists(destination):
        os.mkdir(destination)

    for file in os.listdir(source):
        src_filepath = os.path.join(source, file)
        dst_filepath = os.path.join(destination, file)
        print(f" * {src_filepath} -> {dst_filepath}")
        if os.path.isfile(src_filepath):
            shutil.copy(src_filepath, dst_filepath)
        else:
            move_files(src_filepath, dst_filepath)
    
