#!/usr/bin/env python

import numpy as np
import copy
from obspy.signal.util import _npts2nfft
from obspy.signal.invsim import (cosine_taper, cosine_sac_taper,invert_spectrum)
from scipy import signal

"""
GNU LESSER GENERAL PUBLIC LICENSE

Version 3, 29 June 2007

Copyright © 2007 Free Software Foundation, Inc. <https://fsf.org/>

Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed.

This version of the GNU Lesser General Public License incorporates the terms and conditions of version 3 of the GNU General Public License, supplemented by the additional permissions listed below.

0. Additional Definitions.

As used herein, “this License” refers to version 3 of the GNU Lesser General Public License, and the “GNU GPL” refers to version 3 of the GNU General Public License.

“The Library” refers to a covered work governed by this License, other than an Application or a Combined Work as defined below.

An “Application” is any work that makes use of an interface provided by the Library, but which is not otherwise based on the Library. Defining a subclass of a class defined by the Library is deemed a mode of using an interface provided by the Library.

A “Combined Work” is a work produced by combining or linking an Application with the Library. The particular version of the Library with which the Combined Work was made is also called the “Linked Version”.

The “Minimal Corresponding Source” for a Combined Work means the Corresponding Source for the Combined Work, excluding any source code for portions of the Combined Work that, considered in isolation, are based on the Application, and not on the Linked Version.

The “Corresponding Application Code” for a Combined Work means the object code and/or source code for the Application, including any data and utility programs needed for reproducing the Combined Work from the Application, but excluding the System Libraries of the Combined Work.

1. Exception to Section 3 of the GNU GPL.

You may convey a covered work under sections 3 and 4 of this License without being bound by section 3 of the GNU GPL.

2. Conveying Modified Versions.

If you modify a copy of the Library, and, in your modifications, a facility refers to a function or data to be supplied by an Application that uses the facility (other than as an argument passed when the facility is invoked), then you may convey a copy of the modified version:

a) under this License, provided that you make a good faith effort to ensure that, in the event an Application does not supply the function or data, the facility still operates, and performs whatever part of its purpose remains meaningful, or
b) under the GNU GPL, with none of the additional permissions of this License applicable to that copy.
3. Object Code Incorporating Material from Library Header Files.

The object code form of an Application may incorporate material from a header file that is part of the Library. You may convey such object code under terms of your choice, provided that, if the incorporated material is not limited to numerical parameters, data structure layouts and accessors, or small macros, inline functions and templates (ten or fewer lines in length), you do both of the following:

a) Give prominent notice with each copy of the object code that the Library is used in it and that the Library and its use are covered by this License.
b) Accompany the object code with a copy of the GNU GPL and this license document.
4. Combined Works.

You may convey a Combined Work under terms of your choice that, taken together, effectively do not restrict modification of the portions of the Library contained in the Combined Work and reverse engineering for debugging such modifications, if you also do each of the following:

a) Give prominent notice with each copy of the Combined Work that the Library is used in it and that the Library and its use are covered by this License.
b) Accompany the Combined Work with a copy of the GNU GPL and this license document.
c) For a Combined Work that displays copyright notices during execution, include the copyright notice for the Library among these notices, as well as a reference directing the user to the copies of the GNU GPL and this license document.
d) Do one of the following:
0) Convey the Minimal Corresponding Source under the terms of this License, and the Corresponding Application Code in a form suitable for, and under terms that permit, the user to recombine or relink the Application with a modified version of the Linked Version to produce a modified Combined Work, in the manner specified by section 6 of the GNU GPL for conveying Corresponding Source.
1) Use a suitable shared library mechanism for linking with the Library. A suitable mechanism is one that (a) uses at run time a copy of the Library already present on the user's computer system, and (b) will operate properly with a modified version of the Library that is interface-compatible with the Linked Version.
e) Provide Installation Information, but only if you would otherwise be required to provide such information under section 6 of the GNU GPL, and only to the extent that such information is necessary to install and execute a modified version of the Combined Work produced by recombining or relinking the Application with a modified version of the Linked Version. (If you use option 4d0, the Installation Information must accompany the Minimal Corresponding Source and Corresponding Application Code. If you use option 4d1, you must provide the Installation Information in the manner specified by section 6 of the GNU GPL for conveying Corresponding Source.)
5. Combined Libraries.

You may place library facilities that are a work based on the Library side by side in a single library together with other library facilities that are not Applications and are not covered by this License, and convey such a combined library under terms of your choice, if you do both of the following:

a) Accompany the combined library with a copy of the same work based on the Library, uncombined with any other library facilities, conveyed under the terms of this License.
b) Give prominent notice with the combined library that part of it is a work based on the Library, and explaining where to find the accompanying uncombined form of the same work.
6. Revised Versions of the GNU Lesser General Public License.

The Free Software Foundation may publish revised and/or new versions of the GNU Lesser General Public License from time to time. Such new versions will be similar in spirit to the present version, but may differ in detail to address new problems or concerns.

Each version is given a distinguishing version number. If the Library as you received it specifies that a certain numbered version of the GNU Lesser General Public License “or any later version” applies to it, you have the option of following the terms and conditions either of that published version or of any later version published by the Free Software Foundation. If the Library as you received it does not specify a version number of the GNU Lesser General Public License, you may choose any version of the GNU Lesser General Public License ever published by the Free Software Foundation.

If the Library as you received it specifies that a proxy can decide whether future versions of the GNU Lesser General Public License shall apply, that proxy's public statement of acceptance of any version is permanent authorization for you to choose that version for the Library.
"""

