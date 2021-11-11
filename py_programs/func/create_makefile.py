import os
import jinja2

file_dir_path = os.path.dirname(os.path.realpath(__file__))

BANDS_ALL = ['NB422', 'g', 'r', 'u']
BANDS_BROAD = ['g', 'r', 'u']
BAND_NARROW = 'NB422'

def create_makefile():

    with open(os.path.join(file_dir_path, 'Makefile.template'), 'r') as f:
        t = f.read()

    tp = jinja2.Template(t)
    content = tp.render(bands_all=BANDS_ALL, bands_broad=BANDS_BROAD, band_narrow=BAND_NARROW, bands_all_comma_separated=','.join(BANDS_ALL))
        
    with open('/mnt/data/Makefile', 'w') as mf:
        mf.write(content)