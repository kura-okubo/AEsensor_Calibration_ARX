# AEsensor Calibration using ARX model
This repository contains the MATLAB function to conduct the sensor calibration using the autoregressive exogenous model (ARX) model, represented by poles and zeros, and an example to apply the response removal with the ARX model to the AE waveform. Jupyter notebooks are available to perform those processings above.

# Installation
You need a [MATLAB](https://www.mathworks.com/products/matlab.html) license to use the [lsq_arx.m](code/lsq_arx.m) to compute the poles and zeros using the least square method.

To run the notebook [01_AEsensor_calibration_arx.ipynb](code/01_AEsensor_calibration_arx.ipynb), you need to install

-  MATLAB R2020b or later
- jupyter lab (**NOTE:** do NOT open with the jupyter notebook, otherwise you will get an error.)
- jupyter-matlab-proxy (https://github.com/mathworks/jupyter-matlab-proxy)
- [Signal Processing Toolbox](https://www.mathworks.com/products/signal.html)

See [the installation guide of MATLAB kernel for jupyter notebook](https://github.com/mathworks/jupyter-matlab-proxy#installation).

**NOTE:** You need to export a path to the executable file of MATLAB such as `/Applications/MATLAB_R2021b.app/bin/matlab` to run it from the terminal.

To run the [02_Apply_removalresp_to_AEevent.ipynb](code/02_Apply_removalresp_to_AEevent.ipynb), you need to install

- numpy
- scipy
- [obspy](https://docs.obspy.org)

and the other basic modules. We handle the AE waveforms using the `obspy.core.trace.Trace`.

# Notebooks

- [01_AEsensor_calibration_arx.ipynb](code/01_AEsensor_calibration_arx.ipynb)
We conduct the AE sensor calibration with ARX model. We use the measurement with laser Doppler vibrometer (LDV) and the AE sensor as the input and output of the system, respectively.

- [02_Apply_removalresp_to_AEevent.ipynb](code/02_Apply_removalresp_to_AEevent.ipynb)
We demonstrate the application of the ARX model with poles and zeros to the AE waveform using [remove_resp_digitalfilt.py](code/remove_resp_digitalfilt.py).

- [convert_and_save_AEevent_fb03-087.ipynb](code/convert_and_save_AEevent_fb03-087.ipynb)
This notebook preprocesses the raw AE waveforms to use for the application of response removal.

# Gallery
<img src="figure/AEsensor_bode.png" alt="fig1" width="500"/>
Figure 1. Bode plot of the AE sensor.

<img src="figure/comparison_AEresponse_removal_OL07.png" alt="fig1" width="500"/>
Figure 2. Comparison before and after the response removal of the AE waveform.


# Reference
