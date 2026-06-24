# KPLC Outage Stream 20260624b

A lightweight Python data pipeline designed to ingest, parse, and structure Kenya Power (KPLC) outage notices. It converts unstructured text into validated Pydantic models for real-time status updates.

## Features
- Regex-based extraction of regions, counties, and areas.
- Data validation using Pydantic.
- Mock ingestion engine for demonstration.
- JSON export for downstream API consumption.

## Installation
1. Ensure Python 3.9+ is installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the pipeline directly:
```bash
python pipeline.py
```

The script will output real-time updates to the console and generate a `latest_outages.json` file.

## Project Structure
- `pipeline.py`: The main logic containing the ingestor, processor, and pipeline runner.
- `requirements.txt`: Project dependencies.
- `latest_outages.json`: Generated output (after first run).