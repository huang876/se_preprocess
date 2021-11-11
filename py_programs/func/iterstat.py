import io, contextlib

def iterstat(wreg_image: str) -> tuple:
    from pyraf import iraf
    from pyraf.iraf import stsdas
    from pyraf.iraf import hst_calib

    try:
        from pyraf.iraf import nicmos
    except ModuleNotFoundError:
        pass

    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        hst_calib.iterstat(wreg_image)

    iterstat_output = f.getvalue()

    r = iterstat_output.strip().split('\n')
    # use the last result
    line = r[-1]

    indexOfMean = line.find('mean')
    numbers = line[indexOfMean:].strip().split()

    mean = numbers[0]
    mean = mean[mean.find('=')+1:]

    rms = numbers[1]
    rms = rms[rms.find('=')+1:]

    return mean, rms
