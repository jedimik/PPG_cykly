import utils as ut
import pandas as pd
import os
import numpy as np

def parse_file_to_numpy(filename:str) -> np.array:
    """Function for parsing specific txt file

    Args:
        filename (str): path to file, or data string

    Returns:
        np.array: output parsed np.array data ready to save
    """
    if os.path.isfile(filename):
        content = ut.load_txt_file(filename)
    else:
        content = filename
    content = (content.replace('[', '').replace(']', '').replace('"', '')).split(',')
    arrays = [[float(num_str) for num_str in array_str.split()] for array_str in content]
    return [np.array(array) for array in arrays]

def process(filepath:str,output_filepath:str)->None:
    """Parse processing function

    Args:
        filepath (str): filepath to file
        output_filepath (str): output filepath name
    """
    data=parse_file_to_numpy(filepath)
    ut.save_data_to_csv(output_filepath,data)


if __name__=="__main__":
    input_filepath=ut.merge_paths(ut.get_actual_dir(),"input_data/ppg_pulses.csv")
    output_filepath=ut.merge_paths(ut.get_actual_dir(),"input_data/ppg_pulses_parsed.csv")
    process(input_filepath,output_filepath)
    