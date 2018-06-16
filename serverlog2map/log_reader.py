import datetime
import gzip
import operator
import re
from pathlib import Path
from typing import List, NamedTuple, Optional, Union


class HTTPRequest(NamedTuple):
    ip: str
    time_received: datetime.datetime
    method: str
    uri: str
    http_version: str
    status_code: int
    response_size: int
    referrer: Optional[str]
    user_agent: Optional[str]
    user_id: Optional[str]


def _parse_log(
    path: Path,
    regex_request: str,
    regex_request_invalid: str,
    time_format: str,
    ignore_local: bool,
) -> List[HTTPRequest]:
    http_requests = []

    if path.suffix == ".gz":
        with gzip.open(path, "rb") as f:
            lines = [line.decode() for line in f.readlines()]
    else:
        with open(path) as f:
            lines = f.readlines()

    lines = [line.strip() for line in lines if line.strip()]

    for line in lines:
        try:
            ip, user_id, time_received, method, uri, http_version, status_code, response_size, referrer, user_agent = re.match(
                regex_request, line
            ).groups()
        except AttributeError:
            # Invalid HTTP requests suck, but they occur.
            ip, user_id, time_received, status_code, response_size, referrer, user_agent = re.match(
                regex_request_invalid, line
            ).groups()
            method, uri, http_version = None, None, None

        if ip.startswith("127") and ignore_local:
            continue

        http_request = HTTPRequest(
            ip,
            datetime.datetime.strptime(time_received, time_format),
            method,
            uri,
            http_version,
            int(status_code),
            int(response_size),
            referrer,
            user_agent,
            user_id if user_id != "-" else None,
        )
        http_requests.append(http_request)

    return http_requests


def parse_log_files(
    files: List[Union[Path, str]],
    regex_request: str,
    regex_request_invalid: str,
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
                regex_request_invalid,
                time_format,
                ignore_local,
            )
        ],
        key=operator.attrgetter("time_received"),
    )
