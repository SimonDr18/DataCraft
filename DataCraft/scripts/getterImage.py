from bs4 import BeautifulSoup
import requests
import urllib.request

def screenGetter():
    """
    Commande utilisant BeautifulSoup, module de parsing, afin de récupérer les images d'un site web automatiquement.
    """

    with open('name.txt', 'r') as f:
        # On récupère tous les noms qui étaient dans un fichier .txt
        list = [line.strip() for line in f]

    listUrl = []
    for i in list:
        # On fait une list d'url à chercher
        listUrl.append("minecraft.gamepedia.com/File:" + i + ".png")

    fileUrl = open("fileUrl","w+")

    for url in listUrl:
        r = requests.get("http://" + url)
        data = r.text
        soup = BeautifulSoup(data, "html5lib")
        images = []
        for img in soup.findAll('img'):
            images.append(img.get('src'))
        if "minecraft" in images[1]:
            fileUrl.write(images[1]+"\n")
        else :
            fileUrl.write("FAILED\n")
        print("Running")
    print("Done !")
    fileUrl.close()

def screenDownloader(file):
    with open(file, 'r') as f:
        # On récupère tous les noms qui étaient dans un fichier .txt
        list = [line.strip() for line in f]

    for element in list :
        try :
            urllib.request.urlretrieve(element, element.split('/')[-1].split('?')[0])
        except :
            print("FAILED")


screenDownloader("fileUrl")
