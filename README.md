# photoshopbattles-screensaver
Downloads funny images from /r/photoshopbattles. Next step is to configure your screensaver's slideshow to get images from the hardcoded folder path.

# Setup
`$ python setup.py install`

or

`$ python setup.py install --user`

Will install all the required packages (currently praw and beautifulsoup)

# Running the script

Just run 

`$ python psb_downloader.py`

It will download images in a hardcoded directory (you should change that in the script itself). Then configure your screensaver to fetch images from it.
