#!/usr/bin/env python3
import os, os.path as op
import json
import subprocess as sp
import copy
import shutil
import glob
import logging

import flywheel
from utils import args, gear_preliminaries


if __name__ == '__main__':
    # Get the Gear Context
    context = flywheel.GearContext()

    context.log_config()
    context.gear_dict = {}
    context.config['dry-run'] = False
    gear_preliminaries.initialize_gear(context)

    # Validate against configuration
    try:
        gear_preliminaries.validate_config_against_manifest(context)
    except Exception as e:
        context.log.exception(e)
        context.log.fatal(
            'Please make the prescribed corrections and try again.'
        )
        os.sys.exit(1)

    # Build, Validate, and execute Parameters
    try:
        args.build(context)
        args.validate(context)
        args.execute(context)

    except Exception as e:
        context.log.fatal(e,)
        context.log.fatal('Error executing nobrainer.')
        os.sys.exit(1)

    context.log.info("nobrainer completed Successfully!")
    os.sys.exit(0)