import os
import sys
if os.path.isdir("../TIMIT_proc"):
    sys.path.append("../TIMIT_proc")
    sys.path.append("../")
else:
    sys.path.append("..\\TIMIT_proc")
    sys.path.append("..\\")
import Meta
import Meta_config
