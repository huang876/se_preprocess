def create_master_catalog(bands_comma_separated, pattern, master_catalog_filename):
    from astropy.table import Table
    from astropy.io import ascii

    bands = bands_comma_separated.split(',')
    
    colname_mapping = {
        'NUMBER': 'id',
        'ALPHA_J2000': 'ra',
        'DELTA_J2000': 'dec',
        'FLAGS': 'flag',
        'IMAFLAGS_ISO': 'isoflag',
        'MAG_ISO': 'mag_iso',
        'MAGERR_ISO': 'mag_iso_err',
        'ISOAREAF_IMAGE': 'area',
        'MAG_AUTO': 'mag_auto',
        'MAGERR_AUTO': 'mag_auto_err',
        'MAG_APER_1': 'mag_2aper',
        'MAGERR_APER_1': 'mag_2aper_err',
        'MAG_APER_2': 'mag_3aper',
        'MAGERR_APER_2': 'mag_3aper_err',
    }
    
    data = []
    merged_colnames = []

    for band in bands:
        catalog = ascii.read(pattern % band)

        for original_colname, target_colname in colname_mapping.items():
            new_colname = f'{band}_{target_colname}'
            data.append(catalog[original_colname])
            merged_colnames.append(new_colname)
        
        sng_colname = f'{band}_snr'
        data.append(catalog['FLUX_ISO'] / catalog['FLUXERR_ISO'])
        merged_colnames.append(sng_colname)

    result = Table(data, names=tuple(merged_colnames))
    ascii.write(result, master_catalog_filename, format='csv', fast_writer=False)
