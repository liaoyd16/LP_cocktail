
import numpy as np

def SNR(x, v):
    return 20 * np.log10( np.linalg.norm(x) / np.linalg.norm(v) )

def distortion(xnew, xtgt, xsrc):
    dx_tgt = xnew - xtgt
    dx_src = xnew - xsrc
    dx = xtgt - xsrc

    snr_tgt = SNR(dx, dx_tgt)
    snr_src = SNR(dx, dx_src)

    return (snr_tgt, snr_src) # dx___ -- -> snr ++

def mute(xnew, xsrc):
    return SNR(xnew, xsrc) # mute == SNR --