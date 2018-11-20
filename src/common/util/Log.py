class Logger:
    def __init__(self,logPath,timeDate=True):
        self.logPath=logPath
        self.timeDate=timeDate
        import os
        if not os.path.exists(os.path.dirname(logPath)):
            os.makedirs(os.path.dirname(logPath))
    def writeLog(self,content):
        import common.util.FileFunction as FF
        import time
        wt=FF.getWriter(self.logPath,True)
        if self.timeDate:
            content=time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime(time.time()))+content
        wt.write("\n"+content)
        print(content)
        wt.close()
    def getTime(self):
        import time
        return time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime(time.time()))