import os
from pathlib import Path


def create_dir(dir_path, **kwargs):
    dir_ = Path(dir_path)
    if not dir_.exists():
        action = True
        while action:
            try:
                dir_.mkdir(**kwargs)
                action = False
            except FileNotFoundError:
                dir__ = Path(os.path.split(dir_path)[0])
                create_dir(dir__, **kwargs)
    return None


if __name__ == '__main__':
    create_dir("D:\\project\\sportslottery\\ML\\model\\baseball\\中華職棒\\2020\\ABC\\LINE")