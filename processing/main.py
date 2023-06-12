import numpy as np
from scipy.stats import pearsonr, pointbiserialr
import utils as ut
import ordpy as op
import statsmodels.api as sm
from matplotlib import pyplot as plt

def get_permutation_entropy(data:np.array,taux:int=1,dx:int=None):
    list2d=[]
    delta=[]
    for i in range(1,7):
        list1d=[]
        for ind in range(len(data)):
            if dx is not None:
                list2d.append(op.permutation_entropy(data=data[ind],dx=dx,taux=taux,normalized=True))
                continue
            list1d.append(op.permutation_entropy(data=data[ind],dx=i,taux=taux,normalized=True))   
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

def get_logistic_regression(pe,classification):
    if isinstance(pe[0],list):
        correl=[]
        for i in range(len(pe)):
            perm_e=sm.add_constant(pe[i])
            model=sm.Logit(classification,perm_e)
            result=model.fit()
            correl.append(result.summary())
    else:
        perm_e=sm.add_constant(pe)
        model=sm.Logit(classification,perm_e)
        result=model.fit()
        correl=result.summary()
    return correl

def plot_result(correlations:list,delta:list|str):
    
    fig, ax = plt.subplots()

    # Create a boxplot of the results
    ax.boxplot(correlations)

    # Set the title and labels
    ax.set_title('Correlation Results')
    if isinstance(delta,list):        
        labels=[f"Delta:{delta[i]}" for i in range(len(delta))]
    else:
        labels=f"Delta:{delta}"
    ax.set_xticklabels(labels)
    ax.set_ylabel('Correlation Coefficient')

    plt.show()

def process():
    pass



if __name__=="__main__":
    data=ut.load_csv_data(ut.merge_paths(ut.get_actual_dir(),"input_data/ppg_pulses_parsed.csv"))
    classification=ut.load_csv_data(ut.merge_paths(ut.get_actual_dir(),"classification/ppg_manual_class.csv"))
    results,delta=get_permutation_entropy(data,taux=1)
    correl0=get_pearson_correlation(pe=results,classification=classification)
    correl1=get_pointbiserial_correlation(pe=results,classification=classification)
    correl2=get_logistic_regression(pe=results,classification=classification)
    plot_result(correl0,delta)
    plot_result(correl1,delta)
    print()
