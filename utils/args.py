import os, os.path as op
from collections import OrderedDict
from .common import build_command_list, exec_command

def build(context):
    config = context.config
    inputs = context._invocation['inputs']

    params = OrderedDict()
    if 'HDF5-Model' in inputs.keys():
        params['model'] = context.get_input('HDF5-Model')
    else:
        params['model'] = op.join(
            '/flywheel',
            'v0',
            'model',
            'brain-extraction-unet-128iso-model.h5'
        )
    
    if config['threshold'] != 0.3:
        params['threshold'] = config['threshold']
    
    if config['largest-label']:
        params['l'] = ''
    
    context.gear_dict['params'] = params

def validate(context):
    pass

def execute(context):
    inputs = context._invocation['inputs']
    command = ['nobrainer', 'predict']
    command = build_command_list(command, context.gear_dict['params'])
    command.extend([
        inputs['T1W']['location']['path'],
        op.join(context.work_dir,'brainmask.nii.gz')
    ])
    exec_command(context,command)
