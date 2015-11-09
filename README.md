# Socrata Pusher
Push database tables to Socrata via DataSync

This utility loops through a list of tables and pushes their contents to their corresponding Socrata dataset IDs.

## Requirements
- Java Runtime JDK
- [DataSync](https://socrata.github.io/datasync/)
- Python

## Installation
1. Clone this repository
2. Install dependencies via `pip install -r requirements.txt`
3. Put the DataSync `.jar` file in the `/bin` directory

## Configuration
1. Copy `.env.sample` to `.env` and fill it in
2. Copy `config.sample.json` to `config.json` and fill it in
3. Fill in table and dataset ID information in `datasets.yaml`

## Usage
```bash
$ python main.py
```