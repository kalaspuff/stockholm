from typing import Tuple, Union

__version_info__: Tuple[Union[int, str], ...] = (0, 5, 7)
__version__: str = "".join(
    [
        f".{n}" if isinstance(n, int) or str(n).isdigit() or str(n)[0:4] == "post" or str(n)[0:3] == "dev" else f"{n}"
        for n in __version_info__
    ]
).strip(".")

if __name__ == "__main__":  # pragma: no cover
    print(__version__)  # noqa: T201
