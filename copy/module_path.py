import sys, os
__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.append(os.path.abspath(os.path.join(__dir__, '../')))

from common import util, logging

# if __name__ == '__main__':
#     header = util.get_headers()
#     print(header)
#    # logging.debug(header)