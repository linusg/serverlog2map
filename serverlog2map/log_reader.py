import datetime
import gzip
import operator
import re
from typing import List, NamedTuple

Request = NamedTuple("Request", [("ip", str), ("timestamp", datetime.datetime)])


def _parse_log(
    path: str,
    regex_request: str,
    time_format: str,
    time_first: bool,
    ignore_local: bool,
    ignore_duplicates: bool,
) -> List[Request]:

    requests_ = []
    ip_addresses = set()

    if path.endswith(".gz"):
        with gzip.open(path, "rb") as f:
            lines = [line.decode() for line in f.readlines()]
    else:
        with open(path) as f:
            lines = f.readlines()

    for line_nr, line in enumerate(lines):
        line = line.strip()

        # Ignore empty lines
        if not line:
            continue

        try:
            if time_first:
                timestamp, ip = re.match(regex_request, line).groups()
            else:
                ip, timestamp = re.match(regex_request, line).groups()
        except AttributeError:
            # Invalid requests or other information included in the log will be ignored
            continue

        if (ip.startswith("127") or ip.startswith("192")) and ignore_local:
            continue

        if ip in ip_addresses and ignore_duplicates:
            continue

        print(
            "Parsed {path}, line {line_nr} - time: {timestamp}, IP address: {ip}".format(
                path=path, line_nr=line_nr, timestamp=timestamp, ip=ip
            )
        )

        request = Request(ip, datetime.datetime.strptime(timestamp, time_format))
        requests_.append(request)

        ip_addresses.add(ip)

    return requests_


def parse_log_files(
    files: List[str],
    regex_request: str,
    time_format: str,
    time_first: bool,
    ignore_local: bool,
    ignore_duplicates: bool,
) -> List[Request]:

    return sorted(
        [
            request
            for file in files
            for request in _parse_log(
                file,
                regex_request,
                time_format,
                time_first,
                ignore_local,
                ignore_duplicates,
            )
        ],
        key=operator.attrgetter("timestamp"),
    )
