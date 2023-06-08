import utils as ut
import pandas as pd

import numpy as np

def load_file(path:str)->str:
    with open(path,"r") as file:
        return file.read()

def parse_file_to_numpy(filename):
    with open(filename, 'r') as f:
        content = f.read()

    content = (content.replace('[', '').replace(']', '').replace('"', '')).split(',')
    arrays = [[float(num_str) for num_str in array_str.split()] for array_str in content]
    return [np.array(array) for array in arrays]

def save_data_to_csv(output_path:str,data:np.array)->None:
    np.savetxt(output_filepath,data,delimiter=',')

def process(filepath:str,output_filepath:str)->None:
    data=parse_file_to_numpy(filepath)
    save_data_to_csv(output_filepath,data)


if __name__=="__main__":
    input_filepath=ut.merge_paths(ut.get_actual_dir(),"input_data/ppg_pulses.csv")
    output_filepath=ut.merge_paths(ut.get_actual_dir(),"input_data/ppg_pulses_parsed.csv")
    process(input_filepath,output_filepath)
    print()