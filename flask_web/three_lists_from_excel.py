'''
Usage of these following 3 functions:


1. evolutionList('Samsung Galaxy S III') will give the evolution list of the model Samsung Galaxy S III
in html format

2. revolutionG1('Samsung Galaxy S III') will give the revolution G1 list of the model Samsung Galaxy S III
in html format

3. revolutionG2('Samsung Galaxy S III') will give the revolution G2 list of the model Samsung Galaxy S III
in html format

Suppose you store the evolution list result in a variable in routes.py and pass it into the html template to display it
-----------example------------------------
#in routes.py file,
model_name = 'Samsung Galaxy S III'
evolution = evolutionList(model_name)

#then,
#in the html template file, you'd like to display the string stored in evolution

<p>{{ evolution|safe }}</p>  # |safe ensures the safe conversion from string of html text
-----------------------------------
'''
from io import open
import codecs




lookup = {'Samsung Galaxy S III': 'Mobile', 'Samsung NX3000': 'CAMERA', 'NEC MultiSync EX231W': 'Monitors',
          'Sony BRAVIA HX850': 'TV', 'Samsung Google Nexus 10': 'Tablet', 'iPod nano (7th Gen/2.5\" Multitouch)':'Mp3 Player',
          'Microsoft Xbox 360 Slim':'Video Game console', 'HP TouchSmart 610q': 'Desktop PC', 'HP Officejet Pro X576dw Multifunction': 'Printer',
          'Lenovo IdeaPad Yoga 11':'Laptop1', 'Nikon D800': 'CAMERA_nikon'}

def evolutionList(model_name):
    # print('model name is: {}'.format(model_name))
    model_name = model_name.replace(u'\xa0', u' ') # dirty-remove the strange keyError bug
    filename = lookup[model_name] #.encode(encoding='UTF-8')
    # print('filename is {}'.format(filename))
    content = ''
    with open('lists/' + filename +'.txt', encoding="utf-8") as f:
        lines = f.readlines()
        for item in lines:
            if item.split('\n')[0] == 'Revolution-G1' or item.split('\n')[0] == 'Revolution-G2':
                break
            if item.split('\n')[0] == 'Evolution':
                # print(item)
                continue

            item = "&nbsp;".join(item.split())
            if item[-2:] == '->':
                item = item[0:-2]
            item += '<br />'
            # print(item)
            content += item
    return content

def revolutionG1(model_name):
    model_name = model_name.replace(u'\xa0', u' ')
    filename = lookup[model_name]
    #print('filename is {}'.format(filename))
    content = ''
    flag = False
    with open('lists/' + filename +'.txt', encoding="utf-8") as f:
        lines = f.readlines()
        for item in lines:

            if item.split('\n')[0] == 'Evolution' or item.split('\n')[0] == 'Revolution-G2':
                flag = False
                continue
            if item.split('\n')[0] == 'Revolution-G1':
                # print(item)
                flag = True
                continue
            if not flag:
                continue
            item = "&nbsp;".join(item.split())
            if item[-2:] == '->':
                item = item[0:-2]
            item += '<br />'
            #print(item)
            content += item
    return content

def revolutionG2(model_name):
    model_name = model_name.replace(u'\xa0', u' ')
    filename = lookup[model_name]
    #print('filename is {}'.format(filename))
    content = ''
    flag = False
    with open('lists/' + filename +'.txt', encoding="utf-8") as f:
        lines = f.readlines()
        for item in lines:

            if item.split('\n')[0] == 'Evolution' or item.split('\n')[0] == 'Revolution-G1':
                flag = False
                continue
            if item.split('\n')[0] == 'Revolution-G2':
                # print(item)
                flag = True
                continue
            if not flag:
                continue
            item = "&nbsp;".join(item.split())
            if item[-2:] == '->':
                item = item[0:-2]
            item += '<br />'
            #print(item)
            content += item
    return content

# print(evolutionList('Lenovo IdeaPad Yoga 11'))
# print(revolutionG2('Lenovo IdeaPad Yoga 11'))