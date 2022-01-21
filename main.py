

import os

from script_generate import generate
from script_perfs import experiment



def try_mkdir(dir_path):
    try:
        os.mkdir(dir_path)
    except FileExistsError:
        pass


if __name__ == '__main__':
    try_mkdir("./temp/")
    generate()
    experiment("sensor_mediation")

