def load_words(filename, length):
    import random
    text = open(filename, "r")
    wordlist = []
    for line in text:
        for word in line.split():
            if len(word) == length:
                wordlist.append(word)
    text.close()
    return random.choice(wordlist)


