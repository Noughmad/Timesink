VERSION = (0, 1, 1)

def get_version():
    version = "%s.%s" % (VERSION[0], VERSION[1])
    if VERSION[2] != 0:
        version = "%s.%s" % (version, VERSION[2])
    return version

__version__ = get_version()