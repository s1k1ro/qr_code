# QR Code Generator

A CLI tool for generating QR codes from text, URLs, wifi credentials, or contact cards (vCard), with support for batch generation with CSV

## Features
- Encode plain text, URLs, wifi network credentials, or vCard contact info
- Customise QR code appearance: size, border, fill/background colour, error correction level
- Batch mode: generate multiple QR codes from a CSV file in one run

## Requirements
- Python 3.x
- Dependencies listed in requirements.txt

## Installation

```bash
git clone https://github.com/s1k1ro/qr_code.git
cd qr_code
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Basic text/URL QR code

```
python qr.py "https://example.com" -o mycode.png
```

### Wifi QR code

```bash
python qr.py -t wifi --ssid "MyNetwork" --password "ThePassword" -o wifi.png
```

### vCard QR code

```bash
python qr.py -t vcard --first-name "Rick" --last-name "Owens" --phone "555-0100" -o contact.png
```

### Batch mode

```bash
python qr.py --batch jobs.csv
```

The CSV must include all of the following column headers:

`type, data, output, ssid, password, first_name, last_name, phone, email, size, border, fill_colour, back_colour, level, version`

Not every cell needs a value — leave a cell blank if it doesn't apply to that row's `type`. For example, a `text` row can leave `ssid`, `password`, `first_name`, etc. blank. Only the fields required for that row's specific `type` must be filled in (e.g. `wifi` rows require `ssid` and `password`; `vcard` rows require at least `first_name` or `last_name`).

Rows that fail validation are skipped and reported as failed; the run continues processing remaining rows and prints a final `X succeeded, Y failed` summary.

## Options

| Flag | Description | Default |
|---|---|---|
| `-o, --output` | Output file path | `qr.png` |
| `-v, --version` | QR version (1-40, controls size/capacity) | auto |
| `-s, --size` | Pixel size per box | `10` |
| `-b, --border` | Border thickness in boxes | `4` |
| `-fc, --fill-colour` | Fill colour | `black` |
| `-bc, --back-colour` | Background colour | `white` |
| `-l, --level` | Error correction (`L`/`M`/`Q`/`H`) | `L` |
| `-t, --type` | Data type (`text`/`url`/`wifi`/`vcard`) | `text` |
For the complete flag list run:
```bash
python qr.py --help
```

## Running Tests

```bash
pip install -r requirements-dev.txt
python -m pytest
```

## About This Project

This was built as a personal learning project to practice composing Python from scratch. It covers CLI argument parsing, input validation, string formatting/escaping to spec (ZXing wifi format, vCard 3.0), batch processing from CSV, and unit testing.