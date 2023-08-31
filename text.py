# from common import util
import os, time, sys, logging

logging.basicConfig(filename="log.txt",level=logging.DEBUG,format= "%(asctime)s %(levelname)s -- %(message)s")

if __name__ == '__main__':
    # print(1)
    # header = util.get_headers()
    # print(header)
    # logging.debug(header)

    # desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    # print(desktop_path)
    # util.mkdir(desktop_path + '/' + str(round(time.time() * 1000)))

    # print('{:^10d}'.format(3567))
    # print(f"{0:%>10}")

    logging.debug(f" Query: {1}, Param: {2}, Result: {3}")

