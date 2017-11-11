from typing import Any, Iterable, Iterator, List, Tuple, Union
from lib.typing import Path

from itertools import accumulate, tee, takewhile
from os import mkdir
from os.path import splitext, isdir, join, basename, sep

import pandas as pd


def sensible_export_path(origin  : Path,
                         path    : Path = None,
                         new_ext : str  = None,
                         ) -> Path:
    if not path:
        path = '.'

    if isdir(path):
        final_path = join(path, basename(origin))

        if new_ext:
            final_path = change_ext(final_path, new_ext)
        return final_path

    return path


def change_ext(origin  : Path,
               new_ext : str,
               ) -> Path:
    path, ext = splitext(origin)

    return ''.join((path, new_ext))


def mkdirdeep(path: Path) -> None:
    sections = path.split(sep)  # type: ignore

    # If path is absolute, first section will be empty
    if sections[0] == '':
        sections[0] = sep

    partials = list(
        accumulate(sections,
                   lambda acc, n: acc + sep + n)
    )

    for partial_path in partials:
        try:
            mkdir(partial_path)
        except FileExistsError:
            pass


def to_excel(dfs      : Union[pd.DataFrame, Iterable[Tuple[str, pd.DataFrame]]],
             path     : Path,
             **kwargs : Any,
             ) -> None:
    if not isinstance(dfs, pd.DataFrame):
        writer = pd.ExcelWriter(path)

        for name, df in dfs:
            df.to_excel(writer, sheet_name=name, index=None, **kwargs)

        writer.save()
        return

    dfs.to_excel(path, index=None, **kwargs)  # type: ignore


def drop_repeated_headers(df          : pd.DataFrame,
                          ratio_equal : float = 0.5,
                          ) -> pd.DataFrame:
    # for tolerance reasons, you can set the ratio of
    # columns that need to be considered equal
    num_equal = round(len(df.columns) * ratio_equal)

    matches = sum([df[colname] == colname for colname in df.columns])

    return df[matches < num_equal].reset_index(drop=True)


def pairwise(it : Iterable[Any]) -> Iterator[Tuple[Any, Any]]:
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(it)
    next(b, None)
    return zip(a, b)


def take_consecutive(it : Iterable) -> List:
    it = iter(it)
    it = pairwise(it)
    it = takewhile(lambda t: t[0] + 1 == t[1], it)
    it = list(it)
    it = [a for a, b in it] + [it[-1][1]]
    return it
