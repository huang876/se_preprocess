import sys

from .. import func


class Task:
    arg_names = []

    def process(self, **args):
        return None

    def run(self, commandline_args):
        l = len(commandline_args)

        if len(self.arg_names) == l:
            output = {}
            for idx, arg_name in enumerate(self.arg_names):
                output[arg_name] = commandline_args[idx]
        else:
            raise ValueError('wrong number of inputs')

        self.process(**output)

class ConvolveTask(Task):
    arg_names = ['wreg_file', 'kernel_file', 'output_file']

    def process(self, **args):
        return func.convolve(**args)

class ImexamineTask(Task):
    arg_names = ['wreg_image', 'output_file']

    def process(self, **args):
        beta, moffat = func.imexamine(args['wreg_image'])
        with open(args['output_file'], 'w') as f:
            f.write(str(moffat))
            f.write('\n')

class ImexprTask(Task):
    arg_names = ['rms_image', 'sci_rms_file', 'rms_mean_file', 'output_image']

    def process(self, **args):
        with open(args['sci_rms_file'], 'r') as f:
            sci_rms = float(f.read().strip())
        with open(args['rms_mean_file'], 'r') as f:
            rms_mean = float(f.read().strip())

        return func.imexpr(args['rms_image'], sci_rms, rms_mean, args['output_image'])

class IterstatSciTask(Task):
    arg_names = ['wreg_image', 'output_file']

    def process(self, **args):
        mean, rms = func.iterstat(args['wreg_image'])
        with open(args['output_file'], 'w') as f:
            f.write(str(rms))
            f.write('\n')

class IterstatRmsTask(Task):
    arg_names = ['wreg_image', 'output_file']

    def process(self, **args):
        mean, rms = func.iterstat(args['wreg_image'])
        with open(args['output_file'], 'w') as f:
            f.write(str(mean))
            f.write('\n')

class MakeMoffatTask(Task):
    arg_names = ['fwhm_file', 'output_file']

    def process(self, **args):
        with open(args['fwhm_file'], 'r') as f:
            fwhm = float(f.read().strip())
        return func.make_moffat(fwhm, args['output_file'])

class MsccmatchTask(Task):
    arg_names = ['fits_filename', 'coo_filename']

    def process(self, **args):
        return func.msccmatch(**args)

class WcscopyTask(Task):
    arg_names = ['input_image', 'ref_image']

    def process(self, **args):
        return func.wcscopy(**args)

class WregisterSciTask(Task):
    arg_names = ['input_image', 'ref_image', 'output_image']

    def process(self, **args):
        args['fluxconserve'] = 'yes'
        args['boundary'] = 'constant'
        args['constant'] = -999
        return func.wregister(**args)

class WregisterRmsTask(Task):
    arg_names = ['input_image', 'ref_image', 'output_image']

    def process(self, **args):
        args['fluxconserve'] = 'no'
        args['boundary'] = 'constant'
        args['constant'] = 999
        return func.wregister(**args)

class MakeFlagTask(Task):
    arg_names = ['rms_image', 'output_image']

    def process(self, **args):
        return func.make_flag(**args)

class RmsNormalizeTask(Task):
    arg_names = ['rms_image', 'sci_rms_file', 'rms_mean_file', 'output_image']

    def process(self, **args):
        with open(args['sci_rms_file'], 'r') as f:
            sci_rms = float(f.read().strip())
        with open(args['rms_mean_file'], 'r') as f:
            rms_mean = float(f.read().strip())

        return func.rms_normalize(args['rms_image'], sci_rms, rms_mean, args['output_image'])

class GenerateKernelTask(Task):
    arg_names = ['psf_target', 'psf_origin', 'output']

    def process(self, **args):
        return func.generate_kernel(**args)

class SextractorTask(Task):
    arg_names = [
        'user_parameter_filename',
        'ref_img',
        'ref_rms',
        'mes_img',
        'mes_rms',
        'flag_image_filename',
        'output_catalog_filename',
        'mes_band_seg_filename',
        'mes_band_bg_filename'
    ]
    def process(self, **args):
        return func.run_sextractor_with_parameter_file(**args)

class PrepareSextractorTask(Task):
    arg_names = ['output_filename']
    def process(self, **args):
        return func.prepare_sextractor_user_parameter_file(**args)

class CreateMasterCatalogTask(Task):
    arg_names = ['bands_comma_separated', 'pattern', 'master_catalog_filename']
    def process(self, **args):
        return func.create_master_catalog(**args)

class CreateMakefileTask(Task):
    arg_names = []
    def process(self, **args):
        return func.create_makefile()
