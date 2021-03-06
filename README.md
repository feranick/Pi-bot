# Pi-bot (piRC)
**Raspberry Pi Remote-controlled/autonomous cars**. Different approaches for control and driving are available:
- Fully autonomous through deep learning neural networks 
- Driving aid, pseudo-automated (tries to avoid obstacles)
- Manual controlled via HTML interface

## Hardware
- robot: RC car with one motor for power, one motor for steering.
- controller: [Raspberry Pi 3 B](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/) or [3 B+](https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/). [Raspberry PI zero w](https://www.raspberrypi.org/products/pi-zero-w/)  can be used only with SKLearn and no camera.
- ADC controller: 4 channel 16bit, [ADS1115](http://www.ti.com/lit/ds/symlink/ads1115.pdf) (Op. Voltage: 3.3V)
- Accelerometer: XYZ, [ADXL345](http://www.analog.com/en/products/mems/accelerometers/adxl345.html) (Op. Voltage: 3.3V)
- Stepper motor controller: Adafruit [TB6612](https://learn.adafruit.com/adafruit-tb6612-h-bridge-dc-stepper-motor-driver-breakout/overview), 1.2A DC (Op. Voltage: 3.3V or 5V)
- Sensing the motor status requires a 1.5MOhm resistor to from the power motor leads to the ADS1115. 
- Sonars: 4 [HC-SR04](http://www.micropik.com/PDF/HCSR04.pdf) (left, right, center, back); (Op. Voltage: 5V)
  Warning: the output operating voltage is 5V, while RPi accepts only up to 3.3V, so you need a voltage divider.
- Radar (support is upcoming): 1 microwave Doppler Radar [HB100](https://www.tindie.com/products/limpkin/hb100-doppler-speed-sensor-arduino-compatible/)
- [Raspberry Pi Camera Module](https://www.raspberrypi.org/products/camera-module-v2/)
- Optional: [Google Coral EdgeTPU](https://coral.ai/docs/accelerator/get-started/) for on device efficient inference is supported. Please refer to the product page for installation.

- Deprecated IR sensors:
    - 2 front left side break beam sensors [3mm LEDs](https://www.adafruit.com/products/2167)
    - 1 front [GP2Y0A21YK0F](http://www.sharp-world.com/products/device/lineup/data/pdf/datasheet/gp2y0a21yk_e.pdf) Sharp IR Analog Distance Sensor 10-80cm

## Requirements
Since it uses Python3, it requires the following packages

    sudo apt-get install python3-rpi.gpio python3-dev python3-pip libopenjp2-7 libatlas-base-dev libtiff5 python3-picamera libhdf5-serial-dev libhdf5-dev

You would then need to install two libraries for the ADC (ADS1115) and accelerometer (ADXL345)

    sudo pip3 install adafruit-adxl345 adafruit-ads1x15 Pillow configparser wheel

Machine learing is carried out using Sklearn by default, which needs the following packages:

    sudo pip3 install numpy sklearn 
    
Alternatively and only when used with a Raspberry Pi 3, TensorFlow can be used instead. To install: 

    sudo pip3 install tensorflow tflite-runtime

## Installation
When inside teh folder `Pi-bot/piRC` from the command line:

    python3 setup.bdist_wheel
    sudo pip3 install --upgrade dist/pirc-xxxxxxxx-py3-none-any.whl  
    
You can also run the software directly from the folder (although it is discouraged).
    
- Upon booting Raspbian, the motors may not be responsive due to some GPIO channels not being properly initialized. Use (`piRC/other/pirc_init.py`) to initialize them.

## Usage
### piRC (deep learning neural networks)
All required parameters for ML and for the RC are included into `pirc.ini` which is included in Pi-bot/pirc. If not present, a default file is created upon launching the software.
 
This software (piRC/machine_learning/piRC_ML.py) is designed to accomplish three main tasks
- **Collection mode (CM)** Collect sensor data and save it into what will be a training file. When the software is operated with CM, the user is supposed to operate the RC in fully manual mode (i.e. using the original remote control. You can stop the collection by exiting with CTRL+C. The result is a file (`Training_splrcbxyz.txt`) with sensor readings that are ready for machine training. Examples are provided in `piRC/piRC_ML/Training` (it is strongly recommended to create your own). CM mode runs using this command:

    `pirc -c`

- **Training mode (TM)** Using the training file (for example `Training_splrcbxyz.txt`), a neural network training model is created and saved with the extension `.nnModelC.pkl`. Training can be conducted in the Rpi within the RC car itself, or in any other computer running python and related libraries. This usually is much much faster. TM mode runs using this command:

    `pirc -t <training file>`

- **Running mode (RM)** Once the training is completed, you can run run the inference mode (which uses sensor data acquired in real time to infer steering and power) and ultimately the RC car itself through this command

    `pirc -r Training_splrcbxyz.txt`

Both Classification (default) and Regression can be used.

A few notes on RM:
- If training model is not available, one is created at launch time.
- a bash script is provided (`piRC/machine_learning/syncTraining/syncTFile.sh`) to allow the transfer of the training file to a separate computer, run the training in that computer and retrieve the model for usage in the piRC.
- The training file can be improved while in RM by adding real time sensor data to it (the flag `saveNewTrainingData` needs to be set to True). This is useful as a new training model can be created on the fly (using the bash script as per the previous point). piRC_ML.py can be set to periorically reload (default is 15 seconds, change using `syncTimeLimit`) the training model without relaunching the script (the flag `syncTrainModel` needs to be set to True).
- Two Machine learning methodsare available: using the MultiPerceptron Classifier (`MLPClassifier`, recommended) or Regressor (`MLPRegressor`, highly experimental and not recommended). 
- Two operation modes are available, and can be enabled using the flab `runFullAuto`:
    - Partial Auto: piRC will only respond to the sensor data, but it will no proactively "drive forward" if it has no reason for it. You need to use manual commands to help it. 
    - Full Auto: piRC will proactively drive forward if it has been standing still for a given amount of time. 

### Manual control through web interface (discontinued)
piRC can be controlled using a web interface. Communication between PHP and python is done: 
- via shared file (piRC_file). Auto and manual control take place within the same python script
- via shell (piRC_nofile): Auto control is automated, in the background. Manual control is done via python script when the user 
is calling for an action.

### Additional utilities
- `pirc_init`: Initialize sensors and GPIO ports for full use with remote control.


### Installation (deprecated)
To be working properly, a library file piRC_lib.py needs to be copied inside each of the folders:
- piRC_file
- piRC_nofile
- piRC_ML
- Upon booting Raspbian, the motors may not be responsive due to some GPIO channels not being properly initialized. Use (piRC/other/pirc_init.py) to initialize them.
