#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************************
*
* PiRC - Machine learning train and predict
* version: 20170425d
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
import random
from sklearn.neural_network import MLPClassifier
from sklearn.externals import joblib
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler

#**********************************************
''' Neural Networks'''
#**********************************************
class nnDef:
    runNN = True
    nnAlwaysRetrain = False
    plotNN = True
    nnClassReport = False
    
    # threshold in % of probabilities for listing prediction results
    thresholdProbabilityNNPred = 0.001
    
    ''' Solver for NN
        lbfgs preferred for small datasets
        (alternatives: 'adam' or 'sgd') '''
    nnSolver = 'lbfgs'
    nnNeurons = 100  #default = 100

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
            #try:
            runAuto(sys.argv[2])
            #except:
            #    usage()
            #    sys.exit(2)

        if o in ("-t" , "--train"):
            #try:
            runTrain(sys.argv[2])
            #except:
            #    usage()
            #    sys.exit(2)

#************************************
''' runAuto '''
''' Use ML models to predict steer and power '''
#************************************
def runAuto(trainFile):
    trainFileRoot = os.path.splitext(trainFile)[0]
    Cl, sensors = readTrainFile(trainFile)
    nowsensors = sensors[0,:].reshape(1,-1)  # to be changed
    print(nowsensors.shape)
    nowSteer, nowPower = runNN(sensors, Cl, trainFileRoot, False)


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
    nnTrainedData = Root + '.nnModel.pkl'
    print(' Running Neural Network: multi-layer perceptron (MLP) - (solver: ' + nnDef.nnSolver + ')...')
    
    scaler = StandardScaler()
    sensors = scaler.fit_transform(sensors)

    Y1 = MultiLabelBinarizer().fit(Cl)
    Y = MultiLabelBinarizer().fit_transform(Cl)
    
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
        clf = MLPClassifier(solver=nnDef.nnSolver, alpha=1e-5, hidden_layer_sizes=(nnDef.nnNeurons,), random_state=1)
        clf.fit(sensors, Y)
        joblib.dump(clf, nnTrainedData)

    if trainMode is False:
    
        while True:
            nowsensors = np.array([[1.10,1.10,1.10,1.10,0.000,0.000,0.000]]).reshape(1,-1)
            #nowsensors = np.array([[1.10,1.10,1.10,1.10,0.068,0.204,0.924]]).reshape(1,-1)
            #nowsensors = np.array([[1.10,1.10,1.10,1.10,0.1,0.1,0.89]]).reshape(1,-1)

            nowsensors = scaler.transform(nowsensors)
            print(nowsensors)

            print('\033[1m' + '\n Predicted value (Neural Networks) = ' + str(Y1.inverse_transform(clf.predict(nowsensors))[0]))
            #prob = clf.predict_proba(nowsensors)[0].tolist()
            #print(' (probability = ' + str(round(100*max(prob),4)) + '%)\033[0m\n')
            sleep(0.1)
    else:
        return


#************************************
''' Lists the program usage '''
#************************************
def usage():
    print('\n Usage:\n')
    print(' Requires python 3.x. Not compatible with python 2.x\n')

#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
