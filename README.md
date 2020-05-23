HTTPS Malleable C2 Config
=============
## Overview ##
This tool can be used to configure malleable C2 profiles with SSL certs for Cobalt Strike. LetsEncrypt certs can be automatically generated (or renewed) and added to a Java keystore. Other SSL certs can be added to a keystore by specifying their locations. 

## DISCLAIMER ##
I have not written any of the Malleable C2 profiles this project utilizes. All of the hard work was done by the contrbutors to this repository, which contains the C2 profiles this script uses: https://github.com/rsmudge/Malleable-C2-Profiles

This tool was inspired by this script: https://github.com/killswitch-GUI/CobaltStrike-ToolKit/blob/master/HTTPsC2DoneRight.sh

## Install ##
```bash
sudo apt-get install certbot
git clone https://github.com/Tw1sm/HTTPS-MalleableC2-Config.git
cd HTTPS-MalleableC2-Config
pip3 install -r requirements.txt
```
## Usage ##
usage: httpsprofile.py [-h] -domain DOMAIN -profile PROFILE -pass PASSWORD [-gen] [-keystore KEYSTORE] [-cacert CACERT] [-cert CERT]
```
Select a malleable C2 profile and add HTTPS on the fly

optional arguments:
  -h, --help          show this help message and exit
  -domain DOMAIN      Domain to use with HTTPS certs
  -profile PROFILE    The malleable C2 profile to use
  -pass PASSWORD      The Java keystore password to use
  -gen                Use LetsEncrypt to generate/renew certs for the domain
  -keystore KEYSTORE  Path to the pre-created Java Keystore for non-letsencrypt certs
  -cacert CACERT      Path to the CA cert for non-letsencrypt certs
  -cert CERT          Path to the domain cert for non-letsencrypt certs

To show all available profiles run: httpsprofile.py list
```

## Examples ##
List the available C2 profiles to choose from:
```sudo ./httpsprofile.py list```

Create a profile with pre-existing letsencrypt certs:
```sudo ./httpsprofile.py -domain seetwo.com -profile amazon -pass Password123```

Create a profile and generate/renew letsencrypt certs:
```sudo ./httpsprofile.py -domain seetwo.com -profile amazon -pass Password123 -gen```

Create a profile with non-letsencrypt certs: __*(Not fully tested)*__
```sudo ./httpsprofile.py -domain seetwo.com -profile amazon -pass ExistingPass123 -keystore existing.store -cacert gd_bundle-g2-g1 -cert 47ac05a411ccc8c9.crt```