from common import util, logging
import os, time, sys
if __name__ == '__main__':
    # print(1)
    header = util.get_headers()
    print(header)
    logging.debug(header)

    # desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    # print(desktop_path)
    # util.mkdir(desktop_path + '/' + str(round(time.time() * 1000)))
