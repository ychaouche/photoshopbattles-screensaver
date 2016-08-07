import setuptools
setuptools.setup(
    name             ="psb-downloader"            ,
    version          = "0.1"                      ,
    packages         = setuptools.find_packages() ,
    install_requires = ["praw","bs4"]             ,
)
