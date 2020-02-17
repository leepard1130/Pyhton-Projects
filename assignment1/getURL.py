import urllib.request
wordsURL = 'https://csse1001.uqcloud.net/assignments/assignment1/words.txt'

def getURL():
    stream = urllib.request.urlopen(wordsURL)
    text = stream.read().deode('utf-8')
    stream.close()
    return text

def getText():
    """Return the text in the file, 'wordstxt.html.'

    Parameters:
        No parameters

    Return:
        str: text in 'words.txt.html'
    
    """
    fd = open('words.txt','r')
    text = fd.read()
    fd.close()
    return text
