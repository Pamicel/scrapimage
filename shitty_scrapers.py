import os, requests, shutil
from urllib.request import urlopen

ERASE = 1

class Platform(object):
    def __init__(self, name, pattern, pre_key, post_key = ""):
        self.name = name
        self.pre_key_url = pre_key
        self.post_key_url = post_key
        self.pattern = pattern
        self.all = []


# cible = portions de code type : "736x": {"url": "https://s-media-cache-ak0.pinimg.com/736x/fe/7d/0a/fe7d0a3c34173862f08a65de9ab80e34.jpg"...
pinterest = Platform("Pinterest", b'"736x": {"url": "', "https://fr.pinterest.com/search/pins/?q=")

# cible = portions de code type : "low_res":"https:\/\/68.media.tumblr.com\/cbe236eb78bb36766e0ab738fa5dd394\/tumblr_ol28em9CPk1w4iwblo1_500.jpg","high_re...
tumblr = Platform("Tumblr", b'"low_res":"', "https://www.tumblr.com/search/")

# cible = portions de code type : "display_src": "https://scontent-cdg2-1.cdninstagram.com/t51.2885-15/e35/16585640_1337149983032610_2818077778350440448_n.jpg?ig_cache_key=MTQ0NTczNzUwNTkxNTQ0NTc1Ng%3D%3p.2"...
instagram = Platform("Instagram", b'"display_src": "', "https://www.instagram.com/explore/tags/", "/?hl=en")

# platforms = {
#     "Pinterest" :
#         {
#             "name"            : "Pinterest",
#             "pre_key_url"     : "https://fr.pinterest.com/search/pins/?q=",
#             "post_key_url"    : "",
#             # cible = portions de code type : "736x": {"url": "https://s-media-cache-ak0.pinimg.com/736x/fe/7d/0a/fe7d0a3c34173862f08a65de9ab80e34.jpg"...
#             "pattern"         : b'"736x": {"url": "'
#         },
#
#     "Tumblr" :
#         {
#             "name"            : "Tumblr",
#             "pre_key_url"     : "https://www.tumblr.com/search/",
#             "post_key_url"    : "",
#             # cible = portions de code type : "low_res":"https:\/\/68.media.tumblr.com\/cbe236eb78bb36766e0ab738fa5dd394\/tumblr_ol28em9CPk1w4iwblo1_500.jpg","high_re...
#             "pattern"         : b'"low_res":"'
#         },
#
#     "Instagram" :
#         {
#             "name"            : "Instagram",
#             "pre_key_url"     : "https://www.instagram.com/explore/tags/",
#             "post_key_url"    : "/?hl=en",
#             # cible = portions de code type : "display_src": "https://scontent-cdg2-1.cdninstagram.com/t51.2885-15/e35/16585640_1337149983032610_2818077778350440448_n.jpg?ig_cache_key=MTQ0NTczNzUwNTkxNTQ0NTc1Ng%3D%3p.2"...
#             "pattern"         : b'"display_src": "'
#         }
#     }


# def remove_file(keyword, platform, )

def erase_dir(keyword, platform):
    folder = keyword + '/' + platform
    if os.path.isdir(folder):
        shutil.rmtree(folder)
        print("Recursively erased directory : " + folder)

def make_dir(keyword, platform, all):
    if not os.path.exists(keyword):
        print("Creating new directory : " + keyword)
        os.makedirs(keyword)
    if not os.path.exists(keyword + "/" + platform):
        print("Creating new directory : " + keyword + "/" + platform)
        os.makedirs(keyword + "/" + platform)
    for a in all:
        name = a.split(b'/')[-1]
        print("Downloading " + keyword + "/" + platform + "/" + str(name)[2 : -1])
        with open(bytes(keyword, 'utf-8') + b'/' + bytes(platform, 'utf-8')  + b'/' + name, 'wb') as handle:
            response = requests.get(a, stream=True)
            if not response.ok:
                print(response)
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)

def dirty_field_extractor(html, pattern):
    all = []
    n = html[1:].find(pattern)
    while n != -1:
        html = html[n + 1: ]
        tmp = html[len(pattern): ]
        n = tmp.find(b'"')
        if tmp[: n] not in all:
            # print(tmp[: n])
            all.append(tmp[: n])
        n = html[1:].find(pattern)
    return (all)

# def scraper(keyword, d):
#     response = urlopen(d["pre_key_url"] + keyword + d["post_key_url"])
#     html = response.read()
#     all = dirty_field_extractor(html, d["pattern"])
#     if d["name"] == "Instagram":
#         for i in range(len(all)):
#             all[i] = all[i].split(b'?')[0]
#     if d["name"] == "Tumblr":
#         for i in range(len(all)):
#             all[i] = all[i].replace(b'\\', b'')
#             # print(all[i])
#     if ERASE :
#         erase_dir(keyword, d["name"])
#     make_dir(keyword, d["name"], all)
#     print(d["name"] + " : %d images saved" %(len(all)))

def scraper(keyword, p):
    response = urlopen(p.pre_key_url + keyword + p.post_key_url)
    html = response.read()
    p.all = dirty_field_extractor(html, p.pattern)
    if p.name == "Instagram":
        for i in range(len(p.all)):
            p.all[i] = p.all[i].split(b'?')[0]
    if p.name == "Tumblr":
        for i in range(len(p.all)):
            p.all[i] = p.all[i].replace(b'\\', b'')
            # print(all[i])
    if ERASE :
        erase_dir(keyword, p.name)
    make_dir(keyword, p.name, p.all)
    print(p.name + " : %d images saved" %(len(p.all)))

def scrap_all(keyword):
    scraper(keyword, tumblr)
    scraper(keyword, pinterest)
    scraper(keyword, instagram)

scrap_all("Soulages")
# scrap_all("cat")
# scrap_all("cars")

# def pinterest_scraper(keyword):
#     platform = "pinterest"
#     response = urlopen("https://fr.pinterest.com/search/pins/?q=" + keyword)
#     html = response.read()
#     all = dirty_field_extractor(html, b'"736x": {"url": "')
#     if ERASE :
#         erase_dir(keyword, platform)
#     make_dir(keyword, platform, all)
#     print("Pinterest : %d images saved" %(len(all)))
#
# def instagram_scraper(keyword):
#     platform = "instagram"
#     response = urlopen("https://www.instagram.com/explore/tags/" + keyword + "/?hl=en")
#     html = response.read()
#     all = dirty_field_extractor(html, b'"display_src": "')
#     for i in range(len(all)):
#         all[i] = all[i].split(b'?')[0]
#     if ERASE :
#         erase_dir(keyword, platform)
#     make_dir(keyword, platform, all)
#     print("Instagram : %d images saved" %(len(all)))
#
# print('keyword = "cat"')
# pinterest_scraper("cat")
# instagram_scraper("cat")
# tumblr_scraper("cat")
#
# print
# print('keyword = "cars"')
# pinterest_scraper("cars")
# instagram_scraper("cars")
# tumblr_scraper("cars")

