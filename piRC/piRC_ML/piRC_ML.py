#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************************
*
* PiRC - Machine learning train and predict
* version: 20170511d
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

from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.externals import joblib
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler

#**********************************************
''' General parameters'''
#**********************************************
class params:
    timeDelay = 0.25
    debug = False # do not activate sensors or motors in debug mode
    filename = 'Training_splrcbxyz.txt'

#**********************************************
''' Neural Networks'''
#**********************************************
class nnDef:
    runNN = True
    nnAlwaysRetrain = False
    
    syncTimeLimit = 10  # time in seconds for NN model synchronization
    syncTrainModel = False
    saveNewTrainingData = False
    
    regressor = False

    scaler = StandardScaler()
    binarizer = MultiLabelBinarizer()

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
            nnDef.regressor = False
        elif sys.argv[3] in ("-R", "--Regressor"):
            nnDef.regressor = True
        else:
            runFullAuto = True
    except:
        nnDef.regressor = False
        runFullAuto = False

    for o, a in opts:
        if o in ("-r" , "--run"):
            try:
                runAuto(sys.argv[2],runFullAuto)
            except:
                exitProg()

        if o in ("-t" , "--train"):
            try:
                runTrain(sys.argv[2])
            except:
                sys.exit(2)

        if o in ("-c" , "--collect"):
            try:
                writeTrainFile()
            except:
                exitProg()

#************************************
''' runAuto '''
''' Use ML models to predict steer and power '''
#************************************
def runAuto(trainFile, type):
    trainFileRoot = os.path.splitext(trainFile)[0]
    Cl, sensors = readTrainFile(trainFile)
    clf = runNN(sensors, Cl, trainFileRoot)
    import piRC_lib
    #make sure motors are stopped
    piRC_lib.fullStop(False)
    syncTime = time()
    while True:
        if time() - syncTime > nnDef.syncTimeLimit and nnDef.syncTrainModel == True:
            print(" Synchronizing NN model...\n")
            clf = runNN(sensors, Cl, trainFileRoot)
            syncTime = time()
        
        if type == True:
            print(" Running \033[1mFull Auto\033[0m Mode\n")
            dt=0
            t1=time()
            while dt < 1:
                s, p = predictDrive(clf)
                if p != 0:
                    dt = 0
                else:
                    dt = time() - t1
                    drive(s,p)
                sleep(params.timeDelay)
            drive(0, 1)
            sleep(0.5)
        else:
            print(" Running \033[1mPartial Auto\033[0m Mode\n")
            s, p = predictDrive(clf)
            drive(s,p)
            sleep(params.timeDelay)

#************************************
''' runTrain '''
''' Use ML models to predict steer and power '''
#************************************
def runTrain(trainFile):
    trainFileRoot = os.path.splitext(trainFile)[0]
    Cl, sensors = readTrainFile(trainFile)
    nnDef.nnAlwaysRetrain = True
    runNN(sensors, Cl, trainFileRoot)

#****************************************
''' write training file from sensors '''
#****************************************
def writeTrainFile():
    while True:
        import piRC_lib
        s,p,l,r,c,b,x,y,z = piRC_lib.readAllSensors()
        print(' S={0:.0f}, P={1:.0f}, L={2:.0f}, R={3:.0f}, C={4:.0f}, B={5:.0f}, X={6:.3f}, Y={7:.3f}, Z={8:.3f}'.format(s,p,l,r,c,b,x,y,z))
        with open(params.filename, "a") as sum_file:
            sum_file.write('{0:.0f}\t{1:.0f}\t{2:.0f}\t{3:.0f}\t{4:.0f}\t{5:.0f}\t{6:.3f}\t{7:.3f}\t{8:.3f}\n'.format(s,p,l,r,c,b,x,y,z))

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
def runNN(sensors, Cl, Root):
    if nnDef.regressor is False:
        nnTrainedData = Root + '.nnModelC.pkl'
    else:
        nnTrainedData = Root + '.nnModelR.pkl'
    print(' Running Neural Network: multi-layer perceptron (MLP) - (solver: ' + nnDef.nnSolver + ')...')
    
    sensors = nnDef.scaler.fit_transform(sensors)

    if nnDef.regressor is False:
        Y = nnDef.binarizer.fit_transform(Cl)
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
        if nnDef.regressor is False:
            clf = MLPClassifier(solver=nnDef.nnSolver, alpha=1e-5, hidden_layer_sizes=(nnDef.nnNeurons,), random_state=1)
        else:
            clf = MLPRegressor(solver=nnDef.nnSolver, alpha=1e-5, hidden_layer_sizes=(nnDef.nnNeurons,), random_state=1)
        clf.fit(sensors, Y)
        joblib.dump(clf, nnTrainedData)

    return clf

