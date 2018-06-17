import datetime
import gzip
import operator
import re
from pathlib import Path
from typing import List, NamedTuple, Optional, Union
import sys

HTTPRequest = NamedTuple(
    "Request",
    [
        ("ip", str),
        ("time_received", datetime.datetime),
    ],
)


def _parse_log(
    path: Path,
    regex_request: str,
    time_format: str,
    ignore_local: bool,
) -> List[HTTPRequest]:
    http_requests = []

    if path.suffix == ".gz":
        with gzip.open(str(path), "rb") as f:
            lines = [line.decode() for line in f.readlines()]
    else:
        with open(str(path)) as f:
            lines = f.readlines()

    lines = [line.strip() for line in lines if line.strip()]

    for line in lines:
        try:
            time_received, ip = re.match(
                regex_request, line
            ).groups()
        except AttributeError:
            # Invalid HTTP requests suck, but they occur.
            continue

        if ( ip.startswith("127") or ip.startswith("192") ) and ignore_local:
            continue

        print('*** Parsed from line - timestamp: {0}, ip: {1}'.format(time_received,ip), file=sys.stderr)

        http_request = HTTPRequest(
            ip,
            datetime.datetime.strptime(time_received, time_format),
        )
        http_requests.append(http_request)

    return http_requests


def parse_log_files(
    files: List[Union[Path, str]],
    regex_request: str,
    time_format: str,
    ignore_local: bool = True,
) -> List[HTTPRequest]:
    return sorted(
        [
            request
            for file in files
            for request in _parse_log(
                Path(file),
                regex_request,
                time_format,
                ignore_local,
            )
        ],
        key=operator.attrgetter("time_received"),
    )
