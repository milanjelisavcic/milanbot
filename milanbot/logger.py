import logging


def terminal_logger(name="MilanBot", level=logging.INFO):
    """
    RetA wrapper for retrieving basic logging function
    :param name:
    :param level:
    :return:
    """
    logging.basicConfig(level=level)
    return logging.getLogger(name=name)


def file_logger(file, name="FileMilan", level=logging.INFO):
    logging.basicConfig(level=level)
    logger = logging.getLogger(name=name)
    formatter = logging.Formatter(fmt='%(asctime)s,%(message)s',
                                  datefmt="%Y%m%d%H%M%S")
    handler = logging.FileHandler(filename=file)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def summary():
    return """\
        <html>
          <head></head>
          <body>
            <p>Summary<br>
               How are you?<br>
               Here is the <a href="http://www.python.org">link</a> you wanted.
            </p>
          </body>
        </html>
        """
