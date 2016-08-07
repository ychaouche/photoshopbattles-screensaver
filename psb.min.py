import praw
import bs4
import commands 

destination = "/home/ychaouche/IMAGES/STOCK/PHOTOSHOPBATTLES/"
for submission in praw.Reddit(user_agent="interactive test from ipython").get_content("http://www.reddit.com/r/photoshopbattles") : 
    for comment in submission.comments[1:]:
        try:
            image_url = bs4.BeautifulSoup(comment.body_html).findAll("a")[0].get("href")
        except:
            pass
        if image_url:
            commands.getoutput('cd %s && wget -nc %s' % (destination,image_url))
