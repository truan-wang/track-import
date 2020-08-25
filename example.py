import os
import sys
from track_import import TimeImport


sys.meta_path.insert(0, TimeImport(
    os.path.abspath("."),
    sys.stdout
))

import test_package

