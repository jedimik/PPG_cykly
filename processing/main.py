import numpy as np
from scipy.stats import pearsonr, pointbiserialr
import utils as ut
import ordpy as op
from matplotlib import pyplot as plt
import pandas as pd

def get_permutation_entropy(data:np.array,taux:int=1,dx:int=None):
    list2d=[]
    delta=[]
    for i in range(2,8):
        list1d=[]
        for ind in range(len(data)):
            if dx is not None and data[ind]:
                list2d.append(op.permutation_entropy(data=data[ind],dx=dx,taux=taux,normalized=True))
                continue
            try: # It eliminates empty arrays and low length arrays
                list1d.append(op.permutation_entropy(data=data[ind],dx=i,taux=taux,normalized=True))
            except:
                list1d.append(0)
        if dx is not None:
            delta=dx
            break
        list2d.append(list1d)  
        delta.append(i)
    return list2d, delta

def get_pearson_correlation(pe,classification):
    if isinstance(pe[0],list):
        correl=[]
        for i in range(len(pe)):
            correl.append(pearsonr(classification,pe[i])[0])
    else:
        correl=pearsonr(classification,pe)[0]
    return correl

def get_pointbiserial_correlation(pe,classification):
    if isinstance(pe[0],list):
        correl=[]
        for i in range(len(pe)):
            correl.append(pointbiserialr(classification,pe[i])[0])
    else:
        correl=pointbiserialr(classification,pe)[0]
    return correl

def plot_with_subplots(perm_entropy:list, classification:list,delta:list,without_outlier:bool=False,value:str=""):
    fig, axs = plt.subplots(len(delta), 1, figsize=(10, 6 * len(delta)))
    fig.tight_layout(pad=6.0)  # Increase the vertical spacing between subplots
    class_map = {0: 0, 1: 1}

    for i, ax in enumerate(axs):
        # Creating a DataFrame for easier manipulation
        data = pd.DataFrame({'Permutation Entropy': perm_entropy[i], 'Classification': classification})
        data['Classification'] = data['Classification'].map(class_map)  # Convert class labels into 0's and 1's

        # Remove rows where Permutation Entropy is 0
        if without_outlier:
            data = data[data['Permutation Entropy'] != 0]

        # Calculating the correlation
        correlation = np.corrcoef(data['Permutation Entropy'], data['Classification'])[0, 1]
        print(f'Correlation between permutation entropy and classification at delta {delta[i]}: {correlation}')

        # Creating the plot
        for class_label in data['Classification'].unique():
            subset = data[data['Classification'] == class_label]
            ax.scatter(subset['Permutation Entropy'], np.full_like(subset['Permutation Entropy'], fill_value=class_label), label=class_label)

        ax.set_xlabel(f'Permutation vs classification at delta:{delta[i]}')
        ax.legend()
        ax.set_ylim(-0.5, 1.5)
        fig.suptitle(f'Permutation Entropy vs Classification with:{value}', fontsize=16)
        
def remove_outliers(dataset, multiplier=1.5):
    # Calculate the IQR of the data
    new_dataset = []

    for ind, data in enumerate(dataset):
        Q1 = np.percentile(data, 25)
        Q3 = np.percentile(data, 75)
        IQR = Q3 - Q1

        # Define the upper and lower bounds for outliers
        lower_bound = Q1 - multiplier * IQR
        upper_bound = Q3 + multiplier * IQR

        # Remove outliers
        no_outliers = [x for x in data if ((x >= lower_bound) & (x <= upper_bound) & (x != 0))]
        new_dataset.append(no_outliers)

    return new_dataset

def maintain_with_outliers(data:list,classification:list,outlier_indexes:list):
    new_data=[]
    new_classification=[]
    for i in range(len(data)):
        if i not in outlier_indexes:
            new_data.append(data[i])
            new_classification.append(classification[i])
    return new_data,new_classification

def process_with_outliers(base_data,expert_classification:str,machine_classification:str=None):
    classification_expert=ut.load_csv_data(ut.merge_paths(ut.get_actual_dir(),expert_classification))
    if machine_classification is not None:
        classification_machine=ut.load_csv_data(ut.merge_paths(ut.get_actual_dir(),machine_classification))
        classification_machine=[1 if x >= 0.89 else 0 for x in classification_machine]
    pe,delta=get_permutation_entropy(base_data,taux=1)
    plot_with_subplots(pe,classification_expert,delta,value="with outliers classified by Expert",without_outlier=True)
    plot_with_subplots(pe,classification_machine,delta,value="with outliers classified by Machine",without_outlier=True)
    

def process_removed_outliers(base_data,expert_classification:str,machine_classification:str=None):
    classification_expert=ut.load_csv_data(ut.merge_paths(ut.get_actual_dir(),expert_classification))
    if machine_classification is not None:
        classification_machine=ut.load_csv_data(ut.merge_paths(ut.get_actual_dir(),machine_classification))
        classification_machine=[1 if x >= 0.89 else 0 for x in classification_machine]
    base_data=remove_outliers(base_data)
    pe,delta=get_permutation_entropy(base_data,taux=1)
    plot_with_subplots(pe,classification_expert,delta,value="without outliers classified by Expert",without_outlier=True)
    plot_with_subplots(pe,classification_machine,delta,value="without outliers classified by Machine",without_outlier=True)

def process(data_path:str,expert_classification:str,machine_classification:str=None):
    base_data=ut.load_csv_data(ut.merge_paths(ut.get_actual_dir(),data_path))
    process_with_outliers(base_data,expert_classification,machine_classification)
    process_removed_outliers(base_data,expert_classification,machine_classification)
    plt.show()
    print()

if __name__=="__main__":
    data_path="input_data/ppg_pulses_parsed.csv"
    expert_classification="classification/ppg_manual_class.csv"
    machine_classification="classification/ppg_machine_class.csv"
    process(data_path,expert_classification,machine_classification)


