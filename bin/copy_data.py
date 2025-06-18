# !usr/bin/env python
# -*- coding: utf-8 -*-
#

import shutil

# Copy data files into the python/tree/data directory
tmp = shutil.copytree('data', 'python/tree/data', dirs_exist_ok=True)
