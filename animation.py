# credit: https://stackoverflow.com/questions/22029562/python-how-to-make-simple-animated-loading-while-process-is-running

import itertools
import threading
import time
import sys

done = False
def __animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\r' + c*3 + ' loading ' + c*3)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone!     ')

def start():
    t = threading.Thread(target=__animate)
    t.start()

def end():
    global done
    done = True
    print()