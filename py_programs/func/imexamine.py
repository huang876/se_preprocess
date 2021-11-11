import subprocess, threading, io
from contextlib import redirect_stdout


def launch_ds9(filename: str):
    print('ds9 starting')
    subprocess.call(['ds9', filename, '-scale', 'mode zscale'])
    print('ds9 done')

def do_imexamine() -> str:
    print('imexamine starting')
    from pyraf import iraf
    from pyraf.iraf import tv

    f = io.StringIO()
    with redirect_stdout(f):
        tv.imexamine()

    print('imexamine done')

    return f.getvalue()

def imexamine(wreg_image: str):
    ds9_thread = threading.Thread(target=launch_ds9, args=(wreg_image, ))
    ds9_thread.start()

    imexamine_output = do_imexamine()

    ds9_thread.join()

    output_data = imexamine_output.strip().split('\n')[2:]

    l = len(output_data)

    if l & 1:
        raise ValueError('odd number of lines')

    l = int(int(l) / 2)

    beta_arr = []
    moffat_arr = []

    for i in range(l):
        values = output_data[i * 2 + 1].strip().split()
        beta_arr.append(float(values[7]))
        moffat_arr.append(float(values[9]))

    beta = sum(beta_arr) / l
    moffat = sum(moffat_arr) / l

    return beta, moffat
