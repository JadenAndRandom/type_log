
import sys, os, time, io

__author__ = "Jaden@github.com"
__status__ = "production"
__version__ = "1.0.0"
__date__ = "07 Spr 2023"


LOG_INFO = 10
LOG_NOTICE = 20
LOG_WARNING = 30
LOG_ERROR = 40
LOG_CRITICAL = 50

_log_level_list = [LOG_INFO, LOG_NOTICE, LOG_WARNING, LOG_WARNING, LOG_ERROR, LOG_WARNING]
_log_name_list = ['INFO', 'NOTICE', 'WARNING', 'ERROR', 'CRITICAL']
_log_level_to_name = {
    LOG_INFO: 'INFO',
    LOG_NOTICE: 'NOTICE',
    LOG_WARNING: 'WARNING',
    LOG_ERROR: 'ERROR',
    LOG_CRITICAL: 'CRITICAL'
}

LOG_TERMINAL = 10
LOG_FILE_APPEND = 20
LOG_FILE_COVER = 30

_log_type_list = [LOG_TERMINAL, LOG_FILE_APPEND, LOG_FILE_COVER]
DEFAULT_LEVEL = LOG_WARNING
DEFAULT_TYPE = LOG_FILE_APPEND

LOG_DEBUG_TERMINAL = 10
LOG_DEBUG_FILE = 20
_log_debug_type_list = [LOG_DEBUG_TERMINAL, LOG_DEBUG_FILE]

RET_SUCCESS = 'Success'
RET_ERROR = 'Error'


class TypeLog:
    def __init__(self, log_level=DEFAULT_LEVEL, log_type=DEFAULT_TYPE, log_file=None):
        if log_level not in _log_type_list:
            return

        if log_type not in _log_type_list:
            return

        self.level = log_level
        self.log_type = log_type
        self.log_file = log_file

        self.level_name = _log_level_to_name.get(log_level)
        self.log_level_list = _log_level_list
        self.log_name_list = _log_name_list

        self.debug_log_enable = False
        self.debug_module = []
        self.log_debug_type = LOG_DEBUG_TERMINAL
        self.debug_handle = sys.stdout
        self.log_debug_file = None

        if log_type == LOG_TERMINAL or log_file is None:
            self.handle = sys.stdout
            return

        if log_type is LOG_FILE_APPEND:
            self.handle = open(self.log_file, 'a+', errors='ignore')
        elif log_type is LOG_FILE_COVER:
            self.handle = open(self.log_file, 'w', errors='ignore')

        return

    def __del__(self):
        if self.log_debug_type == LOG_DEBUG_FILE:
            self.debug_handle.close()

        if self.log_type == LOG_FILE_APPEND or self.log_type == LOG_FILE_COVER:
            self.handle.close()

        return

    def set_log_level(self, log_level):
        if log_level in self.log_level_list:
            self.level = log_level
            self.level_name = _log_level_to_name.get(log_level)
            return RET_SUCCESS

        return 'Not find log level :%d. ' % log_level

    def add_log_level(self, log_level, log_level_name):
        if log_level is None or log_level_name is None:
            return RET_ERROR

        if log_level in self.log_level_list:
            return 'The log level is exist.'

        if log_level_name in self.log_name_list:
            return 'The log level name is exist.'

        # the level list is not in order
        self.log_level_list.append(log_level)
        self.log_name_list.append(log_level_name)

        level_to_name = {log_level: log_level_name}
        _log_level_to_name.append(level_to_name)
        return RET_SUCCESS

    def set_log_type(self, log_type, log_file):
        if log_type not in _log_type_list:
            return 'log level is not exist.'

        if self.log_type == LOG_FILE_APPEND or self.log_type == LOG_FILE_COVER:
            self.handle.close()

        self.log_type = log_type
        if log_type == LOG_TERMINAL:
            self.handle = sys.stdout
            return RET_SUCCESS

        if log_file is None:
            return 'log file is None.'
        self.log_file = log_file

        if log_type == LOG_FILE_COVER:
            try:
                self.handle = open(log_file, 'w', errors='ignore', encoding='utf-8')
            except Exception as errors:
                print(errors)
                self.handle.close()

        elif log_type == LOG_FILE_APPEND:
            try:
                self.handle = open(log_file, 'a+', encoding='utf-8')
            except Exception as errors:
                print(errors)
                self.handle.close()

        return RET_SUCCESS

    def set_debug_module(self, debug_module):
        if debug_module in self.debug_module:
            return RET_SUCCESS

        self.debug_module.append(debug_module)
        self.debug_log_enable = True

        return RET_SUCCESS

    def set_debug_type(self, log_debug_type, log_debug_file=None):
        if log_debug_type not in _log_debug_type_list:
            return
        # if the origin type is log file, should close the file handle before set new log type
        if self.log_debug_type == LOG_DEBUG_FILE:
            self.debug_handle.close()

        self.log_debug_type = log_debug_type
        if log_debug_type == LOG_DEBUG_TERMINAL:
            self.debug_handle = sys.stdout
            return

        if log_debug_file is None:
            return

        self.log_debug_type = LOG_DEBUG_FILE
        self.log_debug_file = log_debug_file
        try:
            self.debug_handle = open(log_debug_file, 'w', errors='ignore')
        except Exception as errors:
            print(errors)
            self.debug_handle.close()
        return

    # logging type: 1981-01-01 08:00:00 [level]:[module_name] - logging msg
    def logging(self, module_name, level, msg):
        if level < self.level:
            return

        time_fmt = time.strftime('%Y-%m-%d %H:%M:%S')

        level_name = _log_level_to_name.get(level)
        if level_name is None:
            level_name = str(level)

        log_str = "%s [%s]:[%s] - %s\n" % (time_fmt, level_name, module_name, msg)
        self.handle.write(log_str)
        return

    # logging type: 1981-01-01 08:00:00 : [module_name] - logging msg
    def debug_logging(self, module_name,  msg):
        if self.debug_log_enable is False:
            return

        if module_name not in self.debug_module:
            return

        time_fmt = time.strftime('%Y-%m-%d %H:%M:%S')
        log_str = '%s : [%s] - %s\n' % (time_fmt, module_name, msg)
        self.debug_handle.write(log_str)

        return


if __name__ == '__main__':
    logger = TypeLog()

    logging_str = "this a warning log, level %s." % (_log_level_to_name.get(LOG_WARNING))
    logger.logging("test", LOG_INFO, "this a warning log, level %s." % (_log_level_to_name.get(LOG_WARNING)))
    for id in range(10):
        logging_string = "%s - %d" % (logging_str, id)
        logger.logging('test', LOG_WARNING, logging_string)

    logger.logging("test-2", LOG_NOTICE, "this a critical log, level {0}.".format(_log_level_to_name.get(LOG_CRITICAL)))

    for id in range(10):
        logging_string = "%s - %d" % (logging_str, id)
        logger.logging('test', LOG_CRITICAL, logging_string)

    logger.logging("test-1", LOG_CRITICAL, "this a critical log, level {0}.".format(_log_level_to_name.get(LOG_CRITICAL)))

    logger.set_debug_module('test')
    logging_str = "this a debug log."
    logger.debug_logging("test", logging_str)
    logger.debug_logging("test-2", "this a critical log, level {0}.".format(_log_level_to_name.get(LOG_CRITICAL)))
    logger.debug_logging("test-1", "this a critical log, level {0}.".format(_log_level_to_name.get(LOG_CRITICAL)))




