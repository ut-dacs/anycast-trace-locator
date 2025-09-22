# Anycast Trace Locator

[![DOI](https://img.shields.io/badge/DOI-10.1145/3744200.3744783-blue.svg)](https://doi.org/10.1145/3744200.3744783)

This codebase provides our measurement and analysis code for performing anycast enumeration and geolocation using traceroute.
We initially developped this during an AIMS workshop, and continued working on it as a [paper for ANRW'25](https://dl.acm.org/doi/abs/10.1145/3744200.3744783).

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

## Citation

This work was a contribution of our ANRW'25 paper.
Please use the following .bibtex when using this code.
```
@inproceedings{10.1145/3744200.3744783,
author = {Hendriks, Remi and Betzer, Tim and Du, Ben and Sommese, Raffaele and Jonker, Mattijs and van Rijswijk-Deij, Roland},
title = {Locating and Enumerating Anycast: a Comparison of Two Approaches},
year = {2025},
isbn = {9798400720093},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3744200.3744783},
doi = {10.1145/3744200.3744783},
abstract = {Anycast allows for providing services from multiple, geographically distant Points of Presence (PoPs), using a single IP address, to, e.g., improve resilience. Due to its opaqueness, it is often unknown which addresses are provisioned using anycast and, if so, where the PoPs are located. As anycast is widely used for critical Internet infrastructures (e.g., the DNS) efforts have been made to map anycast deployments. The current state-of-the-art mapping technique, iGreedy, relies on latency-based measurements, and is adversely affected by noise caused by, e.g., network processing delays. Previous work has shown that traceroute can alternatively be used to detect anycast. As traceroute reveals the hops a packet traverses, it may also be used to locate sites using geolocation data for hops near the anycast PoPs.This paper is the first to assess the performance of the traceroute-based approach at scale, by targeting 14k prefixes from an anycast census. Using ground truth we show traceroute achieves a slight increase in enumeration and geolocation precision over iGreedy. However, it suffers from overestimating the number of PoPs and incurs a 4\texttimes{} increase in probing cost, making it unattractive for anycast censuses.},
booktitle = {Proceedings of the 2025 Applied Networking Research Workshop},
pages = {99–105},
numpages = {7},
keywords = {Anycast, Geolocation, Traceroute},
location = {Madrid, Spain},
series = {ANRW '25}
}
```
