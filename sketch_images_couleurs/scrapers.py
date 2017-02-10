import os, requests
from urllib.request import urlopen

ERASE = 1

class Platform(object):
    def __init__(self, name, pattern, pre_key, post_key = ""):
        self.name = name
        self.pre_key_url = pre_key
        self.post_key_url = post_key
        self.pattern = pattern
        self.all = []
        self.files = []
        self.mem = []


# cible = portions de code type : "736x": {"url": "https://s-media-cache-ak0.pinimg.com/736x/fe/7d/0a/fe7d0a3c34173862f08a65de9ab80e34.jpg"...
pinterest = Platform("Pinterest", b'"736x": {"url": "', "https://fr.pinterest.com/search/pins/?q=")

# cible = portions de code type : "low_res":"https:\/\/68.media.tumblr.com\/cbe236eb78bb36766e0ab738fa5dd394\/tumblr_ol28em9CPk1w4iwblo1_500.jpg","high_re...
tumblr = Platform("Tumblr", b'"low_res":"', "https://www.tumblr.com/search/")

# cible = portions de code type : "display_src": "https://scontent-cdg2-1.cdninstagram.com/t51.2885-15/e35/16585640_1337149983032610_2818077778350440448_n.jpg?ig_cache_key=MTQ0NTczNzUwNTkxNTQ0NTc1Ng%3D%3p.2"...
instagram = Platform("Instagram", b'"display_src": "', "https://www.instagram.com/explore/tags/", "/?hl=en")

def remove_files(keyword, p):
    erased = 0
    print("Erasing deprecated files")
    #removes anything in keyword/platform that was not previously scraped (added to p.all)
    folder = 'data/' + p.name
    if os.path.isdir(folder):
        #check all files in keyword/platform, erases those that do not appear in p.all
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            if bytes(file, 'utf-8') not in p.files:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    erased += 1
    print("\tErased %d images" %(erased))

def download_files(keyword, p):
    down = 0
    print("Downloading new files")
    # Check existence of primary folder
    if not os.path.exists("data"):
        print("Creating new directory data" )
        os.makedirs("data")
    # Check existence of secondary folder
    if not os.path.exists("data/" + p.name):
        print("Creating new directory :\t" + "data/" + p.name)
        os.makedirs("data/" + p.name)
    folder_files = os.listdir("data/" + p.name)
    for i in range(len(folder_files)):
        folder_files[i] = bytes(folder_files[i], 'utf-8')
    for i in range(len(p.files)):
        if p.files[i] not in folder_files:
            # print("Downloading\t" + "data/" + p.name + "/" + str(p.files[i])[2 : -1])
            down += 1
            with open(bytes("data", 'utf-8') + b'/' + bytes(p.name, 'utf-8')  + b'/' + p.files[i], 'wb') as handle:
                response = requests.get(p.all[i], stream=True)
                if not response.ok:
                    print(response)
                for block in response.iter_content(1024):
                    if not block:
                        break
                    handle.write(block)
    print("\tDownloaded %d images" %(down))

def dirty_field_extractor(html, p):
    print("Extracting urls from html...")
    n = html[1:].find(p.pattern)
    while n != -1:
        html = html[n + 1: ]
        tmp = html[len(p.pattern): ]
        n = tmp.find(b'"')
        if tmp[: n] not in p.all:
            # print(tmp[: n])
            p.all.append(tmp[: n])
        n = html[1:].find(p.pattern)

def scraper(keyword, p):
    response = urlopen(p.pre_key_url + keyword + p.post_key_url)
    html = response.read()
    print(p.name)
    dirty_field_extractor(html, p)
    if p.name == "Instagram":
        for i in range(len(p.all)):
            p.all[i] = p.all[i].split(b'?')[0]
    if p.name == "Tumblr":
        for i in range(len(p.all)):
            p.all[i] = p.all[i].replace(b'\\', b'')
            # print(all[i])
    p.files = [a.split(b'/')[-1] for a in p.all]
    if ERASE :
        remove_files(keyword, p)
    download_files(keyword, p)

def scrap_all(keyword):
    scraper(keyword, tumblr)
    print("")
    scraper(keyword, pinterest)
    print("")
    scraper(keyword, instagram)

scrap_all("plant")
