# Body Tracking CLI

A Python CLI tool that uses MediaPipe for body tracking and streams pose landmarks over OSC.

## Features:

- Tracks full-body pose using MediaPipe
- Sends real-time OSC messages to a specified host and port
- Supports debug mode (-D) to visualize landmarks

Installation

1. Install via GitHub

Make sure you have Python 3.8+ installed. Then run:

```bash
pip install git+https://github.com/Code-Interfaces/body-tracking
```

or, if you want to install from a specific version:

```bash
pip install git+https://github.com/Code-Interfaces/body-tracking@v0.1.0
```

Install from a Downloaded Repository

```bash
git clone https://github.com/Code-Interfaces/body-tracking.git
cd body-tracking
pip install .
```

## Usage

After installation, run:

```bash
body-tracking --host 127.0.0.1 --port 9000
```

Optional arguments:

- `--host` (default: 0.0.0.0)
- `--port` (default: 9000)
- `-D`,`--debug` (default: False)

## Example Commands

Run with default settings:

```bash
body-tracking
```

Run with custom host and port:

```bash
body-tracking --host 192.168.1.10 --port 9000
```

Enable debug mode:

```bash
body-tracking -D
```