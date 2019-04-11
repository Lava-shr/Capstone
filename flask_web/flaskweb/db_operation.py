# -*- coding: utf-8 -*-

from .models import *


# return the category name
def find_category(target_name):
    target = Category.query.get(target_name)
    parent_name = target.parent_name
    while parent_name is not None:
        parent = Category.query.get(parent_name)
        parent_name = parent.parent_name
    return parent.name


# find_category('Mobile Phones')


# return the list of all categories name in the database created by taxonomy.txt
def getAllcategories():
    all_categories = Category.query.filter_by(parent_name=None).all()
    counter = 0
    list = []
    for c in all_categories:
        list.append(c.name)
        counter += 1
    return list


# print(getAllcategories())
# return the tree structure of a category
def tree_structure_display(root, space1, space2, content):
    for i in range(0, space1):
        content += '&nbsp;'
    content += '->'
    content += root + '<br />'
    root_category = Category.query.get(root)
    cur = root_category
    next_space1 = space1 + space2
    next_space2 = 0
    for c in cur.children_categories:
        if len(c.name) > next_space2:
            next_space2 = len(c.name)

    for c in cur.children_categories:
        content = tree_structure_display(c.name, next_space1, next_space2, content)
    return content


# return the one level below category of the product
def one_level_below_product(product):
    #print(product)
    root_category = Category.query.get(product)
    cur = root_category
    list = []
    for c in cur.children_categories:
        list.append(c.name)
    return list


# print(one_level_below_product('Electronics'))

# return the list of final product that we have in database
def final_product(category, our_reference_product='Samsung Galaxy S III'):
    #print('our_reference_product: ' + our_reference_product)
    product = Category.query.get(category)
    models = product.models
    list = []
    for m in models:
        if m.name == our_reference_product:
            continue
        list.append(m.name)
    # print(list)
    return list


# print(final_product('Electronics'))
# return the list of features belonging to the model with model_name specified
def features_display(model_name):
    model = Model.query.get(model_name)
    features = model.w_features
    list = []
    for f in features:
        list.append(f.name)
    return list

# print(features_display('iPod nano'))
# final_product('Mobile Phones')

# show the existence of a feature in the model (if yes return 1, otherwise 0)
# model_name - the name of the model
# feature_name - the name of the feature to check
def doesFeatureExit(model_name, feature_name):
    model = Model.query.get(model_name)
    features = model.w_features
    for f in features:
        if f.name == feature_name:
            return 1
    return 0


# compute the cosine similarity between two product
# reference_model_name: name of the reference model
# shortlisted_model_name: name of the model used to compare with the reference model
def computeCosineSimilarity(reference_model_name, shortlisted_model_name):
    reference_model = Model.query.get(reference_model_name)
    shortlisted_model = Model.query.get(shortlisted_model_name)
    reference_features = reference_model.w_features
    sum = 0
    count = 0
    for f in reference_features:
        sum += doesFeatureExit(shortlisted_model_name, f.name)
        count += 1
    cos = sum / ((count ** 0.5) * (sum ** 0.5))
    return cos


# print(computeCosineSimilarity('Samsung Galaxy S III', 'iPod nano'))


# return a list of similar model names within threshold
# reference_model_name: name of the reference model
# shortlisted_model_names: list contain name of the models used to find similarity to the reference product
# lower_threshold, upper_threshold: max and min similarity provided by user's input
def find_similar(lower_threshold, upper_threshold, shortlisted_model_names, reference_model_name):
    list = []
    for name in shortlisted_model_names:
        score = computeCosineSimilarity(reference_model_name, name)
        # print(name + ': '+str(score))
        if score < upper_threshold and score > lower_threshold:
            list.append(name)
    return list


# list = ['Lenovo IdeaPad Yoga 11', 'iPod nano']
# print(find_similar(0.1, 0.9, list, 'Samsung Galaxy S III'))


# return a list of feature names that exist in similar model but not the reference model
def list_new_feature(reference_model_name, similar_model_name):
    reference_model = Model.query.get(reference_model_name)
    similar_model = Model.query.get(similar_model_name)
    similar_features = similar_model.w_features
    list = []
    for f in similar_features:
        if not doesFeatureExit(reference_model_name, f.name):
            list.append(f.name)
    return list

# # return the list of final product that we have in excel file
# def final_product(category):
#     if(category == 'Mobile Phones'):
#         return ['iphone 5', 'Samsung Galaxy SIII', 'Nexus 4', 'Samsung Galaxy Note 2', 'HTC One X']
#     if(category == 'Camera' or category == 'Digital Cameras'):
#         return['Nikon D800', 'Samsung NX3000']
#     if(category == 'Monitors' or category == 'Computer Monitors'):
#         return ['Philips 273E3LHSB/00', 'ViewSonic VP2365-LED', 'NEC MultiSync EX231W', 'Iiyama XB2472HD']
#     if(category == 'TV' or category == 'Satellite & Cable TV' or category == 'Televisions'):
#         return ['Panasonic VIERA ST50A','Samsung Series 8','Sony BRAVIA HX850','Panasonic VIERA VT50A']
#     if(category == 'Tablet' or category == 'Tablet Computers'):
#         return ['ASUS Google Nexus 7', 'Samsung Google Nexus 10', 'Amazon Kindle Fire HD', 'Asus Transformer Pad Infinity 700 LTE', 'Samsung Galaxy Note 10.1', 'Microsoft Surface RT']
#     if(category == 'MP3 Players'):
#         return ['SanDisk Sansa Clip Zip', 'iPod nano (7th Gen/2.5" Multitouch)' , 'Samsung Galaxy Player 3.6']
#     if(category == 'Video Game Consoles'):
#         return ['Sony Playstation 3 Slim', 'Microsoft Xbox 360 Slim', 'Nintendo Wii Mario Kart Bundle', 'Nintendo 3DS']
#     if(category == 'Desktop Computers'):
#         return ['Gateway SX2850-33', 'Velocity Micro Edge Z40', 'Digital Storm ODE Level 3', 'HP TouchSmart 610q', 'Apple iMac "Core i7" 3.4 27-Inch']
#     if(category == 'Printers, Copiers & Fax Machines' or category == 'Printer'):
#         return ['HP Officejet Pro X576dw Multifunction' , 'Dell B1163w Mono Laser Multifunction']
#     if(category == 'Laptops'):
#         return ['Alienware M14x R2', 'Lenovo IdeaPad Yoga 11']
#     list =[]
#     return list
