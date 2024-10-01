#!/usr/bin/python3
# SPDX-License-Identifier: GPL-2.0-only

import os
from os.path import isfile, relpath
import sysconfig
from setuptools import setup

if isfile("MANIFEST"):
    os.unlink("MANIFEST")

SCHEME = 'rpm_prefix'
if not SCHEME in sysconfig.get_scheme_names():
    SCHEME = 'posix_prefix'

# Get PYTHONLIB with no prefix so --prefix installs work.
PYTHONLIB = relpath(sysconfig.get_path('platlib', SCHEME), '/usr')

setup(name="python-linux-procfs",
    version = "0.7.3",
    description = "Linux /proc abstraction classes",
    author = "Arnaldo Carvalho de Melo",
    author_email = "acme@redhat.com",
    url = "http://userweb.kernel.org/python-linux-procfs",
    license = "GPLv2",
    long_description =
"""\
Abstractions to extract information from the Linux kernel /proc files.
""",
    packages = ["procfs"],
    scripts = ['pflags'],
    install_requires = ['six'],
)
