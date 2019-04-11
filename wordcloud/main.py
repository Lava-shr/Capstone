import pdftowordcloud
import os
import operator
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize
nltk.download('wordnet')
nltk.download('punkt')
def main():
    for file in os.listdir("./pdf"):
        if file.endswith(".pdf"):
            a = pdftowordcloud.towordcloud("./pdf/"+file)
            b={}
            lmtzr = WordNetLemmatizer()
            for key in a:
                keys = key.split(' ')
                for x in keys:
                    x=lmtzr.lemmatize(x.lower())
                    b[x] = b.get(x, 0) +a[key]
            txtpath= "./wordfrequency/"+ file.replace('.pdf','.txt')
            f= open(txtpath,"w+",encoding='utf-8')
            for key,value in sorted(b.items(), key=lambda x: (-x[1], x[0])):
            
                f.write('%s:%d\n' % (key, value))
if __name__ == '__main__':
    main()
