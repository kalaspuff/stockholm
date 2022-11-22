__version_info__ = (0, 5, 4)
__version__ = "".join([".{}".format(str(n)) if type(n) is int else str(n) for n in __version_info__]).replace(
    ".", "", 1 if type(__version_info__[0]) is int else 0
)

if __name__ == "__main__":  # pragma: no cover
    print(__version__)
