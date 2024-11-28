# Licensed under a 3-clause BSD style license - see LICENSE.md
"""Read and write methods for json genealogy files."""

import json
from pathlib import Path

from chronodata.constants import (
    Arg,
    Key,
    Value,
)


def read(filename: str) -> list:
    mode: str = Arg.READ
    chron: dict = {}
    with Path.open(Path(filename), mode) as file:
        chron = json.load(file)
        file.close()
    cal_name = chron[Key.CAL][Key.NAME]
    chron_name = chron[Key.NAME]
    post = chron[Key.CAL][Key.POST]
    postlen = len(post)
    pre = chron[Key.CAL][Key.PRE]
    prelen = len(pre)
    return (
        cal_name,
        chron_name,
        post,
        postlen,
        pre,
        prelen,
        chron
    )
    # if self.log:
    #     logging.info(Msg.LOADED.format(self.chron_name, self.filename))

def write(filename: str, chron: dict) -> None:
    mode: str = Arg.WRITE
    # if name == Value.EMPTY:
    #     if self.filename == Value.EMPTY:
    #         file = Value.EMPTY.join([self.chron_name, Arg.JSON])
    #     else:
    #         file = self.filename
    # else:
    #     file = name
    with Path.open(Path(filename), mode) as f:
        json.dump(chron, f)
        f.close()
    