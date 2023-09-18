# Test script for remove_resp_digitalfilt.py

import os
import numpy as np
import scipy.io as sio

import obspy
from obspy import read, Stream, Trace
from obspy.signal.util import _npts2nfft
from obspy.core.utcdatetime import UTCDateTime

from pytest import approx
from src.remove_resp_digitalfilt import remove_resp_digitalfilt

UTCDateTime.DEFAULT_PRECISION = 8

def test_responseremoval():

    # Read the event trace
    tr = read("./data/AE_waveform_fb03-087_OL07.sac")[0]

    # Read response of AE sensor
    D = sio.loadmat("./data/AE_resp_dataandcoef");
    D.keys()
    # remove response using the function
    poles_AE = np.squeeze(D["p"])
    zeros_AE = np.squeeze(D["z"])
    scale_fac_AE = np.squeeze(D["k"])

    pre_filt = (5e3, 1e4, 1e6, 2e6) # prefilter for the remove_resp
    water_level = 60 # waterlevel [dB] for the remove_resp

    tr_respremoved, freqs, freq_domain_taper, data_after_freqtapered, freq_response_forward, freq_response = remove_resp_digitalfilt(tr, poles_AE, zeros_AE, scale_fac_AE, pre_filt=pre_filt, water_level=60, zero_mean=True,
        taper=True, taper_fraction=0.05, detrend=True, debug=True)

    # read pre-computed true data
    truedata = np.load("./data/testdata_remove_resp_digitalfilt.npz")

    assert np.linalg.norm(tr_respremoved.data - truedata["data"]) < 1e-12
    assert np.linalg.norm(freqs - truedata["freqs"]) < 1e-2
