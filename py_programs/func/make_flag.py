from astropy.io import fits
import numpy as np

def make_flag(rms_image, output_image):

    d = fits.open(rms_image)
    data = d[0].data
    h = d[0].header
    d.close()

    newdata1 = (data <= 0).astype('int32')

    hdu = fits.PrimaryHDU(newdata1, header=h)
    hdu.writeto(output_image)
