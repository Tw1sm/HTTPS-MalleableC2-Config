#!/usr/bin/env python3
import argparse
import subprocess
import requests
import sys
import os
import shlex
from src.c2profiles import profiles
from texttable import Texttable


def getargs():
    if len(sys.argv) == 2 and sys.argv[1].lower() == 'list':
        t = Texttable()
        t.add_row(['C2 Profile Name', 'Profile URL'])
        for profile in profiles:
            t.add_row([profile.name, profile.url])
        print(t.draw())
        exit()
    else:
        parser = argparse.ArgumentParser(description="Select a malleable C2 profile and add HTTPS on the fly", epilog="To show all available profiles run: httpsprofile.py list", formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument("-domain", type=str, dest="domain", help="Domain to use with HTTPS certs", required=True)
        parser.add_argument("-profile", type=str, dest="profile", help="The malleable C2 profile to use", required=True)
        parser.add_argument("-pass", type=str, dest="password", help="The Java keystore password to use", required=True)
        parser.add_argument("-gen", action="store_true", dest="generate", help="Use LetsEncrypt to generate/renew certs for the domain", required=False)
        parser.add_argument("-keystore", type=str, dest="keystore", help="Path to the pre-created Java Keystore for non-letsencrypt certs", required=False)
        parser.add_argument("-cacert", type=str, dest="cacert", help="Path to the CA cert for non-letsencrypt certs", required=False)
        parser.add_argument("-cert", type=str, dest="cert", help="Path to the domain cert for non-letsencrypt certs", required=False)
        args = parser.parse_args()
        return args


def gen_cert(domain):
    proc = subprocess.run(shlex.split(f'certbot certonly --standalone -d {domain} --non-interactive --register-unsafely-without-email --agree-tos'), capture_output=True)
    if b'not yet due for renewal' in proc.stdout:
        print(f'[*] Certs not yet due for renewal')
    elif b'Congratulations!' in proc.stdout:
        print(f'[*] Certs generated')
    else:
        print('[!] Error generating certs')
        print('[!] Potential firewall issue - this script does not adjust the firewall')
        exit()


def main():
    args = getargs()
    custom_certs = False

    if args.keystore and args.cacert and args.cert:
        custom_certs = True

    # verify args
    if (args.keystore or args.cacert or args.cert) and not custom_certs:
        print('[!] If using non-letsencrypt certs, -keystore -cacert and -cert are all required args')
        exit()

    # check root access
    if os.getuid() != 0:
        print('[!] Sudo access required - rerun with root privs')
        exit()

    cert_folder = '/etc/letsencrypt/live'

    # check if profile exists
    try:
        profile = next((profile for profile in profiles if profile.name == args.profile))
    except:
        print(f'[!] {args.profile} is not an existing profile')
        exit()

    # call certbot
    if args.generate:
        if custom_certs:
            print('[!] Skipping letscencrypt cert generation (-gen not compatible with custom certs)')
        else:
            gen_cert(args.domain)

    # add custom certs to keystore
    if custom_certs:
        store = args.keystore
        profile_file = os.path.join(os.path.dirname(store), f'{profile.name}.profile')

        # import the ca cert
        proc = subprocess.Popen(shlex.split(f'keytool -import -trustcacerts -alias cacert -file {args.cacert} -keystore {store} -storepass {args.password}'), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        proc.wait()

        if proc.returncode == 0:
            print('[*] Imported the CA cert into the keystore')
        else:
            print('[!] Error importing the CA cert into the keystore')
            exit()

        # import the domain cert cert
        proc = subprocess.Popen(shlex.split(f'keytool -import -trustcacerts -alias mykey -file {args.cert} -keystore {store} -storepass {args.password}'), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        proc.wait()

        if proc.returncode == 0:
            print('[*] Imported the domain cert into the keystore')
        else:
            print('[!] Error importing the domain cert into the keystore')
            exit()

    else:
    # make a new keystore with letsencrypt certs

        # add vars for file locations
        chain = os.path.join(cert_folder, args.domain, 'fullchain.pem')
        priv = os.path.join(cert_folder, args.domain, 'privkey.pem')
        p12 = os.path.join(cert_folder, args.domain, f'{args.domain}.p12')
        store = os.path.join(cert_folder, args.domain, f'{args.domain}.store')
        profile_file = os.path.join(cert_folder, args.domain, f'{profile.name}.profile')

        # delete old store
        if os.path.isfile(store):
            os.remove(store)
            print('[*] Deleted old Java keystore')

        # create the PKCS12 archive
        proc = subprocess.Popen(shlex.split(f'openssl pkcs12 -export -in {chain} -inkey {priv} -out {p12} -name {args.domain} -passout pass:{args.password}'), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        proc.wait()

        if proc.returncode == 0:
            print('[*] Created PKCS 12 cert')
        else:
            print('[!] Error creating PKCS 12 cert. Does the domain/cert folder exist?')
            exit()

        # create the Java keystore
        proc = subprocess.Popen(shlex.split(f'keytool -importkeystore -deststorepass {args.password} -destkeystore {store} -srckeystore {p12} -srcstoretype PKCS12 -srcstorepass {args.password} -alias {args.domain}'), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        proc.wait()

        if proc.returncode == 0:
            print('[*] Created Java keystore')
        else:
            print('[!] Error creating Java keystore')
            exit()

    # get raw profile from Github and add keystore configs
    profile_str = profile.get_profile()
    if profile_str is None:
        print(f'[!] Error retreiving profile from {profile.url}')
        exit()

    profile_str += '\nhttps-certificate {'
    profile_str += f'\n    set keystore "{store}";'
    profile_str += f'\n    set password "{args.password}";'
    profile_str += '\n}\n'

    # Write the C2 profile to disk
    with open(profile_file, 'w') as f:
        f.write(profile_str)

    print(f'[*] Created {profile.name} profile')
    print(f'[*] Profile located at: {profile_file}')


if __name__ == '__main__':
    main()
