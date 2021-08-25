#ifndef LOGGER_H
#define LOGGER_H

#include <errlog.h> // EPICS logging facility

#define LOG_INFO(format, ...)  errlogSevPrintf(errlogInfo, format, ##__VA_ARGS__)
#define LOG_MINOR(format, ...) errlogSevPrintf(errlogMinor, format, ##__VA_ARGS__)
#define LOG_MAJOR(format, ...) errlogSevPrintf(errlogMajor, format, ##__VA_ARGS__)
#define LOG_FATAL(format, ...) errlogSevPrintf(errlogFatal, format, ##__VA_ARGS__)

#define LOG_INFO_DETAIL(format, ...)                                                   \
    errlogSevPrintf(                                                                   \
        errlogInfo, "%s(%s:%d): " format, __func__, __FILE__, __LINE__, ##__VA_ARGS__)
#define LOG_MINOR_DETAIL(format, ...)                                                  \
    errlogSevPrintf(errlogMinor,                                                       \
                    "%s(%s:%d): " format,                                              \
                    __func__,                                                          \
                    __FILE__,                                                          \
                    __LINE__,                                                          \
                    ##__VA_ARGS__)
#define LOG_MAJOR_DETAIL(format, ...)                                                  \
    errlogSevPrintf(errlogMajor,                                                       \
                    "%s(%s:%d): " format,                                              \
                    __func__,                                                          \
                    __FILE__,                                                          \
                    __LINE__,                                                          \
                    ##__VA_ARGS__)
#define LOG_FATAL_DETAIL(format, ...)                                                  \
    errlogSevPrintf(errlogFatal,                                                       \
                    "%s(%s:%d): " format,                                              \
                    __func__,                                                          \
                    __FILE__,                                                          \
                    __LINE__,                                                          \
                    ##__VA_ARGS__)

#endif