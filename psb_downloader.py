import praw
import bs4
import urllib
import ssl
# do not enforce SSL validation
ssl._create_default_https_context = ssl._create_unverified_context

# do not use ~ in here
# use real, full path.
DESTINATION_FOLDER="/home/chaouche/IMAGES/REDDIT/PHOTOSHOPBATTLES/"

# let's create a reddit browser
reddit=praw.Reddit(user_agent="interactive test from ipython",
                   client_id="YCqZuFjwVY541akMwbrpIQ",
                   client_secret="aoZsWbzOF-EEG60IRTY0JwlCnxx-IA")

# browse to a subreddit
psbattles=reddit.subreddit("photoshopbattles")

# get top submissions
psbattles.topsubs=psbattles.top()

# loop through them
for sub in psbattles.topsubs:
    print("getting links from submission: %s" % sub.title)
    commentcount=0
    # loop through comments
    for comment in sub.comments:
        commentcount+=1

        # "MoreComments" is a special comment that doesn't have a body
        if hasattr(comment,"body") and "https://" in comment.body : 
            print("found link in comment #%d:%s"%(commentcount,comment.body))

            # Let's extract only the link from the comment,
            # as html this time,
            # bs4 will help us with this.
            comment.soup=bs4.BeautifulSoup(comment.body_html,features="html.parser")

            # oh,
            # btw,
            # a comment may have many links
            for link in comment.soup.find_all("a"):

                # get the href attribute of the a tag
                comment.soup.link=link.get("href")
                print("DIRECT LINK:",comment.soup.link)
                
                
                # if it's a media file
                if any([extension in comment.soup.link for extension in (".jpg",".jpeg",".png",".gif",".mp4",".webp",".webm")]):

                    # save this for later download
                    imglink = comment.soup.link
                    print("IMAGE LINK:",imglink)
                    # parse the url
                    # get the part after the last "/"
                    imgfile=urllib.parse.urlparse(comment.soup.link).path.split("/")[-1]

                    # download to DESTINATION_FOLDER/filename
                    # DESTINATION_FOLDER already has a trailing "/"
                    
                    try:
                        urllib.request.urlretrieve(imglink,DESTINATION_FOLDER+imgfile)
                        print("saved to :", DESTINATION_FOLDER+imgfile)
                    except urllib.error.HTTPError as e :
                        print("there was an error with this url")
                        print("skipping")

                # if it's an imgur album or gallery entry
                elif "imgur.com/" in comment.soup.link:

                    # then grab its HTML 
                    soup=bs4.BeautifulSoup(urllib.request.urlopen(comment.soup.link).read(),features="html.parser")
                    # and find the direct image links in there
                    images=soup.head("meta",attrs={"name":"twitter:image"})                    
                    for image in images:
                        imglink = image.get("content")
                        print("IMAGE LINK <from gallery or album>:",imglink)                        
                        imgfile = urllib.parse.urlparse(imglink).path.split("/")[-1]
                        # download to DESTINATION_FOLDER/filename
                        # DESTINATION_FOLDER already has a trailing "/"                        
                        try:
                            urllib.request.urlretrieve(imglink,DESTINATION_FOLDER+imgfile)
                            print("saved to :", DESTINATION_FOLDER+imgfile)
                        except urllib.error.HTTPError as e:
                            print("there was an error with this url")
                            print("skipping")
                            


                # if it's neither a direct image link
                # nor an imgur link
                # we simply ignore it
                else:
                    print("probably not an image link")
                    print("Ignoring")
                    
