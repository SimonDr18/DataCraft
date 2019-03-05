from bs4 import BeautifulSoup
import requests
import urllib.request

def screenGetter():
    """
    Commande utilisant BeautifulSoup, module de parsing, afin de récupérer les textes d'un site web automatiquement.
    """

    with open('name.txt', 'r') as f:
        # On récupère tous les noms qui étaient dans un fichier .txt
        list = [line.strip() for line in f]

    listUrl = []
    for i in list:
        # On fait une list d'url à chercher
        listUrl.append("minecraft.gamepedia.com/" + i)

    #fileUrl = open("fileText.txt","w+")

    for url in listUrl:
        r = requests.get("http://" + url)
        data = r.text
        soup = BeautifulSoup(data, "html5lib")
        l = soup.findAll("i")[:2]
        l.get_text()
        if "<i><span" in l[0] :
            print(l[1])
        else :
            print(l[0])
        print()
    return None
    #    if "minecraft" in textes[1]:
    #        fileUrl.write(textes[1]+"\n")
    #    else :
    #        fileUrl.write("FAILED\n")
    #    print("Running")
    #print("Done !")
    #fileUrl.close()

screenGetter()
