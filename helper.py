import logging
import os
def logger(logger_name:str,level,page_name):
    path=os.path.join('logging',page_name)
    os.makedirs(path,exist_ok=True)
    logging.getLogger(logger_name).handlers.clear()
    log=logging.getLogger(logger_name)
    log.setLevel(level)
    file=logging.FileHandler(os.path.join(path,logging.getLevelName(level)+'.log'))
    f=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file.setFormatter(f)
    log.addHandler(file)
    log.propagate=False
    return log