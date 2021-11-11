def wcscopy(input_image, ref_image):
    from pyraf import iraf
    from pyraf.iraf import immatch
    immatch.wcscopy(input_image, ref_image)
