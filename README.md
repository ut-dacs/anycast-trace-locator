# Anycast Trace Locator

This project started as an AIMS workshop project, and turned into an ANRW 2025 paper.
We include both the measurement scamper code and the analysis code in this repository.

## Measurement

The measurement code is written in Python and uses the `scamper` tool to perform traceroute measurements.
The code is located in bulktracer.py

## Analysis

Before running the analysis script, you need to ensure the following dependencies are installed on your system.

### Python Dependencies

The necessary Python packages are listed in `requirements.txt`. Install them using pip:

```bash
pip install -r requirements.txt
```

### Data Files

This project requires city-level geolocation data.
We use IPInfo's city-level geolocation data, which can be downloaded from their website.
They provide free access for academic, education, and non-commercial projects (https://ipinfo.io/use-cases/ip-data-for-academic-research)