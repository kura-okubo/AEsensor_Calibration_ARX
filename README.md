# AEsensor Calibration using ARX model
This repository contains the MATLAB function to conduct the sensor calibration using the autoregressive exogenous model (ARX) model, represented by poles and zeros, and an example to apply the response removal with the ARX model to the AE waveform. Jupyter notebooks are available to perform those processings above.

[![Run tests](https://github.com/kura-okubo/AEsensor_Calibration_ARX/actions/workflows/test.yml/badge.svg)](https://github.com/kura-okubo/AEsensor_Calibration_ARX/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/kura-okubo/AEsensor_Calibration_ARX/graph/badge.svg?token=1IQ6TJP65S)](https://codecov.io/gh/kura-okubo/AEsensor_Calibration_ARX)
[![DOI](https://zenodo.org/badge/677228393.svg)](https://zenodo.org/badge/latestdoi/677228393)
![GitHub all releases](https://img.shields.io/github/downloads/kura-okubo/AEsensor_Calibration_ARX/total?logo=github)


## List of Notebooks

<img src="figure/AEsensor_calib_schematic.png" alt="fig1" width="800"/>


- [01_AEsensor_calibration_arx.ipynb](src/01_AEsensor_calibration_arx.ipynb)
  <a href="https://nbviewer.org/github/kura-okubo/AEsensor_Calibration_ARX/blob/master/src/01_AEsensor_calibration_arx.ipynb" target="_blank">
   <img align="center"
      src="https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.png"
      width="109" height="20">
  </a>
  <br>
We conduct the calibration of the AE sensor using  Auto-Regressive eXogenous (ARX) model. We use the measurements of laser Doppler vibrometer (LDV) and the AE sensor as the input and output of the system, respectively.

- [02_Apply_removalresp_to_AEevent.ipynb](src/02_Apply_removalresp_to_AEevent.ipynb)
  <a href="https://nbviewer.org/github/kura-okubo/AEsensor_Calibration_ARX/blob/master/src/02_Apply_removalresp_to_AEevent.ipynb" target="_blank">
   <img align="center"
      src="https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.png"
      width="109" height="20">
  </a>
  <br>
We demonstrate the application of the ARX model with poles and zeros to the AE waveform using [src/remove_resp_digitalfilt.py](src/remove_resp_digitalfilt.py).

- [convert_and_save_AEevent_fb03-087.ipynb](src/convert_and_save_AEevent_fb03-087.ipynb)
This notebook preprocesses the raw AE waveforms to use for the application of response removal.


## Installation to run the notebooks

The easiest way to set up the environment for the notebooks is installing the dependencies using [Miniconda](https://docs.conda.io/projects/miniconda/en/latest/) ([Conda](https://docs.conda.io/projects/conda/en/stable/) also works, but miniconda is enough to execute the notebooks in this repo).

1. install the miniconda following the instruction in the website.

2. Clone the git repository and create the environment
Type the commands below in the terminal.
```sh
git clone https://github.com/kura-okubo/AEsensor_Calibration_ARX.git
cd AEsensor_Calibration_ARX
conda env create -n AEsensor_arx -f environment.yml
conda activate AEsensor_arx
python3 -m pip install jupyter-matlab-proxy
```
These commands download the repository in your local machine, create the environment with the dependencies used in the notebooks, and install the matlab kernel for the jupyter notebook.

3. Find the path to the MATLAB executable file by
```sh
which matlab
```
If the path to the executable e.g.
> /Applications/MATLAB_R2023a.app/bin/matlab

is returned, you are ready to execute the notebook. If not, export the path to the directory with matlab like
```sh
export PATH="$PATH:/Applications/MATLAB_R2023a.app/bin/"
```

4. Launch the Jupyter lab
Type in the terminal as following:
```sh
jupyter lab
```
Then, open the notebooks selecting from the side bar of the jupyter lab.


**NOTE:** The default browser to open the jupyter lab can be changed following [here](https://stackoverflow.com/a/47793764).


### Uninstall the environment
To remove (uninstall) the environment, run the followings:
```sh
conda deactivate
conda env remove -n AEsensor_arx
```

## Matlab license
To use the [src/lsq_arx.m](src/lsq_arx.m) and to execute the notebook of [01_AEsensor_calibration_arx.ipynb](src/01_AEsensor_calibration_arx.ipynb), you need a license for the followings:

- [MATLAB](https://www.mathworks.com/products/matlab.html) R2020b or later
- [Signal Processing Toolbox](https://www.mathworks.com/products/signal.html)

We use butterworth filter and [`tf2zpk`](https://www.mathworks.com/help/signal/ref/tf2zpk.html) implemented in the `Signal Processing Toolbox`.

## Gallery
<img src="figure/AEsensor_bode.png" alt="fig1" width="500"/>
Figure 1. Bode plot of the AE sensor.

<img src="figure/comparison_AEresponse_removal_OL07.png" alt="fig1" width="500"/>
Figure 2. Comparison before and after the response removal of the AE waveform.


# Reference
