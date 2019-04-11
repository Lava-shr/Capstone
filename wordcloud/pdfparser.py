import PyPDF2
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize
nltk.download('wordnet')
nltk.download('punkt')
def get_string_from_pdf(pdf_path):
   # print("start pdf parse")
    content = ""
    p = open(pdf_path, 'rb')
    pdfReader = PyPDF2.PdfFileReader(p)
    if pdfReader.isEncrypted:
        pdfReader.decrypt('')
    for pageNum in range(pdfReader.numPages):
        page = pdfReader.getPage(pageNum)
        if page.extractText() is not None:
            pageContents = page.extractText()
            content += pageContents
    lmtzr = WordNetLemmatizer()
    lemmatized =""
  #  print("start lemmatize")
    onotology = []
    onotology.append(['image','photo','picture','photograph'])
    onotology.append(['video','movie','film'])
    onotology.append(['screen','LCD','monitor','display'])
    onotology.append(['application','app'])
    onotology.append(['key','button'])
    onotology.append(['Autofocus','AF','Auto focus','focus'])
    for word in word_tokenize(content):
        o=lmtzr.lemmatize(word)
        for x in onotology:
            for y in x:
                if o==y:
                    o=x[0]
                    
        lemmatized+=o+" "
 #   print("finished pdf parse")
 
 
 
 
 
    return lemmatized