def remove_resp_digitalfilt(tr, poles, zeros, scale_fac, pre_filt=False, water_level=False, zero_mean=True,
    taper=True, taper_fraction=0.05, detrend=True, debug=False):
    """
    Remove response using the sensor response estimated as digital filter
    y(z) = G(z)u(z)

    Original code is the module of remove_response in obspy.core.trace:
    
    Reference:
    https://docs.obspy.org/_modules/obspy/core/trace.html#Trace.remove_response

    Reference:
    [1] Krischer, L., Megies, T., Barsch, R., Beyreuther, M., Lecocq, T., Caudron, C., and Wassermann, J.
    Obspy: a bridge for seismology into the scientific python ecosystem.
    Computational Science & Discovery, 8(1):014003, 2015, doi:10.1088/1749-4699/8/1/014003.

    2022.07.29 Kurama Okubo: modify the original code to adapt the digital filter using signal.freqz
    """

    # store the data trace on which the instrumental response is removed
    data = tr.copy().data.astype(np.float64)
    npts = len(data)

    # time domain pre-processing
    if zero_mean:
        data -= data.mean()
    if taper:
        data *= cosine_taper(npts, taper_fraction, sactaper=True, halfcosine=False) 
        
    # smart calculation of nfft dodging large primes
    nfft = _npts2nfft(npts)
    # Transform data to Frequency domain
    data = np.fft.rfft(data, n=nfft)
    freq_rfft = np.fft.rfftfreq(nfft, d=1/tr.stats.sampling_rate)

    #--------------------------------------------------------------------------------------#        
    # calculate and apply frequency response
    # To obtain freq_response of digital filter, we modified obspy.signal.invsim.paz_to_freq_resp().
    # Ref: https://docs.obspy.org/master/packages/autogen/obspy.signal.invsim.paz_to_freq_resp.html
    #--------------------------------------------------------------------------------------#        

    b, a = signal.zpk2tf(zeros, poles, scale_fac)
    # a has to be a list for the scipy.signal.freqs() call later but zpk2tf()
    # strangely returns it as an integer.
    # update: this feature is fixed in the signal.zpk2tf.
    # if not isinstance(a, np.ndarray) and a == 1.0:
    #     a = [1.0]
    
    # compute the frequency response as digital filter at identical frequencies of rfft
    freqs, freq_response = signal.freqz(b, a, worN=freq_rfft, whole=False, plot=None, fs=tr.stats.sampling_rate, include_nyquist=False) 

    # # DEBUG using freqz_zpk
    # freqs, freq_response = signal.freqz_zpk(zeros, poles, scale_fac, worN=freq_rfft, whole=False, fs=tr.stats.sampling_rate)

    freq_response_forward = copy.deepcopy(freq_response)

    # frequency domain pre-filtering of data spectrum
    # (apply cosine taper in frequency domain)
    if pre_filt:
        freq_domain_taper = cosine_sac_taper(freqs, flimit=pre_filt)
        data *= freq_domain_taper
        data_after_freqtapered = copy.deepcopy(data)

    else:
        freq_domain_taper = np.ones_like(freqs)

    if water_level is None:
        # No water level used, so just directly invert the response.
        # First entry is at zero frequency and value is zero, too.
        # Just do not invert the first value (and set to 0 to make sure).
        freq_response[0] = 0.0
        freq_response[1:] = 1.0 / freq_response[1:]
    else:
        # Invert spectrum with specified water level.
        invert_spectrum(freq_response, water_level)

    data *= freq_response
    data[-1] = abs(data[-1]) + 0.0j

    # transform data back into the time domain
    data_removed_infreq = copy.deepcopy(data)
    data = np.fft.irfft(data)[0:npts]

    # detrend using least squares
    if detrend:
        data = signal.detrend(data, type="linear")

    # assign processed data and store processing information
    tr_removed = tr.copy()
    tr_removed.data = data

    if debug:
        return tr_removed, freqs, freq_domain_taper, data_after_freqtapered, freq_response_forward, freq_response
    else:
        return tr_removed
