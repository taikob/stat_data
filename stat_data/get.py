import numpy as np
import re
import os
from natsort import natsorted

def get_sysparam(data,paramrow):

    param=list()
    for i in paramrow:
        prm=np.empty(0)
        for j in range(len(data)):
            if not float(data[j][i]) in prm:
                prm=np.append(prm,float(data[j][i]))
        param.append(np.sort(prm))

    nump=[]
    for p in param:
        nump.append(len(p))

    return param,nump

def readtitleparam(title,sw=0):
    #sw=0: str
    #sw=1: int
    #sw=2: float

    titleparam=[]
    title=title.split('_')
    del title[len(title)-1]
    pattern = r'([+-]?[0-9]+\.?[0-9]*)'

    for t in title:
        titleparam.append(re.sub('\\D','',t))

    if sw==0: out=[re.findall(pattern, t)[0] for t in title]
    if sw==1: out=[int(re.findall(pattern, t)[0]) for t in title]
    if sw==2: out=[float(re.findall(pattern, t)[0]) for t in title]

    return out

def file_para(path,comtxt,title=None,paramnum=None):
    #comtxt : common text
    #paramum : parameter number

    for dir in natsorted(os.listdir(path)):
        if comtxt in dir:
            tprm = readtitleparam(dir)
            data = np.loadtxt(path + '/' + dir, dtype='float')
            if paramnum is None:
                paramnum = len(tprm)
            datanum=data.shape[0]
            break

    out = np.empty((0, paramnum + datanum))
    for dir in natsorted(os.listdir(path)):
        if comtxt in dir:
            data = np.loadtxt(path + '/' + dir, dtype='float')
            tprm = readtitleparam(dir,2)
            tprm=tprm+data.tolist()
            out = np.append(out, np.array([tprm]), axis=0)

    if title is None: title='stat_data.csv'
    np.savetxt(path + '/' + title, out, delimiter=',')