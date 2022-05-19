import os
from os import listdir
from os.path import isfile, join
import numpy as np
import pickle
from gym_flp.envs import continual
import pandas as pd

def load_mip_files():
    flowfiles = [f for f in listdir(join(search_path, 'flows')) if isfile(join(search_path, 'flows', f))]
    areafiles = [f for f in listdir(join(search_path,'areas')) if isfile(join(search_path,'areas', f))]
    MIPs={}
    
    FlowMatrices={}
    Areas={}
    
    cnt = 0
    f=[]

    for file in flowfiles:
        if file.split('.')[1] == "prn":
            
            cnt += 1
            print("flows", cnt, file)
            file_path = join(search_path, 'flows', file)
            with open(file_path, "r") as datfile:
                
                temp=datfile.read().splitlines()
                for i, line in enumerate(temp):
                    if i == 0:
                        n = int(line.strip())
                        MIPs[file.split(".")[0]] = n
                    elif len(line)<2:
                        continue
                    elif len(f)<n:
                        temp = np.array([line.split()],dtype=float)
                        f.append(temp[0])
                
                F = np.asarray(f)
                FlowMatrices[file.split(".")[0]]=F[:]
                
                datfile.close()
                f = []

    cnt = 0
    
    Layout_widths = {}
    Layout_heights = {}
    
    df = pd.DataFrame()
    for file in areafiles:
        a=[]
        cols = []
        if file.split('.')[1] == "prn":
            cnt += 1
            print("areas", cnt, file)
            file_path = join(search_path,'areas', file)
            with open(file_path, "r") as datfile:
    
                text=datfile.read().splitlines()
                for i, line in enumerate(text):
                    if i == 0:
                        n = int(line.strip())
                        #Areas[file.split(".")[0]] = n
                    elif len(line)<1:
                        continue
                    elif i == 2:
                        temp = line.split()
                        
                        for j in temp:
                            cols.append(j)
                            #df[j] = np.nan
                    elif len(a)<n:
                        temp = np.array(line.split(),dtype = float)
                        a.append(temp)
                    else:
                        temp = line.split()
                        
                        if temp[0] == 'W':
                            Layout_widths[file.split(".")[0]] = float(temp[1])
                        elif temp[0] == 'H':
                            Layout_heights[file.split(".")[0]] = float(temp[1])
                       
                df = pd.DataFrame(a, columns = cols)
                print(n, file)
                A = np.asarray(a)
                Areas[file.split(".")[0]]=df
                
    return MIPs, FlowMatrices, Areas, Layout_heights, Layout_widths

if __name__ == '__main__':
    search_path = os.path.dirname(os.path.realpath(continual.__file__))
    MIPs, FlowMatrices, Areas, Layout_heights, Layout_widths = load_mip_files()
          
    with open(join(search_path, 'cont_instances.pkl'), 'wb') as f:
        pickle.dump([MIPs, FlowMatrices, Areas, Layout_heights, Layout_widths], f)    

   