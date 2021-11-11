"""
equivalent of IRAF imexpr task, but uses Python and is faster
"""

from astropy.io import fits

def imexpr(rms_image, sci_rms, rms_mean, output_image):

    d = fits.open(rms_image)
    data = d[0].data
    h = d[0].header
    d.close()

    newdata1 = data * sci_rms / rms_mean

    hdu = fits.PrimaryHDU(newdata1.astype('float'), header=h)
    hdu.writeto(output_image)
