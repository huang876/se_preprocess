import sys
from . import tasks

tasks_dict = {
    'create_makefile': tasks.CreateMakefileTask,
    'convolve': tasks.ConvolveTask,
    'imexam': tasks.ImexamineTask,
    'imexpr': tasks.ImexprTask,
    'iterstat_sci': tasks.IterstatSciTask,
    'iterstat_rms': tasks.IterstatRmsTask,
    'make_moffat': tasks.MakeMoffatTask,
    'msccmatch': tasks.MsccmatchTask,
    'wcscopy': tasks.WcscopyTask,
    'wregister_sci': tasks.WregisterSciTask,
    'wregister_rms': tasks.WregisterRmsTask,
    'make_flag': tasks.MakeFlagTask,
    'rms_normalize': tasks.RmsNormalizeTask,
    'generate_kernel': tasks.GenerateKernelTask,
    'sextractor': tasks.SextractorTask,
    'prepare_sextractor': tasks.PrepareSextractorTask,
    'create_master_catalog': tasks.CreateMasterCatalogTask
}

def main(args):

    if len(args) == 1:
        taskname = 'list'
    else:
        taskname = args[1]
        commandline_args = args[2:]

    if taskname == 'list':
        for key in tasks_dict.keys():
            print(key)
        return
    elif taskname == 'help':
        if len(args) == 3 and args[2] in tasks_dict:
            task = tasks_dict[args[2]]
            task_args = task.arg_names
            print(task_args)
            return
        else:
            raise ValueError('the second argument should be an existing task name')
    elif taskname in tasks_dict:
        task = tasks_dict[taskname]()
    else:
        raise ValueError('wrong task name')

    task.run(commandline_args)


if __name__ == '__main__':
    args = sys.argv
    main(args)
