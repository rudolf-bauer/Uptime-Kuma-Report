# Uptime-Kuma-Report

## Install
Simply clone and install requirements:
```bash
git clone https://github.com/MrT3acher/Uptime-Kuma-Report/
pip install -r requirements.txt
```

## Use
Simply run this command: (report of 30 days)
```bash
python -m kumareport --db kuma.db -d 30
```
Wait until the report get generated and a browser window pops up.


This is the usage help:
```
Usage: python -m kumareport [OPTIONS]

Options:
  -t, --tag TEXT      Tagname of the monitors to include in the report
  --db FILENAME       Uptime Kuma database path.  [required]
  -d, --days INTEGER  Number of days to report.  [required]
  --help              Show this message and exit.
```