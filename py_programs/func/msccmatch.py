import os

def msccmatch(fits_filename, coo_filename):
    from pyraf import iraf
    from pyraf import gwm
    from pyraf.iraf import mscred

    mtime = os.path.getmtime(fits_filename)

    mscred.msccmatch(fits_filename, coo_filename, nsearch=250, search30, rsearch=0.2, maxshift=5., cfrac=0.5)

    m = gwm.getGraphicsWindowManager()
    m.delete('graphics1')

    mtime2 = os.path.getmtime(fits_filename)

    if mtime == mtime2:
        raise ValueError('data not modified!')
