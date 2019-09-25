#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************************
*
* PiRC - Self-driving RC car via Machine Learning
* version: 20190925c
*
* By: Nicola Ferralis <feranick@hotmail.com>
*
***********************************************************
'''
print(__doc__)

import numpy as np
import sys, os.path, os, getopt, glob, csv, joblib, configparser
from time import sleep, time
from os.path import exists, splitext
from os import rename
from datetime import datetime, date

from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.preprocessing import StandardScaler
import libpirc #Comment this out for debug mode.

#***************************************************
# This is needed for installation through pip
#***************************************************
def pirc():
    main()

#************************************
# Parameters
#************************************
class Conf():
    def __init__(self):
        confFileName = "pirc.ini"
        self.configFile = os.getcwd()+"/"+confFileName
        self.conf = configparser.ConfigParser()
        self.conf.optionxform = str
        self.tf_directory = "TF_MLP"
        if os.path.isfile(self.configFile) is False:
            print(" Configuration file: \""+confFileName+"\" does not exist: Creating one.\n")
            self.createConfig()
        self.readConfig(self.configFile)
        
        if self.useCamera == True:
            self.filename = 'Training_splrcbxyzvCam.txt'
            self.camStr = "ON"
        else:
            self.filename = 'Training_splrcbxyzv.txt'
            self.camStr = "OFF"
    
        self.scaler = StandardScaler()
        self.mlp = MultiClassReductor()
            
    def pircDef(self):
        self.conf['Parameters'] = {
            'timeDelay' : .25,
            'runFullAuto' : False,
            'useCamera' : False,
            'nnAlwaysRetrain': False,
            'syncTimeLimit': 20, # time in seconds for NN model synchronization
            'syncTrainModel': False,
            'saveNewTrainingData': False,
            'useRegressor': False,
            'HL': [10,],
            }
            
        self.conf['SKLearn'] = {
            'runNN_SK': True,
            'nnSolver': 'lbfgs',  #Solver for NN lbfgs preferred for small datasets. Alternatives: 'adam' or 'sgd'
            }
            
        self.conf['TF'] = {
            'runNN_TF': False,
            'l_rate' : 0.001,
            'l_rdecay' : 1e-4,
            'drop' : 0,
            'l2' : 1e-4,
            'epochs' : 100,
            'cv_split' : 0.01,
            'fullSizeBatch' : True,
            'batch_size' : 64,
            }
            
        self.conf['System'] = {
            'debug': False, # do not activate sensors or motors in debug mode
            #'useTFKeras' : False,
            #'setMaxMem' : False,   # TensorFlow 2.0
            #'maxMem' : 4096,       # TensorFlow 2.0
            }
            

    def readConfig(self,configFile):
        try:
            self.conf.read(configFile)
            self.pircDef = self.conf['Parameters']
            self.sklearnDef = self.conf['SKLearn']
            self.TF = self.conf['TF']
            self.sysDef = self.conf['System']
            
            self.timeDelay = self.conf.getfloat('Parameters','timeDelay')
            self.runFullAuto = self.conf.getboolean('Parameters','runFullAuto')
            self.useCamera = self.conf.getboolean('Parameters','useCamera')
            self.nnAlwaysRetrain = self.conf.getboolean('Parameters','nnAlwaysRetrain')
            self.syncTimeLimit = self.conf.getint('Parameters','syncTimeLimit')
            self.syncTrainModel = self.conf.getboolean('Parameters','syncTrainModel')
            self.saveNewTrainingData = self.conf.getboolean('Parameters','saveNewTrainingData')
            self.useRegressor = self.conf.getboolean('Parameters','useRegressor')
            self.HL = eval(self.pircDef['HL'])
            
            self.runNN_SK = self.conf.getboolean('SKLearn','runNN_SK')
            self.nnSolver = self.conf.get('SKLearn','nnSolver')
            
            self.runNN_TF = self.conf.getboolean('TF','runNN_TF')
            self.l_rate = self.conf.getfloat('TF','l_rate')
            self.l_rdecay = self.conf.getfloat('TF','l_rdecay')
            self.drop = self.conf.getfloat('TF','drop')
            self.l2 = self.conf.getfloat('TF','l2')
            self.epochs = self.conf.getint('TF','epochs')
            self.cv_split = self.conf.getfloat('TF','cv_split')
            self.fullSizeBatch = self.conf.getboolean('TF','fullSizeBatch')
            self.batch_size = self.conf.getint('TF','batch_size')
            
            self.debug = self.conf.getboolean('System','debug')
            
        except:
            print(" Error in reading configuration file. Please check it\n")

    # Create configuration file
    def createConfig(self):
        try:
            self.pircDef()
            with open(self.configFile, 'w') as configfile:
                self.conf.write(configfile)
        except:
            print("Error in creating configuration file")

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
        
    def classes_(self):
        return self.totalClass
        
    def num_classes_(self):
        return len(self.totalClass)


#**********************************************
''' Main '''
#**********************************************
def main():
    params = Conf()
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
            params.useRegressor = False
        elif sys.argv[3] in ("-R", "--Regressor"):
            params.useRegressor = True
    except:
        params.useRegressor = False

    for o, a in opts:
        if o in ("-r" , "--run"):
            try:
                runAuto(sys.argv[2],params.runFullAuto)
            except:
                exitProg()

        if o in ("-t" , "--train"):
            #try:
            runTrain(sys.argv[2])
            #except:
            #    exitProg()

        if o in ("-c" , "--collect"):
            try:
                writeTrainFile()
            except:
                exitProg()

#*************************************************
''' runAuto '''
''' Use ML models to predict steer and power '''
#*************************************************
def runAuto(trainFile, type):
    params = Conf()
    trainFileRoot = os.path.splitext(trainFile)[0]
    Cl, sensors = readTrainFile(trainFile)
    clf = runNN(sensors, Cl, trainFileRoot)
    fullStop(False)
    syncTime = time()
    while True:
        if time() - syncTime > params.syncTimeLimit and params.syncTrainModel == True:
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
    params = Conf()
    trainFileRoot = os.path.splitext(trainFile)[0]
    Cl, sensors = readTrainFile(trainFile)
    params.nnAlwaysRetrain = True
    if params.runNN_SK:
        print(" Using SKlearn")
        runNN_SK(sensors, Cl, trainFileRoot)
    if params.runNN_TF:
        print(" Using TensorFlow")
        runNN_TF(sensors, Cl, trainFileRoot)

#*************************************************
''' write training file from sensors '''
#*************************************************
def writeTrainFile():
    params = Conf()
    while True:
        data = libpirc.readAllSensors(params.useCamera)
        print(' S={0:.0f}, P={1:.0f}, L={2:.0f}, R={3:.0f}, C={4:.0f}, B={5:.0f}, X={6:.3f}, Y={7:.3f}, Z={8:.3f}, V={9:.2f}, Cam={10:s}'.format(\
        data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],params.camStr))
        with open(params.filename, "ab") as sum_file:
            np.savetxt(sum_file, [data], fmt="%.2f", delimiter=' ', newline='\n')

#*************************************************
''' read Train File '''
#*************************************************
def readTrainFile(trainFile):
    params = Conf()
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
def runNN_SK(sensors, Cl, Root):
    params = Conf()
    if params.useRegressor is False:
        nnTrainedData = Root + '.nnModelC.pkl'
    else:
        nnTrainedData = Root + '.nnModelR.pkl'
    print(' Running Neural Network: multi-layer perceptron (MLP) - (solver: ' + params.nnSolver + ')...\n')

    try:
        if params.nnAlwaysRetrain == False:
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
        
        sensors = params.scaler.fit_transform(sensors)
        if params.useRegressor is False:
            Y = params.mlp.transform(Cl)
            #print(params.mlp.classes_())
        else:
            Y = Cl
        
        if params.useRegressor is False:
            clf = MLPClassifier(solver=params.nnSolver, alpha=1e-5, hidden_layer_sizes=params.HL, random_state=1)
        else:
            clf = MLPRegressor(solver=params.nnSolver, alpha=1e-5, hidden_layer_sizes=params.HL, random_state=9)
        clf.fit(sensors, Y)
        joblib.dump(clf, nnTrainedData)

    return clf

#********************************************************************************
''' Run Neural Network '''
#********************************************************************************
def runNN_TF(sensors, Cl, Root):
    params = Conf()
    if params.useRegressor is False:
        nnTrainedData = Root + '.nnModelC.h5'
    else:
        nnTrainedData = Root + '.nnModelR.h5'
    print(' Running Neural Network: multi-layer perceptron (MLP) - Using TensorFlow...\n')

    try:
        import tensorflow as tf
        import h5py, pickle
        import tensorflow.keras as keras  #tf.keras
        if params.nnAlwaysRetrain == False:
            print(' Opening NN training model...\n')
            model = keras.models.load_model(nnTrainedData)
            print("\nDone. Training model loaded\n")
        else:
            raise ValueError('Force NN retraining.')
    except:
        #**********************************************
        ''' Retrain data if not available'''
        #**********************************************
        print(' Retraining NN model...\n')
        #tf.compat.v1.Session(config=conf)
        
        sensors = params.scaler.fit_transform(sensors)
        print(params.mlp.num_classes_())
        
        if params.useRegressor is False:
            Y = params.mlp.transform(Cl)
            Y = keras.utils.to_categorical(Y, num_classes=params.mlp.num_classes_())
        else:
            Y = Cl
            
        if params.fullSizeBatch == True:
            params.batch_size = sensors.shape[0]
                    
        optim = keras.optimizers.Adam(lr=params.l_rate, beta_1=0.9,
        beta_2=0.999, epsilon=1e-08, decay=params.l_rdecay,
        amsgrad=False)
        
        #************************************
        ### Build model
        #************************************
        model = keras.models.Sequential()
        for i in range(len(params.HL)):
            model.add(keras.layers.Dense(params.HL[i],
                activation = 'relu',
                input_dim=sensors.shape[1],
                kernel_regularizer=keras.regularizers.l2(params.l2)))
            model.add(keras.layers.Dropout(params.drop))
        
        if params.useRegressor:
            model.add(keras.layers.Dense(1))
            model.compile(loss='mse',
            optimizer=optim,
            metrics=['mae'])
        else:
            model.add(keras.layers.Dense(params.mlp.num_classes_(), activation = 'softmax'))
            model.compile(loss='categorical_crossentropy',
                optimizer=optim,
                metrics=['accuracy'])
    
        tbLog = keras.callbacks.TensorBoard(log_dir=params.tf_directory, histogram_freq=120,
                batch_size=params.batch_size,
                write_graph=True, write_grads=True, write_images=True)
        tbLogs = [tbLog]
                
        log = model.fit(sensors, Y,
            epochs=params.epochs,
            batch_size=params.batch_size,
            callbacks = tbLogs,
            verbose=2)
                
        model.save(nnTrainedData)
        
        print("\nDone. Training model saved in: ",nnTrainedData,"\n")

    return model

#*************************************************
''' Predict drive pattern '''
#*************************************************
def predictDrive(clf):
    params = Conf()
    np.set_printoptions(suppress=True)
    sp = [0,0]
    if params.debug is True:
        data = [-1,-1,116,117,111,158,0.224,0.108,1.004,1.5]
    else:
        data = libpirc.readAllSensors(params.useCamera)

    print(' S={0:.0f}, P={1:.0f}, L={2:.0f}, R={3:.0f}, C={4:.0f}, B={5:.0f}, X={6:.3f}, Y={7:.3f}, Z={8:.3f}, V={9:.2f}'.format(\
            data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9]))

    nowsensors = np.array([[round(data[2],0),round(data[3],0),round(data[4],0),round(data[5],0),
        round(data[6],3),round(data[7],3),round(data[8],3),round(data[9],2)]])

    if params.useCamera == True:
        nowsensors = np.append(nowsensors, data[10:]).reshape(1,-1)

    if params.useRegressor is False:
        nowsensors = params.scaler.transform(nowsensors)
        try:
            sp[0] = params.mlp.inverse_transform(clf.predict(nowsensors)[0])[0]
            sp[1] = params.mlp.inverse_transform(clf.predict(nowsensors)[0])[1]
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
        
    if params.saveNewTrainingData is True:
        with open(params.filename, "a") as sum_file:
            sum_file.write('{0:.0f}\t{1:.0f}\t{2:.0f}\t{3:.0f}\t{4:.0f}\t{5:.0f}\t{6:.3f}\t{7:.3f}\t{8:.3f}\t{9:.3f}\n'.format(sp[0],sp[1],l,r,c,b,x,y,z,v))

    return sp[0], sp[1]

#*************************************************
''' Drive '''
#*************************************************
def drive(s,p):
    if Conf().debug is False:
        libpirc.runMotor(0,s)
        libpirc.runMotor(1,p)

def fullStop(type):
    if Conf().debug is False:
        libpirc.fullStop(type)

#*************************************************
''' Lists the program usage '''
#*************************************************
def usage():
    print('\n Usage:')
    print('\n Training (Classifier):\n  python3 pirc.py -t <train file>')
    print('\n Prediction (Classifier):\n  python3 pirc.py -r <train file>')
    print('\n Training (Regression):\n  python3 pirc.py -t <train file> -R')
    print('\n Prediction (Regression):\n  python3 pirc.py -r <train file> -R')
    print('\n Collect data from sensors into training file:\n  python3 pirc.py -c')
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
