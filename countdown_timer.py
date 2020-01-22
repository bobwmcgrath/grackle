from segment_driver import SegmentDriver
import time


class CountdownTimer:

    def __init__(self, conf):
        self.seg_driver = SegmentDriver(conf['pins'])
        self.cd_time = conf['time']
    
    def update(self):
        print('time: '+ str(self.cd_time))
        self.seg_driver.showNum( self.cd_time )
        self.cd_time -= 1



