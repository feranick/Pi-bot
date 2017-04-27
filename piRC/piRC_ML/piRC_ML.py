#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************************
*
* PiRC - Machine learning train and predict
* version: 20170426g
*
* By: Nicola Ferralis <feranick@hotmail.com>
*
***********************************************************
'''
print(__doc__)

import numpy as np
import sys, os.path, getopt, glob, csv
from time import sleep, time
from os.path import exists, splitext
from os import rename
from datetime import datetime, date

#import piRC_gpio
#from piRC_lib import *

from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.externals import joblib
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler

#**********************************************
''' Neural Networks'''
#**********************************************
class nnDef:
    runNN = True
    nnAlwaysRetrain = False
    
    regressor = False

    # threshold in % of probabilities for listing prediction results
    thresholdProbabilityNNPred = 0.001
    
    ''' Solver for NN
        lbfgs preferred for small datasets
        (alternatives: 'adam' or 'sgd') '''
    nnSolver = 'lbfgs'
    nnNeurons = 10  #default = 10

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

    try:
        sys.argv[3]
        if sys.argv[3] in ("-C", "--Classifier"):
            nnDef.regressor = False
        elif sys.argv[3] in ("-R", "--Regressor"):
            nnDef.regressor = True
    except:
        print('C')

    for o, a in opts:
        if o in ("-r" , "--run"):
            try:
                runAuto(sys.argv[2])
            except:
                #fullStop()
                #GPIO.cleanup()
                sys.exit(2)

        if o in ("-t" , "--train"):
            try:
                runTrain(sys.argv[2])
            except:
                #fullStop()
                #GPIO.cleanup()
                sys.exit(2)

#************************************
''' runAuto '''
''' Use ML models to predict steer and power '''
#************************************
def runAuto(trainFile):
    trainFileRoot = os.path.splitext(trainFile)[0]
    Cl, sensors = readTrainFile(trainFile)
    runNN(sensors, Cl, trainFileRoot, False)

#************************************
''' runTrain '''
''' Use ML models to predict steer and power '''
#************************************
def runTrain(trainFile):
    trainFileRoot = os.path.splitext(trainFile)[0]
    Cl, sensors = readTrainFile(trainFile)
    runNN(sensors, Cl, trainFileRoot, True)

#************************************
''' read Train File '''
#************************************
def readTrainFile(trainFile):
    try:
        with open(trainFile, 'r') as f:
            M = np.loadtxt(f, unpack =False)
    except:
        print('\033[1m' + ' Training file not found \n' + '\033[0m')
        return

    steer = M[:,0]
    power = M[:,1]
    Cl = M[:,[0,1]]
    
    sensors = np.delete(M,np.s_[0:2],1)
    return Cl, sensors

#********************************************************************************
''' Run Neural Network '''
#********************************************************************************
def runNN(sensors, Cl, Root, trainMode):
    if nnDef.regressor is False:
        nnTrainedData = Root + '.nnModelC.pkl'
    else:
        nnTrainedData = Root + '.nnModelR.pkl'
    print(' Running Neural Network: multi-layer perceptron (MLP) - (solver: ' + nnDef.nnSolver + ')...')
    
    scaler = StandardScaler()
    sensors = scaler.fit_transform(sensors)

    if nnDef.regressor is False:
        binarizer = MultiLabelBinarizer()
        Y = binarizer.fit_transform(Cl)
    else:
        Y = Cl
    
    if trainMode is True:
        nnDef.nnAlwaysRetrain = True
    try:
        if nnDef.nnAlwaysRetrain == False:
            with open(nnTrainedData):
                print(' Opening NN training model...\n')
                clf = joblib.load(nnTrainedData)
        else:
            raise ValueError('Force NN retraining.')
    except:
        #**********************************************
        ''' Retrain data if not available'''
        #**********************************************
        print(' Retraining NN model...')
        if nnDef.regressor is False:
            clf = MLPClassifier(solver=nnDef.nnSolver, alpha=1e-5, hidden_layer_sizes=(nnDef.nnNeurons,), random_state=1)
        else:
            clf = MLPRegressor(solver=nnDef.nnSolver, alpha=1e-5, hidden_layer_sizes=(nnDef.nnNeurons,), random_state=1)
        clf.fit(sensors, Y)
        joblib.dump(clf, nnTrainedData)

    if trainMode is False:
        while True:
            try:
                #l,r,c,b = readAllSonars(TRIG, ECHO)
                #x,y,z = readAccel(True)
                #nowsensors = np.array(['{:0.2f}'.format(x) for x in [l,r,c,b,x,y,z]]).reshape(1,-1)
            
                nowsensors = np.array([[1.10,1.10,1.10,1.10,0.000,0.000,0.000]]).reshape(1,-1)
                nowsensors = np.array([[1.10,1.10,1.10,1.10,0.028,0.236,0.952]]).reshape(1,-1)
                
                if nnDef.regressor is False:
                    nowsensors = scaler.transform(nowsensors)
                    
                    sp = binarizer.inverse_transform(clf.predict(nowsensors))[0]
                    print('\033[1m' + '\n Predicted classification value (Neural Networks) = (',str(sp[0]),',',str(sp[1]),')')
                    prob = clf.predict_proba(nowsensors)[0].tolist()
                    print(' (probability = ' + str(round(100*max(prob),4)) + '%)\033[0m\n')
                else:
                    sp = clf.predict(nowsensors)[0]
                    print('\033[1m' + '\n Predicted regression value (Neural Networks) = (',str(round(sp[0])),',',str(round(sp[1])),')')
                sleep(0.1)
            except:
                return
    else:
        return

#************************************
''' Lists the program usage '''
#************************************
def usage():
    print('\n Usage:')
    print('\n Trainining only (Classifier):\n  python3 piRC_ML.py -t <train file>')
    print('\n Prediction only (Classifier):\n  python3 piRC_ML.py -r <train file>')
    print('\n Trainining only (Regression):\n  python3 piRC_ML.py -t <train file> -R')
    print('\n Trainining only (Regression):\n  python3 piRC_ML.py -t <train file> -R')
    print('\n (Separate trained models are created for regression and classification\n')

    print(' Requires python 3.x. Not compatible with python 2.x\n')

#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
