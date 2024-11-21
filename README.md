# dEX: Data Extraction via DNS Tool
dEX is a powerful tool for transmitting OS command output over DNS. It is equipped with robust mechanisms for handling missing chunks, ensuring efficient data recovery.

## How It Works
dEX leverages interactsh-client to launch an Out-of-Band (OOB) server. This server is used to generate payloads and listen for DNS queries. Before using dEX, ensure that the interactsh tool is installed and properly configured.

## Installation
1. Install [interactsh](https://github.com/projectdiscovery/interactsh)
2. Clone the dEX repository:
```bash
git clone https://github.com/your-repo/dEX.git
cd dEX
```
3. Run main.py
```
python3 main.py -h
```

## Usage
Run the tool with the following options. Use `-h` for help:
```
usage: main.py [-h] [-s SERVER] [-c CHUNK] [-pi POLL_INTERVAL] -m {nodejs} -cmd COMMAND -o OUTPUT

dEX: A tool to send OS command output over DNS, with support for handling missing chunks.

options:
  -h, --help            show this help message and exit
  -s, --server SERVER   interactsh server(s) to use (default: 'oast.pro')
  -c, --chunk CHUNK     chunk size for splitting data (default: 10)
  -pi, --poll-interval POLL_INTERVAL
                        poll interval in seconds to pull interaction data (default: 30)
  -m, --module {nodejs}
                        module to generate payloads
  -cmd, --command COMMAND
                        command to execute with the modules
  -o, --output OUTPUT   output file where results will be written
```

## Example: Exfiltrating /etc/passwd
Below is a demonstration of how to exfiltrate the /etc/passwd file using dEX:

[![asciicast](https://asciinema.org/a/sG4NmLBCEVPOtrH02i5goTfGC.svg)](https://asciinema.org/a/sG4NmLBCEVPOtrH02i5goTfGC)