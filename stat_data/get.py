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

def readtitleparam(title):

    titleparam=[]
    title=title.split('_')
    del title[len(title)-1]
    pattern = r'([+-]?[0-9]+\.?[0-9]*)'

    for t in title:
        titleparam.append(re.sub('\\D','',t))

    return [re.findall(pattern, t)[0] for t in title]

def file_para(path,comtxt,title=None):
    #comtxt : common text
    #paramum : parameter number

    for dir in natsorted(os.listdir(path)):
        if comtxt in dir:
            tprm = readtitleparam(dir)
            paramnum = len(tprm)
            break

    out = np.empty((0, paramnum + 1))
    for dir in natsorted(os.listdir(path)):
        if comtxt in dir:
            data = float(np.loadtxt(path + '/' + dir))
            tprm = readtitleparam(dir)
            tprm.append(data)
            out = np.append(out, np.array([[tprm]], axis=0))

    if title is None: title='stat_data.csv'
    np.savetxt(path + '/' + title, out, delimiter=',')