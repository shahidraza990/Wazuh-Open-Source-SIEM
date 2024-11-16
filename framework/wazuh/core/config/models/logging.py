import logging

from pydantic import Field
from typing import List
from enum import Enum

from wazuh.core.config.models.base import WazuhConfigBaseModel


class LoggingFormat(str, Enum):
    """Enum representing the available logging formats."""
    plain = "plain"
    json = "json"


class LoggingLevel(str, Enum):
    """Enum representing the different levels of logging verbosity."""
    info = "info"
    debug = "debug"
    debug2 = "debug2"


class APILoggingLevel(str, Enum):
    """Enum representing the different levels of logging verbosity for an API."""
    debug = "debug"
    info = "info"
    warning = "warning"
    error = "error"
    critical = "critical"


class LoggingConfig(WazuhConfigBaseModel):
    """Configuration for logging levels.

    Parameters
    ----------
    level : Literal["info", "debug", "debug2"]
        The logging level. Default is "info".
    """
    level: LoggingLevel = LoggingLevel.info

    def get_level_value(self) -> int:
        """Returns the integer value associated with the logging level.

        Returns
        -------
        int
            The integer value corresponding to the logging level:
            - 0 for "info"
            - 1 for "debug"
            - 2 for "debug2"
        """
        if self.level == LoggingLevel.info:
            return 0
        if self.level == LoggingLevel.debug:
            return 1

        return 2


class LogFileMaxSizeConfig(WazuhConfigBaseModel):
    """Configuration for maximum log file size.

    Parameters
    ----------
    enabled : bool
        Whether the maximum file size feature is enabled. Default is False.
    size : str
        The maximum size of the log file. Supports 'M' for megabytes and 'K' for kilobytes. Default is "1M".
    """
    enabled: bool = False
    size: str = Field(default="1M", pattern=r"^([1-9]\d*)([KM])$")


class RotatedLoggingConfig(WazuhConfigBaseModel):
    """Configuration for logging with rotation.

     Parameters
     ----------
     level : Literal["debug", "info", "warning", "error", "critical"]
         The logging level. Default is "debug".
     format : List[Literal["plain", "json"]]
         The format for logging output. Default is ["plain"].
     max_size : LogFileMaxSizeConfig
         Configuration for the maximum log file size. Default is an instance of LogFileMaxSizeConfig.
    """
    level: APILoggingLevel = APILoggingLevel.debug
    format: List[LoggingFormat] = Field(default=[LoggingFormat.plain], min_length=1)
    max_size: LogFileMaxSizeConfig = LogFileMaxSizeConfig()

    def get_level(self) -> int:
        """Returns the integer value corresponding to the logging level.

        Returns
        -------
        int
            The integer value corresponding to the logging level:
            - logging.DEBUG for "debug"
            - logging.INFO for "info"
            - logging.WARNING for "warning"
            - logging.ERROR for "error"
            - logging.CRITICAL for "critical"
        """
        if self.level == APILoggingLevel.debug:
            return logging.DEBUG
        elif self.level == APILoggingLevel.info:
            return logging.INFO
        elif self.level == APILoggingLevel.warning:
            return logging.WARNING
        elif self.level == APILoggingLevel.error:
            return logging.ERROR
        elif self.level == APILoggingLevel.critical:
            return logging.CRITICAL
        else:
            return logging.ERROR
