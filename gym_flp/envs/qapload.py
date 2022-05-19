import os
from os import listdir
from os.path import isfile, join
import numpy as np
import pickle
from gym_flp.envs.discrete import problems

def load_qap_files():
    search_path = os.path.dirname(os.path.realpath(problems.__file__))
    qapfiles = [f for f in listdir(search_path) if isfile(join(search_path, f))]
    QAPs={}
    DistanceMatrices={}
    FlowMatrices={}
    
    cnt = 0
    d=[]
    f=[]
    
    for file in qapfiles:
        if file.lower().endswith('.dat'):
            cnt += 1
            file_path = os.path.join(search_path, file)
            with open(file_path, "r") as datfile:
                temp=datfile.read().splitlines()
                for i, line in enumerate(temp):
                    if i == 0:
                        n = int(line.strip())
                        QAPs[file.split(".")[0]] = n
                    elif len(line)<2:
                        continue
                    elif len(d)<n:
                        temp = np.array([line.split()],dtype=float)
                        d.append(temp[0])
                    elif i>n:
                        if len(f)<n:
                            temp = np.array([line.split()],dtype=float)
                            f.append(temp[0])
                
                D = np.asarray(d)
                F = np.asarray(f)
                DistanceMatrices[file.split(".")[0]]=D[:]
                FlowMatrices[file.split(".")[0]]=F[:]
                
                datfile.close()
                d = []
                f = []
    return DistanceMatrices, FlowMatrices

if __name__ == '__main__':
    DistanceMatrices, FlowMatrices = load_qap_files()
    
    with open(join(os.path.dirname(os.getcwd()), 'envs', 'discrete', 'qap_matrices.pkl'), 'wb') as f:
        pickle.dump([DistanceMatrices, FlowMatrices], f)