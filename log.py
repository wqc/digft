import os
import time

class Log():
    def __init__(self):
        self.profit_file = 'profit'
        if not os.path.isdir('.log/'):
            os.makedirs('.log/')

    def loss(self, lossNum):
        fw = open('.log/profit', 'a+')
        fw.write(time.asctime( time.localtime(time.time())) + '     ')
        fw.write('loss: '+ str(lossNum))
        fw.write('\n')
        fw.flush()
        fw.close()
