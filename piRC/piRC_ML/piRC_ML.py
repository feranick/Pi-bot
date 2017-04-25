#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************************
*
* PiRC - Machine learning train and predict
* version: 20170424c
*
* By: Nicola Ferralis <feranick@hotmail.com>
*
***********************************************************
'''
import numpy as np
import sys, os.path, getopt, glob, csv
from os.path import exists, splitext
from os import rename
from datetime import datetime, date
import random


#**********************************************
''' Main '''
#**********************************************
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "rth:", ["run", "train", "help"])
    except:
        usage()
        sys.exit(2)
    
    if opts == []:
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ("-r" , "--run"):
            try:
                runAuto(sys.argv[2])
            except:
                usage()
                sys.exit(2)

    if o in ("-t" , "--traintf"):
        if len(sys.argv) > 3:
            try:
                Train(sys.argv[2])
            except:
                usage()
                sys.exit(2)

#************************************
''' runAuto '''
''' Use ML models to predict steer and power '''
#************************************
def runAuto(learnFile):
    readTrainFile(learnFile)

#************************************
''' read Train File '''
#************************************
def readTrainFile(learnFile):
    try:
        with open(learnFile, 'r') as f:
            M = np.loadtxt(f, unpack =False)
    except:
        print('\033[1m' + ' Training file not found \n' + '\033[0m')
        return

    En = np.delete(np.array(M[0,:]),np.s_[0:1],0)
    M = np.delete(M,np.s_[0:1],0)
    steer = ['{:.2f}'.format(x) for x in M[:,0]]
    power = ['{:.2f}'.format(x) for x in M[:,0]]
    A = np.delete(M,np.s_[0:2],1)
    '''
    Atemp = A[:,range(len(preprocDef.enSel))]

    if preprocDef.cherryPickEnPoint == True and preprocDef.enRestrictRegion == False:
        enPoints = list(preprocDef.enSel)
        enRange = list(preprocDef.enSel)
        
        for i in range(0, len(preprocDef.enSel)):
            enRange[i] = np.where((En<float(preprocDef.enSel[i]+preprocDef.enSelDelta[i])) & (En>float(preprocDef.enSel[i]-preprocDef.enSelDelta[i])))[0].tolist()
            
            for j in range(0, A.shape[0]):
                Atemp[j,i] = A[j,A[j,enRange[i]].tolist().index(max(A[j, enRange[i]].tolist()))+enRange[i][0]]
            
            enPoints[i] = int(np.average(enRange[i]))
        A = Atemp
        En = En[enPoints]
        
        if type == 0:
            print( ' Cheery picking points in the spectra\n')

    # Find index corresponding to energy value to be used for Y normalization
    if preprocDef.fullYnorm == True:
        YnormXind = np.where(En>0)[0].tolist()
    else:
        YnormXind_temp = np.where((En<float(preprocDef.YnormX+preprocDef.YnormXdelta)) & (En>float(preprocDef.YnormX-preprocDef.YnormXdelta)))[0].tolist()
        if YnormXind_temp == []:
            print( ' Renormalization region out of requested range. Normalizing over full range...\n')
            YnormXind = np.where(En>0)[0].tolist()
        else:
            YnormXind = YnormXind_temp

    print(' Number of datapoints = ' + str(A.shape[0]))
    print(' Size of each datapoint = ' + str(A.shape[1]) + '\n')
    return En, Cl, A, YnormXind
    '''

#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
