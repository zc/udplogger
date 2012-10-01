"""usage: udplogger host:port
"""
import signal, sys, time, zc.ngi.async

def handle(addr, s):
    print s

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    [addr] = args
    addr = addr.split(':')

    listener = zc.ngi.async.udp_listener((addr[0], int(addr[1])), handle)

    def handle_signal(*args):
        listener.close()
        sys.exit(0)

    signal.signal(signal.SIGTERM, handle_signal)
    while 1:
        time.sleep(99999)
