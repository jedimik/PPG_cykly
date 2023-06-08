import numpy as np
import pandas as pd
import os

def get_actual_dir()->str:    
    return os.path.dirname(os.path.realpath(__file__))

def merge_paths(path1:str,path2:str)->str:
    return os.path.join(path1,path2)

def load_csv_data(path:str)->pd.DataFrame:
    data=pd.read_csv(path)
    return data