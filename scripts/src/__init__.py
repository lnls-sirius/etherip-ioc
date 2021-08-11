import logging as _logging


def config_logger(logger):
    handler = _logging.StreamHandler()
    formatter = _logging.Formatter("%(asctime)s %(name)-6s %(levelname)-8s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(_logging.DEBUG)
