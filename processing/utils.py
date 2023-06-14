import numpy as np
import pandas as pd
import os

def get_actual_dir()->str:    
    """ Function for getting actual directory

    Returns:
        str: filepath to actual directory of calling script
    """
    return os.path.dirname(os.path.realpath(__file__))

def merge_paths(path1:str,path2:str)->str:
    """ Function for merging two paths

    Args:
        path1 (str): path 1
        path2 (str): path 2

    Returns:
        str: merged path
    """
    return os.path.join(path1,path2)

def load_csv_data(path:str)->pd.DataFrame:
    """ Function for loading csv data with numpy, returns pandas dataframe

    Args:
        path (str): input_path

    Returns:
        pd.DataFrame: pandas dataframe
    """    
    data=np.loadtxt(path,delimiter=",",dtype=float)
    return data

def save_data_to_csv(output_path:str,data:np.array)->None:
    """ Np method for saving csv data

    Args:
        output_path (str): output path for saving
        data (np.array): input data
    """    
    np.savetxt(output_path,data,delimiter=',')

def load_txt_file(path:str)->str:
    """ Function for loading txt file

    Args:
        path (str): input path

    Returns:
        str: return string of file
    """    
    with open(path,"r") as file:
        return file.read()
