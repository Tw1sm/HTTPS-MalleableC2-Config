#!/usr/bin/env python3
import argparse
import subprocess
import requests
import sys
import os
import shlex
from c2profiles import profiles


def getargs():
    if len(sys.argv) == 2 and sys.argv[1].lower() == 'list':
        print('Malleable C2 Profiles')
        for profile in profiles:
            print(profile.name)
        exit()
    else:
        parser = argparse.ArgumentParser(description="Select a malleable C2 profile and add HTTPS on the fly\nShow available profiles: httpsprofile.py list", formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument("-d", type=str, dest="domain", help="Domain to use with HTTPS certs", required=True)
        parser.add_argument("-p", type=str, dest="profile", help="The malleable C2 profile to use", required=True)
        parser.add_argument("--pass", type=str, dest="password", help="The Java keystore password to use", required=True)
        parser.add_argument("-g", action="store_true", dest="generate", help="Use LetsEncrypt to generate/renew certs for the domain", required=False)
        args = parser.parse_args()
        return args


def main():
    args = getargs()
    cert_folder = '/etc/letsencrypt/live'

    # check if profile exists
    try:
        profile = next((profile for profile in profiles if profile.name == args.profile))
    except:
        print(f'[!] {args.profile} is not an existing profile')
        exit()


    chain = os.path.join(cert_folder, args.domain, 'fullchain.pem')
    priv = os.path.join(cert_folder, args.domain, 'privkey.pem')
    p12 = os.path.join(cert_folder, args.domain, f'{args.domain}.p12')
    store = os.path.join(cert_folder, args.domain, f'{args.domain}.store')

    proc = subprocess.Popen(shlex.split(f'openssl pkcs12 -export -in {chain} -inkey {priv} -out {p12} -name {args.domain} -passout pass:{args.password}'))
    proc.wait()

    print(proc.returncode)
    if proc.returncode == 0:
        print('[*] Created PKCS 12 cert')

    proc = subprocess.Popen(shlex.split(f'keytool -importkeystore -deststorepass {args.password} -destkeystore {store} -srckeystore {p12} -srcstoretype PKCS12 -srcstorepass {args.password} -alias {args.domain}'))
    proc.wait()

    print(proc.returncode)
    if proc.returncode == 0:
        print('[*] Created Java keystore')


    # get raw profile from Github and add keystore configs
    profile_str = profile.get_profile()
    profile_str += '\nhttps-certificate {'
    profile_str += f'\n    set keystore "{store}";'
    profile_str += f'\n    set password "{args.password}";'
    profile_str += '\n}'


if __name__ == '__main__':
    main()
