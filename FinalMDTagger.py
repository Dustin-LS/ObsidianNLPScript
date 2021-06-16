import os
import nltk
import gensim
from gensim import corpora
import random
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
import pickle
import spacy
from spacy.lang.en import English
import shutil

#~~~~~~ BEGINNING OF VARIABLES SECTION ~~~~~~~#
# Any file in this path (including subdirectories) will be analyzed.
path = "D:/Notes/AssocMemex/markdownNotes"

# The lower the number, the more data will be collected and analyzed.
# Recommended is around .2, but depends on how large of files you're analyzing.
# The longer the documents, the higher this number can be. (between zero and one)
PercentTrainingData = .2

# The higher the number, the more potential associations may be found.
# Recommended is ~5 topics, run script again to find more.
NUM_TOPICS = 5
#~~~~~~~~ END OF VARIABLES SECTION ~~~~~~~~~~~#

parser = English()


def tokenize(text):
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        elif token.like_url:
            lda_tokens.append('URL')
        elif token.orth_.startswith('@'):
            lda_tokens.append('SCREEN_NAME')
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens


nltk.download('wordnet')


def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma


def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)


"""Filter out stop words:"""

nltk.download('stopwords')
en_stop = set(nltk.corpus.stopwords.words('english'))

"""Now we can define a function to prepare the text for topic modelling:"""


def prepare_text_for_lda(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [get_lemma(token) for token in tokens]
    return tokens


# This deletes out any files that are empty
for root, dirs, files in os.walk(path):
    for file in files:
        size = os.stat(os.path.join(root, file)).st_size
        if size == 0:
            os.remove(os.path.join(root, file))

# This filters out anything that doesn't have the file extension '.md'
# If your files are all in .txt format, the following change can be made:
# and the code will look for associations in all .txt files rather than .md.
# if(file[-4:] == ".txt"):
filelist = []

for root, dirs, files in os.walk(path):
    for file in files:
        if(file[-3:] == ".md"):  # replaces this line here.
            filelist.append(os.path.join(root, file))

for filepath in filelist:
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()

        # This gets all of the old tags right off the bat.

        oldTags = []
        TagArea = False

        for line in lines:
            if line == 'End of Automatic Tag Area\n':
                break
            if TagArea is True and line not in oldTags:
                oldTags.append(line)
            if line == 'The following Tags have been added automatically\n':
                TagArea = True

        # Now, we'll re-write the entire file line by line, excluding the old tags.

        with open(filepath, 'r+') as f:
            with open("temp.txt", "w+") as o:
                lines = f.readlines()
                tagArea = False
                for line in lines:
                    if line == 'The following Tags have been added automatically\n':
                        tagArea = True
                    if tagArea == False:
                        o.write(line)
                    if line == 'End of Automatic Tag Area\n':
                        tagArea = False
        shutil.move("temp.txt", filepath)

        # This tokenizes the text for LDA to use, taking only some amount of all the possible tokens.
        text_data = []
        with open(filepath, 'r') as f:
            for line in f:
                tokens = prepare_text_for_lda(line)
                if random.random() > PercentTrainingData:
                    # print(tokens)
                    text_data.append(tokens)

        """LDA with Gensim
        First, we are creating a dictionary from the data, then convert to bag-of-words corpus and save the dictionary and corpus for future use.
        """

        dictionary = corpora.Dictionary(text_data)
        corpus = [dictionary.doc2bow(text) for text in text_data]
        pickle.dump(corpus, open('corpus.pkl', 'wb'))
        dictionary.save('dictionary.gensim')

        """We are asking LDA to find 10 topics in the data:"""
        # Num_Topics = the number of individual topics that are talked about in the paper
        # num_words = the number of MOST relevant words to each topic that has been determined.

        # currently as written, this looks for the X most relevant topics, and get's the 1 most relevant word per that topic.
        try:
            ldamodel = gensim.models.ldamodel.LdaModel(
                corpus, num_topics=NUM_TOPICS, id2word=dictionary, passes=15)
            ldamodel.save('model5.gensim')
            topics = ldamodel.print_topics(num_words=1)
            """Now we have the topics that are related to the data we entered.
            We just have to do something with them"""

            with open(filepath, 'r') as f:
                lines = f.readlines()

    # write new tags that are not already found
            newTags = []
            with open(filepath, 'a') as f:
                f.write("\n")
                f.write("The following Tags have been added automatically\n")
            for tag in topics:
                topicName = tag[1]
                topicName = topicName[7:-1]
                toWrite = "[[" + str(topicName) + "]]\n"
                if toWrite not in oldTags and toWrite not in newTags:
                    newTags.append(toWrite)
            for tag in newTags:
                with open(filepath, 'a') as f:
                    f.write(tag)
    # write old tags
            for tag in oldTags:
                with open(filepath, 'a') as f:
                    f.write(tag)

            with open(filepath, 'a') as f:
                f.write("End of Automatic Tag Area\n")

        except:
            print("\n")
            print(
                "Unable to gather enough training/execution data. Perhaps file too small.")
            print(filepath)

    except UnicodeDecodeError:
        print("\n")
        print("Warning: Malformed Markdown in file: ")
        print(filepath)
        print("Could not find tags!")
