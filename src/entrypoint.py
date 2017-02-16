from skynet import Skynet
from kernet.logger import Logger

logger = Logger('entrypoint')

def main():
    skynet = Skynet.instance
    skynet.boot()
    if not skynet.hasBooted:
        logger.error("Program failed to boot")
    else:
        skynet.run()
    skynet.shutdown()

if __name__ == "__main__":
    main()
