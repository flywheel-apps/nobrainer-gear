import os, os.path as op
from collections import OrderedDict
from .common import build_command_list, exec_command

def build(context):
    config = context.config
    inputs = context._invocation['inputs']

    params = OrderedDict()
    if 'model' in inputs.keys():
        params['model'] = context.get_input('model')
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

    if config['rotate-and-predict']:
        params['rotate-and-predict']=''
    
    context.gear_dict['params'] = params

def validate(context):
    params = context.gear_dict['params']
    # Ensure that the model exists
    if not op.exists(params['model']):
        raise FileNotFoundError('Model not found!!!')

def execute(context):
    inputs = context._invocation['inputs']
    command = ['nobrainer', 'predict']
    command = build_command_list(command, context.gear_dict['params'])
    command.extend([
        inputs['T1W']['location']['path'],
        op.join(context.output_dir,'brainmask.nii.gz')
    ])
    exec_command(context,command)
