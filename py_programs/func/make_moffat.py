from astropy.io import fits
import numpy as np

beta = 3.0

def create_matrix(xx, yy, beta, fwhm):
    alpha = fwhm / (2 * np.sqrt(2 ** (1 / beta) - 1))
    I0 = (beta - 1) / (np.pi * alpha ** 2)
    I = I0 * (1 + (np.sqrt(xx ** 2 + yy ** 2) / alpha) ** 2) ** (-beta)
    return I

def make_moffat(fwhm, output_file):

    x = np.linspace(-15,15,31)
    y = np.linspace(-15,15,31)
    xx, yy = np.meshgrid(x, y)

    data = create_matrix(xx, yy, beta, fwhm)

    hdu=fits.PrimaryHDU()
    hdu.data = data
    hdu.writeto(output_file)
