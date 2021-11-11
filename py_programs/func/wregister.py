def wregister(input_image: str, ref_image: str, output_image: str, fluxconserve: str, boundary: str, constant: int):
    from pyraf import iraf
    from pyraf.iraf import immatch
    immatch.wregister(input_image, ref_image, output_image, wcs='world', fluxconserve=fluxconserve, boundary=boundary, constant=constant)
