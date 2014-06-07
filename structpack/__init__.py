from ._version import __version__
version = __version__

import sys
from . import structpack
sys.modules[__name__] = structpack.data
