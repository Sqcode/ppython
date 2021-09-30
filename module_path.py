import sys, os
__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.append(os.path.abspath(os.path.join(__dir__, './common')))

import util
import logging

logging.basicConfig(filename = "out.txt",level=logging.DEBUG,format= "%(asctime)s %(levelname)s -- %(message)s")
# logging.debug(111111111)

# , excel