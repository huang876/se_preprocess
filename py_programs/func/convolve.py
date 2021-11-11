from astropy.io import fits

def convolve(wreg_file: str, kernel_file: str, output_file: str):
    from astropy.convolution import convolve

    wreg = fits.open(wreg_file)
    wreg_data = wreg[0].data
    hd = wreg[0].header
    wreg.close()
    kernel = fits.open(kernel_file)[0].data

    wreg_data = convolve(wreg_data, kernel)

    hdu = fits.PrimaryHDU(header=hd)
    hdu.data = wreg_data
    hdu.writeto(output_file)
