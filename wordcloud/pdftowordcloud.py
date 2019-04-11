import pdfparser
import cloud


def towordcloud(path):

#    print("start pdf to cloud")


    # width of the picture
    WIDTH = 1280

    # height of the picture
    HEIGHT = 720

    # Number of words in the cloud
    NUM_OF_WORDS = 70

    # Name of the image
    image_file_name = path.replace('.pdf','').replace('./pdf/','./wordcloudimage/')

    # If you want to exclude certain words from the cloud,
    # you can add them as a new line to the file stopwords.txt
    # Currently stopwords.txt only contain Stop Words

    pdf_to_word = pdfparser.get_string_from_pdf(path)
 #   print("finish pdf to cloud")
    return cloud.makecloud(pdf_to_word, WIDTH,HEIGHT, NUM_OF_WORDS, image_file_name)