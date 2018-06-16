# serverlog2map
> Visualize IP address locations from server logs on a map.

## Requirements

- Python 3.6+
- Flask, grequests and their dependencies

## Installing

Just clone this repo and install the requirements using `pip`:

```bash
git clone https://github.com/linusg/serverlog2map.git
cd serverlog2map
pip install -r requirements.txt
```

Consider using a virtual environment.

## Running

For development or quick testing you can use the `werkzeug` server which ships with Flask. Make sure you are in the
top-level directory of this repository and run:

```bash
export FLASK_APP=serverlog2map
flask run
```

## Configuration

You can create a file `config.json` in the top-level directory of this repository to overwrite some or even all default
values, which are shown below:

```json
{
    "log_dir": "/var/log/nginx",
    "file_pattern": "access.log*",
    "marker_color": "#00000055",
    "marker_size": 20,
    "regex_request": "([(\\d\\.)]+) .*? (.*?) \\[(.*?)\\] \"(.*?) (.*?) (.*?)\" (\\d+) (\\d+)(?: \"(.*?)\" \"(.*?)\")?",
    "regex_request_invalid": "([(\\d\\.)]+) .*? (.*?) \\[(.*?)\\] \".*?\" (\\d+) (\\d+)(?: \"(.*?)\" \"(.*?)\")?",
    "time_format": "%d/%b/%Y:%H:%M:%S %z",
    "ignore_local": true
}
```

## Contributing

Contributions and bug reports are always welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
