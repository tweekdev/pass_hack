#!/usr/bin/env python3
# coding:utf-8
import argparse
import atexit
import time

from pyfiglet import Figlet

from cracker import *


def affiche_duree():
    # affiche la durée écoulée à la fin du script
    print("Time : " + str(time.time() - debut) + " seconds")


if __name__ == '__main__':
    f = Figlet(font='chunky')
    print("-" * 60)
    print(Color.MAGENTA + f.renderText('Pass Hacker') + Color.FIN)
    print("-" * 60)

    parser = argparse.ArgumentParser(description="Password hacker Python")
    parser.add_argument("-f", "--file", dest="file",
                        help="Dictionary path", required=False)
    parser.add_argument("-g", "--gen", dest="gen",
                        help="Generate a md5 with a choose word", required=False)
    parser.add_argument("-md5", dest="md5",
                        help="Enter a Hashed md5", required=False)
    parser.add_argument("-l", dest="plength",
                        help="Password length", required=False, type=int)
    parser.add_argument("-z", dest="zipfile",
                        help="Choose a zip file", required=False)
    parser.add_argument("-o", dest="online", help="Find the hash online (google)",
                        required=False, action="store_true")

    args = parser.parse_args()

    debut = time.time()
    atexit.register(affiche_duree)

    if args.gen:
        print("-" * 60)
        print("[*] HASH MD5 DE " + args.gen + " : " +
              hashlib.md5(args.gen.encode("utf8")).hexdigest())
        print("-" * 60)
    elif args.zipfile and args.plength and not args.file:
        print("-" * 60)
        print("[*] UTILISANT LE FICHIER ZIP " + args.zipfile)
        print("-" * 60)
        Cracker.crack_zip(args.zipfile, args.plength, args.file)
    elif args.zipfile and not args.plength and args.file:
        print("-" * 60)
        print("[*] UTILISANT LE FICHIER ZIP " + args.zipfile)
        print("-" * 60)
        Cracker.crack_zip(args.zipfile, args.plength, args.file)
    elif args.md5:
        print("-" * 60)
        print("[*] CRACKING DU HASH " + args.md5)
        print("-" * 60)
        if args.file:
            print("[*] UTILISANT LE FICHIER DE MOTS-CLÉS " + args.file)
            print("-" * 60)
            Cracker.crack_dict(args.md5, args.file)
        elif args.plength:
            print("[*] UTILISANT LE MODE INCREMENTAL POUR " +
                  str(args.plength) + " LETTRE(S)")
            print("-" * 60)
            Cracker.crack_incr(args.md5, args.plength)
        elif args.online:
            print("[*] UTILISANT LE MODE EN LIGNE")
            print("-" * 60)
            Cracker.crack_en_ligne(args.md5)
        else:
            print(Color.ROUGE +
                  "[-] VEUILLEZ CHOISIR L'ARGUMENT -f ou -l avec -md5." + Color.FIN)
            print("-" * 60)

    else:
        print(Color.ROUGE + "[-] HASH MD5 NON FOURNI." + Color.FIN)
        print("-" * 60)
