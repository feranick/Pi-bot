#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************************
*
* PiRC - Self-driving RC car via Machine Learning
* version: 20180112b
*
* By: Nicola Ferralis <feranick@hotmail.com>
*
***********************************************************
'''
print(__doc__)

import numpy as np
import sys, os.path, os, getopt, glob, csv
from time import sleep, time
from os.path import exists, splitext
from os import rename
from datetime import datetime, date

from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler

#**********************************************
''' MultiClassReductor '''
#**********************************************
class MultiClassReductor():
    def __self__(self):
        self.name = name
    
    totalClass = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,0],[0,1],[1,-1],[1,0],[1,1]]
    
    def transform(self,y):
        Cl = np.zeros(y.shape[0])
        for j in range(len(y)):
            Cl[j] = self.totalClass.index(np.array(y[j]).tolist())
        return Cl
    
    def inverse_transform(self,a):
        return self.totalClass[int(a)]

#**********************************************
''' General parameters'''
#**********************************************
class params:
    timeDelay = 0.25
    filename = 'Training_splrcbxyzv.txt'

    runFullAuto = False
    useCamera = True

    debug = False # do not activate sensors or motors in debug mode

#**********************************************
''' Neural Networks'''
#**********************************************
class nnDef:
    runNN = True
    nnAlwaysRetrain = False
    
    syncTimeLimit = 20  # time in seconds for NN model synchronization
    syncTrainModel = False
    saveNewTrainingData = False
    
    useRegressor = False

    scaler = StandardScaler()
    mlp = MultiClassReductor()
    
    ''' Solver for NN
        lbfgs preferred for small datasets
        (alternatives: 'adam' or 'sgd') '''
    nnSolver = 'lbfgs'
    nnNeurons = 10  #default = 10


#******************************************************
''' Import hardware library if not in debug mode'''
#******************************************************
if params.debug == False:
        import piRC_lib

#**********************************************
''' Main '''
#**********************************************
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "rtch:", ["run", "train", "collect", "help"])
    except:
        usage()
        sys.exit(2)
    
    if opts == []:
        usage()
        sys.exit(2)

    try:
        sys.argv[3]
        if sys.argv[3] in ("-C", "--Classifier"):
            nnDef.useRegressor = False
        elif sys.argv[3] in ("-R", "--Regressor"):
            nnDef.useRegressor = True
    except:
        nnDef.useRegressor = False

    for o, a in opts:
        if o in ("-r" , "--run"):
            #try:
            runAuto(sys.argv[2],params.runFullAuto)
            #except:
            #    exitProg()

        if o in ("-t" , "--train"):
            #try:
            runTrain(sys.argv[2])
            #except:
            #    sys.exit(2)

        if o in ("-c" , "--collect"):
            #try:
            writeTrainFile()
            #except:
            #    exitProg()

#*************************************************
''' runAuto '''
''' Use ML models to predict steer and power '''
#*************************************************
def runAuto(trainFile, type):
    trainFileRoot = os.path.splitext(trainFile)[0]
    Cl, sensors = readTrainFile(trainFile)
    clf = runNN(sensors, Cl, trainFileRoot)
    fullStop(False)
    syncTime = time()
    while True:
        if time() - syncTime > nnDef.syncTimeLimit and nnDef.syncTrainModel == True:
            print(" Reloading NN model...")
            clf = runNN(sensors, Cl, trainFileRoot)
            print(" Synchronizing NN model...\n")
            os.system("./syncTFile.sh " + trainFileRoot + " &")
            syncTime = time()
        
        if type == False:
            print(" Running \033[1mPartial Auto\033[0m Mode\n")
            s, p = predictDrive(clf)
            drive(s,p)
            sleep(params.timeDelay)
        else:
            print(" Running \033[1mFull Auto\033[0m Mode\n")
            dt=0
            t1=time()
            while dt < 0.5:
                s, p = predictDrive(clf)
                if p != 0:
                    dt = 0
                    drive(s,p)
                else:
                    dt = time() - t1
                sleep(params.timeDelay)
            drive(0, 1)
            sleep(0.5)
            drive(0, 0)

#*************************************************
''' runTrain '''
''' Use ML models to predict steer and power '''
#*************************************************
def runTrain(trainFile):
    trainFileRoot = os.path.splitext(trainFile)[0]
    Cl, sensors = readTrainFile(trainFile)
    nnDef.nnAlwaysRetrain = True
    runNN(sensors, Cl, trainFileRoot)

#*************************************************
''' write training file from sensors '''
#*************************************************
def writeTrainFile():
    while True:
        if params.useCamera == False:
            s,p,l,r,c,b,x,y,z,v = piRC_lib.readAllSensors(params.useCamera)
        else:
            s,p,l,r,c,b,x,y,z,v,img = piRC_lib.readAllSensors(params.useCamera)
            print(img)
        print(' S={0:.0f}, P={1:.0f}, L={2:.0f}, R={3:.0f}, C={4:.0f}, B={5:.0f}, X={6:.3f}, Y={7:.3f}, Z={8:.3f}, V={9:.2f}'.format(s,p,l,r,c,b,x,y,z,v))
        with open(params.filename, "a") as sum_file:
            sum_file.write('{0:.0f}\t{1:.0f}\t{2:.0f}\t{3:.0f}\t{4:.0f}\t{5:.0f}\t{6:.3f}\t{7:.3f}\t{8:.3f}\t{9:.2f}\n'.format(s,p,l,r,c,b,x,y,z,v))

#*************************************************
''' read Train File '''
#*************************************************
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
def runNN(sensors, Cl, Root):
    if nnDef.useRegressor is False:
        nnTrainedData = Root + '.nnModelC.pkl'
    else:
        nnTrainedData = Root + '.nnModelR.pkl'
    print(' Running Neural Network: multi-layer perceptron (MLP) - (solver: ' + nnDef.nnSolver + ')...')
    
    sensors = nnDef.scaler.fit_transform(sensors)

    if nnDef.useRegressor is False:
        Y = nnDef.mlp.transform(Cl)
    else:
        Y = Cl

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
        print(' Retraining NN model...\n')
        if nnDef.useRegressor is False:
            clf = MLPClassifier(solver=nnDef.nnSolver, alpha=1e-5, hidden_layer_sizes=(nnDef.nnNeurons,), random_state=1)
        else:
            clf = MLPRegressor(solver=nnDef.nnSolver, alpha=1e-5, hidden_layer_sizes=(nnDef.nnNeurons,), random_state=9)
        clf.fit(sensors, Y)
        joblib.dump(clf, nnTrainedData)

    return clf

#*************************************************
''' Predict drive pattern '''
#*************************************************
def predictDrive(clf):
    np.set_printoptions(suppress=True)
    sp = [0,0]
    if params.debug is True:
        s,p,l,r,c,b,x,y,z,v = [-1,-1,116,117,111,158,0.224,0.108,1.004,1.5]
    else:
        s,p,l,r,c,b,x,y,z,v = piRC_lib.readAllSensors(params.useCamera)

    print(' S={0:.0f}, P={1:.0f}, L={2:.0f}, R={3:.0f}, C={4:.0f}, B={5:.0f}, X={6:.3f}, Y={7:.3f}, Z={8:.3f}, V={9:.2f}'.format(s,p,l,r,c,b,x,y,z,v))
    nowsensors = np.array([[round(l,0),round(r,0),round(c,0),round(b,0),round(x,3),round(y,3),round(z,3),round(v,2)]]).reshape(1,-1)

    if nnDef.useRegressor is False:
        nowsensors = nnDef.scaler.transform(nowsensors)
        try:
            sp[0] = nnDef.mlp.inverse_transform(clf.predict(nowsensors)[0])[0]
            sp[1] = nnDef.mlp.inverse_transform(clf.predict(nowsensors)[0])[1]
        except:
            sp = [0,0]
        print('\033[1m' + '\n Predicted classification value (Neural Networks) = ( S=',str(sp[0]),', P=',str(sp[1]),')')
        prob = clf.predict_proba(nowsensors)[0].tolist()
        print(' (probability = ' + str(round(100*max(prob),4)) + '%)\033[0m\n')
    else:
        sp = clf.predict(nowsensors)[0]
        print('\033[1m' + '\n Predicted regression value (Neural Networks) = ( S=',str(sp[0]),', P=',str(sp[1]),')')
        for k in range(2):
            if sp[k] >= 1:
                sp[k] = 1
            elif sp[k] <= -1:
                sp[k] = -1
            else:
                sp[k] = 0
        print('\033[1m' + ' Predicted regression value (Neural Networks) = ( S=',str(sp[0]),', P=',str(sp[1]),') Normalized\n')
        
    if nnDef.saveNewTrainingData is True:
        with open(params.filename, "a") as sum_file:
            sum_file.write('{0:.0f}\t{1:.0f}\t{2:.0f}\t{3:.0f}\t{4:.0f}\t{5:.0f}\t{6:.3f}\t{7:.3f}\t{8:.3f}\t{9:.3f}\n'.format(sp[0],sp[1],l,r,c,b,x,y,z,v))

    return sp[0], sp[1]

#*************************************************
''' Drive '''
#*************************************************
def drive(s,p):
    if params.debug is False:
        piRC_lib.runMotor(0,s)
        piRC_lib.runMotor(1,p)

def fullStop(type):
    if params.debug is False:
        piRC_lib.fullStop(type)

#*************************************************
''' Lists the program usage '''
#*************************************************
def usage():
    print('\n Usage:')
    print('\n Training (Classifier):\n  python3 piRC_ML.py -t <train file>')
    print('\n Prediction (Classifier):\n  python3 piRC_ML.py -r <train file>')
    print('\n Training (Regression):\n  python3 piRC_ML.py -t <train file> -R')
    print('\n Prediction (Regression):\n  python3 piRC_ML.py -r <train file> -R')
    print('\n Collect data from sensors into training file:\n  python3 piRC_ML.py -c')
    print('\n (Separate trained models are created for regression and classification)\n')

    print(' Requires python 3.x. Not compatible with python 2.x\n')

def exitProg():
    fullStop(True)
    sys.exit(2)

#*************************************************
''' Main initialization routine '''
#*************************************************
if __name__ == "__main__":
    sys.exit(main())
