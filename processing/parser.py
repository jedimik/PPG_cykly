import utils as ut
import pandas as pd
from io import StringIO

def load_file(path:str)->str:
    with open(path,"r") as file:
        return file.read()


def parse_data(s):
    # Remove the leading and trailing brackets and quotes.
    s = s.replace("[", "").replace("]", "").replace('"', "")

    # Convert the array of floats into a DataFrame.
    df = pd.read_csv(StringIO(s),sep=",",header=None)
    
    return df

if __name__=="__main__":
    filepath=ut.merge_paths(ut.get_actual_dir(),"input_data/ppg_pulses.csv")
    data=load_file(filepath)
    data1=parse_data(data)
    pass