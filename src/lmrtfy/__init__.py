# -*- coding: utf-8 -*-

import os
import pathlib

__version__ = "0.0.10"
# Don't import or use the underscored variables. These are subject to change.
_user_home = pathlib.Path.home()

# TODO: respect system standard directories, for linux this is:
#  https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
#  issue #2
_lmrtfy_dir = _user_home.joinpath('.lmrtfy')
_lmrtfy_profiles_dir = _lmrtfy_dir.joinpath('profiles')
_lmrtfy_config_dir = _lmrtfy_dir.joinpath('config')
_lmrtfy_auth_dir = _lmrtfy_dir.joinpath('auth')
_lmrtfy_template_dir = _lmrtfy_dir.joinpath('templates')
_lmrtfy_job_dir = _lmrtfy_dir.joinpath('jobs')

if not _lmrtfy_dir.is_dir():
    os.mkdir(_lmrtfy_dir)

if not _lmrtfy_profiles_dir.is_dir():
    os.mkdir(_lmrtfy_profiles_dir)

if not _lmrtfy_config_dir.is_dir():
    os.mkdir(_lmrtfy_config_dir)

if not _lmrtfy_auth_dir.is_dir():
    os.mkdir(_lmrtfy_auth_dir)

if not _lmrtfy_template_dir.is_dir():
    os.mkdir(_lmrtfy_template_dir)

if not _lmrtfy_job_dir.is_dir():
    os.mkdir(_lmrtfy_job_dir)