#************************************
''' Predict drive pattern '''
#************************************
def predictDrive(clf):
    import piRC_lib
    sp = [0,0]
    s,p,l,r,c,b,x,y,z = piRC_lib.readAllSensors()
    print(' S={0:.0f}, P={1:.0f}, L={2:.0f}, R={3:.0f}, C={4:.0f}, B={5:.0f}, X={6:.3f}, Y={7:.3f}, Z={8:.3f}'.format(s,p,l,r,c,b,x,y,z))
    np.set_printoptions(suppress=True)
            
    if params.debug is True:
        nowsensors = np.array([[1.10,1.10,1.10,1.10,0.000,0.000,0.000]]).reshape(1,-1)
        #nowsensors = np.array([[1.10,1.10,1.10,1.10,0.028,0.236,0.952]]).reshape(1,-1)
    else:
        nowsensors = np.array([[round(l,0),round(r,0),round(c,0),round(b,0),round(x,3),round(y,3),round(z,3)]]).reshape(1,-1)

    if nnDef.regressor is False:
        nowsensors = nnDef.scaler.transform(nowsensors)
        try:
            sp[0] = nnDef.binarizer.inverse_transform(clf.predict(nowsensors))[0][0]
            sp[1] = nnDef.binarizer.inverse_transform(clf.predict(nowsensors))[0][1]
        except:
            sp = [0,0]
        print('\033[1m' + '\n Predicted classification value (Neural Networks) = ( S=',str(sp[0]),', P=',str(sp[1]),')')
        prob = clf.predict_proba(nowsensors)[0].tolist()
        print(' (probability = ' + str(round(100*max(prob),4)) + '%)\033[0m\n')
    else:
        sp = clf.predict(nowsensors)[0]
        for k in range(2):
            print(sp[k])
            if sp[k] >= 1:
                sp[k] = 1
            elif sp[k] <= -1:
                sp[k] = -1
            else:
                sp[k] = 0

        score = clf.score(sensors,Y)
        print('\033[1m' + '\n Predicted regression value (Neural Networks) = ( S=',str(sp[0]),', P=',str(sp[1]),')')
        print(' (R^2 = ' + str('{:.5f}'.format(score)) + ')\033[0m')
        
    if nnDef.saveNewTrainingData is True:
        with open(params.filename, "a") as sum_file:
            sum_file.write('{0:.0f}\t{1:.0f}\t{2:.0f}\t{3:.0f}\t{4:.0f}\t{5:.0f}\t{6:.3f}\t{7:.3f}\t{8:.3f}\n'.format(sp[0],sp[1],l,r,c,b,x,y,z))

    return sp[0], sp[1]

#************************************
''' Drive '''
#************************************
def drive(s,p):
    import piRC_lib
    piRC_lib.runMotor(0,s)
    piRC_lib.runMotor(1,p)

#************************************
''' Lists the program usage '''
#************************************
def usage():
    print('\n Usage:')
    print('\n Training (Classifier):\n  python3 piRC_ML.py -t <train file>')
    print('\n Prediction (Classifier):\n  python3 piRC_ML.py -r <train file>')
    print('\n Training (Regression):\n  python3 piRC_ML.py -t <train file> -R')
    print('\n Prediction (Regression):\n  python3 piRC_ML.py -r <train file> -R')
    print('\n Collect data from sensors into training file:\n  python3 piRC_ML.py -c')
    print('\n (Separate trained models are created for regression and classification\n')

    print(' Requires python 3.x. Not compatible with python 2.x\n')

def exitProg():
    import piRC_lib
    piRC_lib.fullStop(True)
    sys.exit(2)

#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
