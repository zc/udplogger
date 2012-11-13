udplogger
=========

Quick and dirty server to listen on a udp socket and log what it gets.

It logs to standard output.  Being quick and dirty, it relies on a
process manager, like zdaemon (http://pypi.python.org/pypi/zdaemon),
to take care of logging standard outout to a file.
