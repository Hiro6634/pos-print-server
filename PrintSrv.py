import log4p

class PrintSrv:
    def __init__(self):
        self.loggerInit()
        logger = log4p.GetLogger(__name__,config='./log4p.json')
        self.log =logger.loggger


#def main():

#    pass

#if __name__ == '__main__':
#    main()
    