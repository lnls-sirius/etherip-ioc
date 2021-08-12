import logging as _logging
import os as _os


def config_logger(logger):
    handler = _logging.StreamHandler()
    formatter = _logging.Formatter("%(asctime)s %(name)-6s %(levelname)-8s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(_logging.DEBUG)


class FileManager:
    def __init__(self, ioc_name: str) -> None:
        self._base_path = _os.path.dirname(_os.path.abspath(__file__))
        self._ioc_name = ioc_name

    def ioc_cmd_file_path(self, cmd_name: str = None):
        if not cmd_name:
            cmd_name = f"{self._ioc_name}.cmd"
        return _os.path.join(self.ioc_cmd_dir, cmd_name)

    @property
    def ioc_cmd_dir(self):
        return _os.path.join(self._base_path, "../../ioc/iocBoot/iocetheripIOC/")

    def ioc_db_file_path(self, db_name: str = None):
        if not db_name:
            cmd_name = f"{self._ioc_name}.db"
        return _os.path.join(self.ioc_db_dir, cmd_name)

    @property
    def ioc_db_dir(self):
        return _os.path.join(self._base_path, "../../ioc/database/")
