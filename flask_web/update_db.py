# This file includes all the operations which would change the content of the database.

from flaskweb.models import *
from flaskweb import db
from sqlalchemy import exists
import os
import fnmatch
# db.session.rollback()

# create database for all categories listed in google taxanomy.txt file
def categoryDB():
    db.drop_all()

    db.create_all()
    counter = 0
    counter_sub = 0
    with open('taxonomy.txt', encoding='utf-8') as f:
        lines = f.readlines()
        for item in lines:
            if not item.__contains__('#'):
                if not item.__contains__('>'):
                    outest = item.split('\n')[0]
                    print(str(counter) + ': ' + outest)
                    counter += 1
                    outest_category = Category(name=outest)
                    db.session.add(outest_category)
                    db.session.commit()

                else:
                    # print('processing')
                    item = item.split('\n')[0]
                    item = item.split(' > ')

                    for i in range(1, len(item)):
                        if Category.query.get(item[i]) is None:
                            sub_category = Category(name=item[i], parent_name=item[i-1])
                            db.session.add(sub_category)
                            db.session.commit()

    print('category database created')


# create database for all models listed in products execl file
def productModelsDB():
    directory = 'wordfrequency/'
    count = 0
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            if fnmatch.fnmatch(filename, '*_new.txt'):
                continue
            print(os.path.join(directory, filename))
            model_name = filename.split('.txt')[0]
            if model_name == 'iPod nano':
                model_name = 'iPod nano (7th Gen/2.5\" Multitouch)'
            print(str(count) + ': model >> ' + model_name)
            count += 1
            file_path = directory + filename
            new_feature_list = directory + filename.split('.')[0] + '_new.txt'
            with open(file_path,  encoding='utf-8') as f:
                lines = f.readlines()
                flag = 0
                feature_count = 0
                new_feature = None
                new_model = None
                for item in lines:
                    if item.__contains__('product*'):
                        product_name = item.split('product*')[1].split('\n')[0]
                        print('product name is: ' + product_name)
                        ret = db.session.query(exists().where(Model.name == model_name)).scalar()
                        if ret:
                            print('model: {} already exists'.format(model_name))
                            break
                        new_model = Model(name=model_name, product_name=product_name)

                    elif item.__contains__(':'):
                        if feature_count == 70:
                            break
                        curr_frequency = item.split(':')[1].split('\n')[0]
                        feature_name = item.split(':')[0].lower()
                        ret = db.session.query(exists().where(Term.name == feature_name)).scalar()
                        if not ret:
                            new_feature = Term(name=feature_name)
                            db.session.add(new_feature)
                            db.session.commit()
                        else:
                            new_feature = Term.query.filter_by(name=feature_name).first()

                        new_model.w_features.append(new_feature)
#########################################
                        with open(new_feature_list, 'a') as txtfile:
                            txtfile.write(str(feature_count) + ':' + feature_name + '-' + curr_frequency + '\n')
                        print(str(feature_count) + ':' + feature_name + '-' + curr_frequency)
#########################################
                        feature_count += 1

            if new_model is None:
                continue
            db.session.add(new_model)
            db.session.commit()
    print('product database created')

# add the non-feature term defined by the user to non_features list of the product
def add_non_feature_term_to_DB(model_name, term_name):
    cur_model = Model.query.filter_by(name=model_name).first()
    cur_term = Term.query.filter_by(name=term_name).first()
    cur_model.w_features.remove(cur_term)
    cur_model.non_features.append(cur_term)
    db.session.commit()
    return
#
# categoryDB()
# productModelsDB()