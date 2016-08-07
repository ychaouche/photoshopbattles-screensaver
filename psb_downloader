import praw
import bs4
import commands 

def get_submissions(subreddit):
    """ returns a list of submissions from a subreddit  """
    app = praw.Reddit(user_agent="psbattle-screensaver")
    url = "http://www.reddit.com/r/"+subreddit
    return app.get_content(url)

def get_comments(submission):
    """ returns a list of comments from a thread """
    return submission.comments

def extract_image(comment):
    """ returns an img url from a comment """
    try:
        return bs4.BeautifulSoup(comment.body_html).findAll("a")[0].get("href")
    except:
        print "[DEBUG] no image found in this comment"
        pass

def save_image(image_url,destination):
    """ downloads the image into a destination folder """
    commands.getoutput('cd %s && wget -nc %s' % (destination,image_url))

def main():
    # FIXME
    destination = "/home/ychaouche/IMAGES/STOCK/PHOTOSHOPBATTLES/"
    for submission in get_submissions("photoshopbattles"):
        print "[DEBUG] looking at submission",submission
        for comment in get_comments(submission)[1:]:
            print "[DEBUG] getting images from",comment
            image_url = extract_image(comment)
            print "[DEBUG] got image_url",image_url
            if image_url:
                print "[DEBUG] saving to",destination
                save_image(image_url,destination)

if __name__ == "__main__":
    main()
