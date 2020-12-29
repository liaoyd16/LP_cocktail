import os
import sys
if os.path.isdir("../"):
    sys.path.append("../")
    sys.path.append("../model")
else:
    sys.path.append("..\\")
    sys.path.append("..\\model")
import Meta
import Meta_config
