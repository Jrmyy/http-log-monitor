This reader is a thread to enable to reading and the alerting on the same time. The reader goes through every lines
of the log file, starting when it lasts the previous time.

Attributes
==========

log_path : /path/to/http/log/file
interval: int representing the time between 2 readings
line_read: number of read lines (keep track of where we are in the file, prevent from reading all the file each time
name: the name of the reader