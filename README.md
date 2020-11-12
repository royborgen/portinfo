# portinfo
A Python scrip that fetches network port information from SANS Internet Storm Center. 
The output includes a list of common services and malware. 

## Usage
```
Usage: portinfo [PORT_NUMBER]
A valid port number in the range of 1 and 65535 number must be provided as argument..
```

## Example
Running portinfo 22 provides following results: 
```
Protocol   Service              Name
tcp        ssh                  SSH Remote Login Protocol
udp        ssh                  SSH Remote Login Protocol
tcp        Adoresshd            [trojan] Adore sshd
tcp        Shaft                [trojan] Shaft
udp        pcanywhere           PCAnywhere (deprecated) 
```

## Requirements
- Python 3 
- requests library installed (standard with Python 3) 
- sys library installed (standard with Python 3) 
- random library installed (standard with Python 3) 
- BeautifulSoup library installed (pip3 install BeautifulSoup)
