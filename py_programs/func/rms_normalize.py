from astropy.io import fits
import numpy as np

def rms_normalize(rms_image, sci_rms, rms_mean, output_image):

    d = fits.open(rms_image)
    data = d[0].data
    h = d[0].header
    d.close()

    newdata = data * sci_rms / rms_mean

    hdu = fits.PrimaryHDU(newdata.astype('float'), header=h)
    hdu.writeto(output_image)
