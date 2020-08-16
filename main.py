import os
import sys
from hurry.filesize import size as sizef

def get_size(start_path='.'):
    total_size = 0
    for root, dirs, files in os.walk(start_path, topdown=False):
        for name in files:
            fp = os.path.join(root, name)
            if not os.path.islink(fp):
                try:
                    size = os.path.getsize(fp)
                    total_size += size
                except:
                    pass
    return total_size

def get_each_folder_size(start_path="."):
    all_files = [f for f in os.listdir(start_path)]
    files_with_sizes = []
    for file in all_files:
        if not os.path.isfile(file):
            size = get_size(os.path.join(start_path, file))
            files_with_sizes.append((file, size))
        else:
            size = os.path.getsize(file)
            files_with_sizes.append((file, size))

    return files_with_sizes


def sort_files(files):
    def sorting_method(file):
        return file[1]
    return files.sort(reverse=True, key=sorting_method)


if __name__ == "__main__":
    args = sys.argv
    path = '.'
    if len(args) > 1:
        path = args[1]
    files = get_each_folder_size(path)
    sort_files(files)
    for file in files:
        # gb_size = file[1]/1000000000
        size = sizef(file[1])
        print("%s %s" % (file[0], size))
