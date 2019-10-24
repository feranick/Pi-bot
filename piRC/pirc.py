#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************************
* PiRC - Self-driving RC car via Machine Learning
* version: 20191023c
* By: Nicola Ferralis <feranick@hotmail.com>
***********************************************************
'''
print(__doc__)

import numpy as np
import sys, os.path, os, getopt, glob, csv, joblib, configparser
import h5py, pickle
from time import sleep, time
from os.path import exists, splitext
from os import rename
from datetime import datetime, date

from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.preprocessing import StandardScaler
#import libpirc #Comment this out for debug mode.

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
            
        if self.ML_framework == "SKLearn":
            self.runNN_SK = True
            self.runNN_TF = False
        if self.ML_framework == "TF":
            self.runNN_SK = False
            self.runNN_TF = True
    
        self.scaler = StandardScaler()
        self.scalFileExt = '_scaler.pkl'
        self.mlp = MultiClassReductor()
        
        if not self.debug:
            importModule("libpirc")
            
    def pircDef(self):
        self.conf['Parameters'] = {
            'timeDelay' : .25,
            'runFullAuto' : True,
            'useCamera' : True,
            'nnAlwaysRetrain': True,
            'syncTimeLimit': 20, # time in seconds for NN model synchronization
            'syncTrainModel': False,
            'saveNewTrainingData': True,
            'ML_framework': 'SKLearn',     # Use either: SKLearn (for scikit-learn) or TF (for TensorFlow)
            'useRegressor': False,
            'HL': [270,170,70,10],
            'l2' : 1e-5,
            'epochs' : 200,
            }
            
        self.conf['SKLearn'] = {
            'nnSolver': 'lbfgs',  #Solver for NN lbfgs preferred for small datasets. Alternatives: 'adam' or 'sgd'
            }
            
        self.conf['TF'] = {
            'l_rate' : 0.001,
            'l_rdecay' : 1e-4,
            'drop' : 0,
            'cv_split' : 0.01,
            'fullSizeBatch' : True,
            'batch_size' : 64,
            }
            
        self.conf['System'] = {
            'makeQuantizedTFlite' : False,
            'useTFlitePred' : False,
            'TFliteRuntime' : False,
            'debug': False, # do not activate sensors or motors in debug mode
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
            self.ML_framework = self.conf.get('Parameters','ML_framework')
            self.useRegressor = self.conf.getboolean('Parameters','useRegressor')
            self.HL = eval(self.pircDef['HL'])
            self.l2 = self.conf.getfloat('Parameters','l2')
            self.epochs = self.conf.getint('Parameters','epochs')
            
            self.nnSolver = self.conf.get('SKLearn','nnSolver')
            
            self.l_rate = self.conf.getfloat('TF','l_rate')
            self.l_rdecay = self.conf.getfloat('TF','l_rdecay')
            self.drop = self.conf.getfloat('TF','drop')
            self.cv_split = self.conf.getfloat('TF','cv_split')
            self.fullSizeBatch = self.conf.getboolean('TF','fullSizeBatch')
            self.batch_size = self.conf.getint('TF','batch_size')
            
            self.makeQuantizedTFlite = self.conf.getboolean('System','makeQuantizedTFlite')
            self.useTFlitePred = self.conf.getboolean('System','useTFlitePred')
            self.TFliteRuntime = self.conf.getboolean('System','TFliteRuntime')
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

    for o, a in opts:
        if o in ("-r" , "--run"):
            try:
                runAuto(sys.argv[2],params.runFullAuto)
            except:
                exitProg()

        if o in ("-t" , "--train"):
            try:
                runTrain(sys.argv[2])
            except:
                exitProg()

        if o in ("-c" , "--collect"):
            try:
                writeTrainFile()
            except:
                exitProg()

#*************************************************
''' seletMLFramework '''
''' Select and initialize appropriate framework '''
#*************************************************
def selectMLFramework(sensors, Cl, trainFileRoot):
    params = Conf()
    printParams()
    if params.runNN_SK:
        #print(" Using SKLearn")
        model = runNN_SK(sensors, Cl, trainFileRoot)
    if params.runNN_TF:
        if not params.TFliteRuntime:
            import tensorflow as tf
            if params.useTFlitePred:
                # model here is intended as interpreter
                model = tf.lite.Interpreter(model_path=os.path.splitext(fileTrainingData(trainFileRoot, True))[0]+'.tflite')
                model.allocate_tensors()
            else:
                model = tf.keras.models.load_model(fileTrainingData(trainFileRoot, True))
        else:
            import tflite_runtime.interpreter as tflite
            # model here is intended as interpreter
            model = tflite.Interpreter(model_path=os.path.splitext(fileTrainingData(trainFileRoot, True))[0]+'.tflite')
            model.allocate_tensors()
    return model

#*************************************************
''' runAuto '''
''' Use ML models to predict steer and power '''
#*************************************************
def runAuto(trainFile, type):
    params = Conf()
    trainFileRoot = os.path.splitext(trainFile)[0]
    Cl, sensors = readTrainFile(trainFile)
    model = selectMLFramework(sensors, Cl, trainFileRoot)
    scal = pickle.loads(open(trainFileRoot+params.scalFileExt, "rb").read())
    fullStop(False)
    syncTime = time()
    while True:
        if time() - syncTime > params.syncTimeLimit and params.syncTrainModel == True:
            print(" Reloading NN model...")
            #model = selectMLFramework(sensors, Cl, trainFileRoot)
            print(" Synchronizing NN model...\n")
            os.system("./syncTFile.sh " + trainFileRoot + " &")
            syncTime = time()
        
        if type == False:
            print(" Running \033[1mPartial Auto\033[0m Mode\n")
            s, p = predictDrive(model, scal, fileTrainingData(trainFileRoot, False))
            drive(s,p)
            sleep(params.timeDelay)
        else:
            print(" Running \033[1mFull Auto\033[0m Mode\n")
            dt=0
            t1=time()
            while dt < 0.5:
                s, p = predictDrive(model, scal, fileTrainingData(trainFileRoot, False))
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
    printParams()
    if params.runNN_SK:
        #print(" Using SKlearn")
        runNN_SK(sensors, Cl, trainFileRoot)
    if params.runNN_TF:
        #print(" Using TensorFlow")
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
    nnTrainedData = fileTrainingData(Root, True)
    print("\n Training file:", nnTrainedData)

    try:
        if params.nnAlwaysRetrain == False:
            with open(nnTrainedData):
                print(' Opening NN training model...\n')
                model = joblib.load(nnTrainedData)
            print("\n Done. Training model loaded")
        else:
            raise ValueError("\n Force NN retraining.")
    except:
        #**********************************************
        ''' Retrain data if not available'''
        #**********************************************
        print("\n Retraining NN model...")
        
        params.scaler.fit(sensors)
        sensors = params.scaler.transform(sensors)
        
        with open(Root+params.scalFileExt, 'ab') as g:
            g.write(pickle.dumps(params.scaler))
        print("\n Scaling model saved in: ",nnTrainedData)
            
        
        if params.useRegressor is False:
            Y = params.mlp.transform(Cl)
            #print(params.mlp.classes_())
        else:
            Y = Cl
        
        if params.useRegressor is False:
            model = MLPClassifier(solver=params.nnSolver, hidden_layer_sizes=params.HL, random_state=1,
                alpha = params.l2, max_iter = params.epochs)
        else:
            model = MLPRegressor(solver=params.nnSolver, hidden_layer_sizes=params.HL, random_state=9,
                alpha = params.l2, max_iter = params.epochs)
        model.fit(sensors, Y)
        joblib.dump(model, nnTrainedData)
    
    print("\n Done. Training model saved in: ",nnTrainedData,"\n")

    return model

#********************************************************************************
''' Run Neural Network '''
#********************************************************************************
def runNN_TF(sensors, Cl, Root):
    params = Conf()
    nnTrainedData = fileTrainingData(Root, True)
    print("\n Training file:", nnTrainedData)

    try:
        import tensorflow as tf
        import tensorflow.keras as keras  #tf.keras
        
        
        
        if params.nnAlwaysRetrain == False:
            print("\n Opening NN training model...")
            model = keras.models.load_model(nnTrainedData)
            print("\n Done. Training model loaded\n")
        else:
            raise ValueError("\n Force NN retraining.")
    except:
        #**********************************************
        ''' Retrain data if not available'''
        #**********************************************
        print("\n Retraining NN model...")
        #tf.compat.v1.Session(config=conf)
        
        params.scaler.fit(sensors)
        sensors = params.scaler.transform(sensors)
        with open(Root+params.scalFileExt, 'ab') as g:
            g.write(pickle.dumps(params.scaler))
        
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
            model.add(keras.layers.Dense(2))
            model.compile(loss='mse',
            optimizer=optim,
            metrics=['mae'])
        else:
            model.add(keras.layers.Dense(params.mlp.num_classes_(), activation = 'softmax'))
            model.compile(loss='categorical_crossentropy',
                optimizer=optim,
                metrics=['accuracy'])
    
        tbLog = keras.callbacks.TensorBoard(log_dir=params.tf_directory,
                write_graph=True, write_images=True)
        tbLogs = [tbLog]
                
        log = model.fit(sensors, Y,
            epochs=params.epochs,
            batch_size=params.batch_size,
            callbacks = tbLogs,
            verbose=2)
                
        model.save(nnTrainedData)
        
        if params.makeQuantizedTFlite:
            makeQuantizedTFmodel(sensors, model, nnTrainedData)
        
        print("\n Training with TensorFlow v.",tf.version.VERSION)
        print("\n Done. Training model saved in: ",nnTrainedData,"\n")

    return model

#*************************************************
''' Predict drive pattern '''
#*************************************************
def predictDrive(model, scal, root):
    params = Conf()
    np.set_printoptions(suppress=True)
    sp = [0,0]
    if params.debug is True:
        data = [0,0,254.36,36.73,132.25,124.67,
                0,0,0,0,149,151,147,141,139,99,87,82,98,101,181,157,
                179,116,136,108,91,83,90,76,124,141,174,93,131,90,86,
                85,81,63,158,140,138,88,126,60,74,78,74,59,183,191,158,
                147,143,81,83,86,81,63,119,129,144,181,158,163,115,93,
                85,69,28,175,171,85,199,209,106,85,79,99,9,183,176,124,
                218,168,85,106,78,109,145,207,149,129,233,171,81,101,85,
                84,196,205,123,134,208,138,67,96,79,103]
    else:
        data = libpirc.readAllSensors(params.useCamera)

    print(' S={0:.0f}, P={1:.0f}, L={2:.0f}, R={3:.0f}, C={4:.0f}, B={5:.0f}, X={6:.3f}, Y={7:.3f}, Z={8:.3f}, V={9:.2f}'.format(\
            data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9]))

    nowsensors = np.array([[round(data[2],0),round(data[3],0),round(data[4],0),round(data[5],0),
        round(data[6],3),round(data[7],3),round(data[8],3),round(data[9],2)]])

    if params.useCamera == True:
        nowsensors = np.append(nowsensors, data[10:]).reshape(1,-1)

    if params.useRegressor:
        if params.ML_framework == "SKLearn":
            sp = model.predict(nowsensors)[0]
        if params.ML_framework == "TF":
            if params.useTFlitePred:
                sp = getPredictions(nowsensors, model)
            else:
                sp = model.predict(R).flatten()[0]
        
        print('\033[1m' + ' Predicted regression = ( S=',str(sp[0]),', P=',str(sp[1]),')')
        for k in range(2):
            if sp[k] >= 1:
                sp[k] = 1
            elif sp[k] <= -1:
                sp[k] = -1
            else:
                sp[k] = 0
        print('\033[1m' + ' Predicted regression = ( S=',str(sp[0]),', P=',str(sp[1]),') Normalized\n')
    else:
        nowsensors = scal.transform(nowsensors)
        try:
            if params.ML_framework == "SKLearn":
                predictions = model.predict(nowsensors)
                sp = params.mlp.inverse_transform(predictions[0])
                prob = model.predict_proba(nowsensors)[0].tolist()
                predProb = round(100*max(prob),2)
            if params.ML_framework == "TF":
                if params.useTFlitePred:
                    predictions = getPredictions(nowsensors, model)
                else:
                    predictions = model.predict(R, verbose=0)
                    
                pred_class = np.argmax(predictions)
                sp = params.mlp.inverse_transform(pred_class)
                predProb = round(100*predictions[0][pred_class],2)
            
        except:
            print("FAIL")
            sp = [0,0]
            predProb = 0
                    
        print('\033[1m' + ' Predicted classification = ( S=',str(sp[0]),', P=',str(sp[1]),') (prob = ' + str(predProb) + '%)\033[0m\n')
        #print(' (prob = ' + str(predProb) + '%)\033[0m\n')
        
    if params.saveNewTrainingData is True:
        with open(params.filename, "a") as sum_file:
            np.savetxt(sum_file, [data], fmt="%.2f", delimiter=' ', newline='\n')

    return sp[0], sp[1]
    
#************************************
# Print NN Info
#************************************
def printParams():
    params = Conf()
    if params.ML_framework == 'TF':
        if not params.TFliteRuntime:
            if not params.useTFlitePred:
                print("  Importing TensorFlow...")
                framework = "TensorFlow"
            if params.useTFlitePred:
                print("  Importing TensorFlowLite...")
                framework = "TensorFlowLite"
            import tensorflow as tf
            version = tf.version.VERSION
        else:
            print("  Importing TensorFlowLite Runtime...")
            framework = "TensorFlowLite Runtime"
            version = 0
    else:
        framework = params.ML_framework
        version = 0
        
    print('\n  ================================================')
    print('  \033[1mNeural Network\033[0m - Parameters')
    print('  ================================================')
    print('  ML Framework:',framework)
    print('  Framework version:', version)
    print('  Optimizer:',params.nnSolver,
            '\n  Activation function:','relu',
            '\n  Hidden layers:', params.HL,
            '\n  Epochs:',params.epochs,
            '\n  L2:',params.l2,
            '\n  Dropout (TF):', params.drop,
            '\n  Learning rate (TF):', params.l_rate,
            '\n  Learning decay rate (TF):', params.l_rdecay)
    print('  ================================================\n')


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
        
#************************************
### Create Quantized tflite model
#************************************
def makeQuantizedTFmodel(A, model, model_name):
    params = Conf()
    import tensorflow as tf
    import tensorflow.keras as keras  #tf.keras
        
    print("\n  Creating quantized TensorFlowLite Model...\n")
    def representative_dataset_gen():
        for i in range(A.shape[0]):
            yield [A[i:i+1].astype(np.float32)]
    try:
        converter = tf.lite.TFLiteConverter.from_keras_model(model)    # TensorFlow 2.x
    except:
        converter = tf.lite.TFLiteConverter.from_keras_model_file(model_name)  # TensorFlow 1.x

    #converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.optimizations = [tf.lite.Optimize.OPTIMIZE_FOR_LATENCY]
    #converter.optimizations = [tf.lite.Optimize.OPTIMIZE_FOR_SIZE]
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
    converter.inference_input_type = tf.uint8
    converter.inference_output_type = tf.uint8
    converter.representative_dataset = representative_dataset_gen
    tflite_quant_model = converter.convert()

    with open(os.path.splitext(model_name)[0]+'.tflite', 'wb') as o:
        o.write(tflite_quant_model)

#************************************
# Make prediction based on framework
#************************************
def getPredictions(R, interpreter):
    params = Conf()
    #interpreter.allocate_tensors()
    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Test model on random input data.
    input_shape = input_details[0]['shape']
    input_data = np.array(R, dtype=np.float32)
    interpreter.set_tensor(input_details[0]['index'], input_data)

    interpreter.invoke()

    # The function `get_tensor()` returns a copy of the tensor data.
    # Use `tensor()` in order to get a pointer to the tensor.
    predictions = interpreter.get_tensor(output_details[0]['index'])[0][0]
        
    return predictions

#*************************************************
# Define File Training Data
#*************************************************
def fileTrainingData(Root, verbose):
    params = Conf()
    if params.ML_framework == "SKLearn":
        if params.useRegressor:
            nnTrainedData = Root + '.nnModelR.pkl'
            if verbose:
                print("\n Running multi-layer perceptron (SKLearn) - Regression")
        else:
            nnTrainedData = Root + '.nnModelC.pkl'
            if verbose:
                print("\n Running multi-layer perceptron (SKLearn) - Classification")
    elif params.ML_framework == "TF":
        if params.useRegressor:
            nnTrainedData = Root + '.nnModelR.h5'
            if verbose:
                print("\n Running multi-layer perceptron (TensorFlow) - Regression")
        else:
            nnTrainedData = Root + '.nnModelC.h5'
            if verbose:
                print("\n Running multi-layer perceptron (TensorFlow) - Classification")
    else:
        nnTrainedData = Root
    return nnTrainedData

#*************************************************
# Lists the program usage
#*************************************************
def usage():
    print('\n Usage:')
    print('\n Training:\n  python3 pirc.py -t <train file>')
    print('\n Prediction:\n  python3 pirc.py -r <train file>')
    print('\n Collect data from sensors into training file:\n  python3 pirc.py -c')
    print('\n (Separate trained models are created for regression and classification)\n')

    print(' Requires python 3.x. Not compatible with python 2.x\n')

def exitProg():
    fullStop(True)
    sys.exit(2)

def importModule(module_name):
    globals()[module_name] = __import__(module_name)

#*************************************************
''' Main initialization routine '''
#*************************************************
if __name__ == "__main__":
    sys.exit(main())
