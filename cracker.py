# coding:utf-8
import codecs
import hashlib
import string
import sys
import zipfile
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from utils import *


class Cracker:
    @staticmethod
    def crack_zip(filezipe, length, file, currpass=None):
        """
        :param filezipe: File zip to hack
        :param length: Number of password character
        :param file: Dictionary file
        :param currpass:
        :return:
        """
        if currpass is None:
            currpass = []
        lettres = string.ascii_letters  # .printable
        z = zipfile.ZipFile(filezipe)
        tries = 0
        if file is None and length is not None:

            for current in range(length):
                a = [i for i in lettres]
                for x in range(current):
                    a = [y + i for i in lettres for y in a]
                currpass = currpass + a

            print("Scanning...")
            for password in currpass:
                try:
                    tries += 1
                    z.setpassword(password.encode('ascii'))
                    z.extract('secret.txt')
                    print(Color.VERT +
                          "[+] MOT DE PASSE TROUVÉ : " + password + Color.FIN)
                    break
                except Exception as err:
                    if "Bad" in str(err):
                        pass
                    elif "File <ZipInfo" in str(err):
                        pass
                    else:
                        print(str(err))
        else:
            try:
                print("Scanning...")
                trouve = False
                # zip_file = zipfile.ZipFile(filezipe, 'r')
                ofile = codecs.open(file, "r", encoding="latin-1")
                for password in ofile.readlines():
                    password = password.strip("\n")
                    try:
                        z.setpassword(password.encode("utf-8"))
                        z.extract('secret.txt')
                        print(
                            Color.VERT + "[+] MOT DE PASSE TROUVÉ : " + str(password) + Color.FIN)
                        trouve = True
                        break
                    except Exception as err:
                        if "Bad" in str(err):
                            # print(str(err))
                            pass
                        else:
                            print(str(err))
                if not trouve:
                    print(Color.ROUGE +
                          "[-] Mot de passe non trouvé :(" + Color.FIN)
                ofile.close()
            except FileNotFoundError:
                print(
                    Color.ROUGE + "[-] Erreur : nom de dossier ou fichier introuvable !" + Color.FIN)
                sys.exit(1)
            except Exception as err:
                print("Couleur.ROUGE + [-] Erreur : " + str(err) + Color.FIN)
                sys.exit(2)

    @staticmethod
    def crack_dict(md5, file):
        """
        :param md5: Hash MD5
        :param file: Dictionary file
        :return:
        """
        # Casse un HASH MD5 (md5) via une liste de mots-clés (file)
        try:
            trouve = False
            ofile = open(file, "r")
            for mot in ofile.readlines():
                mot = mot.strip("\n")
                hashmd5 = hashlib.md5(mot.encode("utf8")).hexdigest()
                if hashmd5 == md5:
                    print(Color.VERT + "[+] Mot de passe trouvé : " +
                          str(mot) + " (" + hashmd5 + ")" + Color.FIN)
                    trouve = True
            if not trouve:
                print(Color.ROUGE + "[-] Mot de passe non trouvé :(" + Color.FIN)
            ofile.close()
        except FileNotFoundError:
            print(Color.ROUGE +
                  "[-] Erreur : nom de dossier ou fichier introuvable !" + Color.FIN)
            sys.exit(1)
        except Exception as err:
            print("Couleur.ROUGE + [-] Erreur : " + str(err) + Color.FIN)
            sys.exit(2)

    @staticmethod
    def crack_incr(md5, length, currpass=None):
        """
        :param md5: Hash MD5
        :param length: Number of characters
        :param currpass:
        :return:
        """
        # casse un HASH MD5 via une méthode incrémentale pour un mdp de longueur length

        if currpass is None:
            currpass = []
        lettres = string.ascii_letters  # .printable
        if length >= 1:
            if len(currpass) == 0:
                currpass = ['a' for _ in range(length)]
                Cracker.crack_incr(md5, length, currpass)
            else:
                for c in lettres:
                    currpass[length - 1] = c
                    print("[*] TEST DE : " + "".join(currpass))
                    if hashlib.md5("".join(currpass).encode("utf8")).hexdigest() == md5:
                        print(
                            Color.VERT + "[+] MOT DE PASSE TROUVÉ : " + "".join(currpass) + Color.FIN)
                        sys.exit(0)
                    else:
                        Cracker.crack_incr(md5, length - 1, currpass)

    @staticmethod
    def crack_en_ligne(md5):
        """
        :param md5: Hash MD5
        :return:
        """

        try:
            agent_utilisateur = "Mozilla/5.0 (Windows; U; Windows NT 5.1; fr-FR; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7"
            headers = {'User-Agent': agent_utilisateur}
            url = "https://www.google.com/search?hl=fr&q=" + md5
            requete = Request(url, None, headers)
            response = urlopen(requete)
        except HTTPError as e:
            print(Color.ROUGE + "[-] Erreur HTTP : " + str(e.code) + Color.FIN)
        except URLError as e:
            print(Color.ROUGE + "[-] Erreur d'URL : " + e.reason + Color.FIN)

        if "Aucun document" in response.read().decode("utf8"):
            print(Color.ROUGE + "[-] HASH NON TROUVE VIA GOOGLE" + Color.FIN)
        else:
            print(Color.VERT +
                  "[+] MOT DE PASSE TROUVE VIA GOOGLE : " + url + Color.FIN)
            print("-" * 60)
