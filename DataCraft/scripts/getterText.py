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

    fileText = open("fileText.txt","w+")
    for url in listUrl:
        print("Running")
        r = requests.get("http://" + url)
        data = r.text
        soup = BeautifulSoup(data, "html5lib")
        l = soup.findAll("i")[:3]
        try :
            if "<i><span" in str(l[0]) :
                fileText.write(l[1]+"\n")
            else :
                fileText.write(l[0]+"\n")
        except:
            fileText.write("Erreur\n")
    fileText.close()
    print("Done")
    return None
    #    if "minecraft" in textes[1]:
    #        fileUrl.write(textes[1]+"\n")
    #    else :
    #        fileUrl.write("FAILED\n")
    #    print("Running")
    #print("Done !")
    #fileUrl.close()

screenGetter()
