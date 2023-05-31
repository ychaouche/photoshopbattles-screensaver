import praw
import bs4
import urllib
import ssl
# do not enforce SSL validation
ssl._create_default_https_context = ssl._create_unverified_context


# do not use ~ in here
# use real, full path.
DESTINATION_FOLDER="/home/chaouche/IMAGES/REDDIT/PHOTOSHOPBATTLES/"

def main():
    # let's create a reddit browser
    reddit=praw.Reddit("psb")

    # browse to a subreddit
    psbattles=reddit.subreddit("photoshopbattles")

    # loop through the new submissions
    for sub in psbattles.new():
        print("getting links from submission: %s" % sub.title)
        commentcount=0
        # loop through comments
        for comment in sub.comments:
            commentcount+=1

            # "MoreComments" is a special comment that doesn't have a body
            if hasattr(comment,"body") and "https://" in comment.body : 
                print("found link in comment #%d:%s"%(commentcount,comment.body))
                comment.links = extract_links(comment.body_html)
                for link in comment.links:
                    download(link,DESTINATION_FOLDER)

            
def download(link,destination):
    print("downloading",link)
    # if it's a media file
    if any([extension in link for extension in (".jpg",".jpeg",".png",".gif",".mp4",".webp",".webm")]):
        direct_download(link,destination)
    elif "imgur.com/" in link:
        imgur_download(link,destination)
    else:
        print("probably not an image link")
        print("Ignoring")

def direct_download(link,destination):
    imgfile=urllib.parse.urlparse(link).path.split("/")[-1]
    try:
        urllib.request.urlretrieve(link,destination+imgfile)
        print("saved to: ", destination+imgfile)
    except urllib.error.HTTPError as e :
        print("there was an error with this url")
        print("skipping")
        
def imgur_download(link,destination):
    soup=bs4.BeautifulSoup(urllib.request.urlopen(link).read(),features="html.parser")
    images=soup.head("meta",attrs={"name":"twitter:image"})
    for image in images:
        imglink = image.get("content")
        direct_download(imglink,destination)

        
def extract_links(html):
    soup=bs4.BeautifulSoup(html,features="html.parser")
    return [a.get("href") for a in soup.find_all("a")]

    
main()
