import numpy as np
import pandas as pd
import os


def get_actual_dir()->str:    
    return os.path.dirname(os.path.realpath(__file__))

def load_csv_data(path:str)->pd.DataFrame:
    data=pd.read_csv(os.path.join(get_actual_dir(),path))
    return data



if __name__=="__main__":
    data=load_csv_data("input_data/ppg_pulses.csv")
    print()
