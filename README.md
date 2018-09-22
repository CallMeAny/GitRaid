GitRaid is an attempt to categorize the long list of github repos that I had bookmarked in my browser.

## What is this?

The internet is full of amazing projects, and github collects a big part of them.
It is a pity that all the great software you could stumble upon is just laying bookmarked in the broswer, with no idea what the content is and how it looks like.
Therefore GitRaid takes a list of those links, and from each of the repos extracts the basic information: title, author, tags, description and, if available, the readme and an image. The result is an html page where each project has its own section summarizing the content.

## Requirements and relevant info

* The script works with python3, and only requires the BeautifulSoup module.<

* Only links to main pages of repositories will work properly: ```https://github.com/<username>/<projectname>``` is the right format. 
* The link can basically be copied from the URL of the project page.
* Links to other pages will either be ignored or not parsed correclty.
* To work properly, the css file (gitRaid.css) used to style the output file needs to be in the same folder as the output file.

## How to use it?

1. Install BeautifulSoup with ```pip3 install beautifulsoup4```
2. Download the repo with ```git clone https://github.com/CallMeAny/GitRaid.git```
3. Create a file with a list of all your links, one link per line
    * You can also use a single link, in which case you don't need a file
4. Run the script with ```python gitRaid.py -f <inputfile || link> -o <outputfile>``` (use your own paths)
5. Wait a bit, and when the script is done you have your summary of github repos ready

## ToDo

* It would be great to have the tags summarized, for example on the side of the page, and clickable to show all the related repos. Probably requires some JS magic.
* Image collection is not working properly because no specific html tag class is used. There should be a better and less broken way to grab them.
* A search field. Oh, that would be amazing. It would be a not-too-messy starting point for the tag summary thingy.