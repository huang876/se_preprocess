import os, sys, subprocess, json

def prepare_sextractor_user_parameter_file(output_filename):
    param_names = [
        'zero_point',
        'configuration_file',
        'sextractor_parameters_name',
        'analysis_thresh',
        'detect_thresh',
        'pixel_scale',
        'minarea',
        'filter_name'
    ]

    params = {}
    for param_name in param_names:
        params[param_name] = input(f'{param_name}: ')

    with open(output_filename, 'w') as f:
        f.write(json.dumps(params))

def sextractor(ref_img,
               ref_rms,
               mes_img,
               mes_rms,
               flag_image_filename,
               output_catalog_filename,
               mes_band_seg_filename,
               mes_band_bg_filename,
               zero_point,
               configuration_file,
               sextractor_parameters_name,
               analysis_thresh,
               detect_thresh,
               pixel_scale,
               minarea,
               filter_name,
            ):
                  
    command = [
        'source-extractor',
        f'{ref_img},{mes_img}',
        '-c', configuration_file,
        '-CATALOG_NAME', output_catalog_filename,
        '-MAG_ZEROPOINT', str(zero_point),
        '-GAIN', 'GAIN',
        '-FLAG_IMAGE', flag_image_filename,
        '-WEIGHT_TYPE', 'MAP_RMS,MAP_RMS',
        '-WEIGHT_IMAGE', f'{ref_rms},{mes_rms}',
        '-ANALYSIS_THRESH', str(analysis_thresh),
        '-DETECT_THRESH', str(detect_thresh),
        '-PIXEL_SCALE', str(pixel_scale),
        '-DETECT_MINAREA', str(minarea),
        '-PARAMETERS_NAME', sextractor_parameters_name,
        '-FILTER_NAME', filter_name,
        '-CHECKIMAGE_TYPE', 'SEGMENTATION,BACKGROUND',
        '-CHECKIMAGE_NAME', f'{mes_band_seg_filename},{mes_band_bg_filename}'
        ]
    print('running source-extractor:')
    print(command)
    print('')

    subprocess.call(command)

def run_sextractor_with_parameter_file(
    user_parameter_filename,
    ref_img,
    ref_rms,
    mes_img,
    mes_rms,
    flag_image_filename,
    output_catalog_filename,
    mes_band_seg_filename,
    mes_band_bg_filename
):
    with open(user_parameter_filename, 'r') as f:
        content = f.read()
        
    parameter = json.loads(content)
    sextractor(
        ref_img,
        ref_rms,
        mes_img,
        mes_rms,
        flag_image_filename,
        output_catalog_filename,
        mes_band_seg_filename,
        mes_band_bg_filename,
        **parameter
    )
