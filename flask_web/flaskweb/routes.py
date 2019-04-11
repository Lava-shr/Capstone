from flask import render_template, url_for, flash, redirect, request
from flaskweb import app
from flaskweb.forms import RegistrationForm, LoginForm, TypeForm, CategoryForm, ThresholdForm
# from flaskweb.db_operation import find_category, tree_structure_display, one_level_below_product, getAllcategories, final_product
from flaskweb.db_operation import *
from flaskweb.models import *
from update_db import categoryDB, productModelsDB, add_non_feature_term_to_DB
from three_lists_from_excel import *

our_reference_model = 'Samsung Galaxy S III'

# our_reference_product = None


@app.route("/", methods=['GET', 'POST'])
@app.route("/reference_product_selection", methods=['GET', 'POST'])
def reference_product_selection():
    from shutil import copyfile
    import os
    copyfile(os.getcwd() + '/flaskweb/site_original.db', os.getcwd() + '/flaskweb/site.db')
    form = TypeForm()
    if form.validate_on_submit():
        return render_template('category_found.html', title='Category', form=form, result=find_category(form.target.data))

    return render_template('reference_product_selection.html', title='YourProduct', form=form)

@app.route("/identify_category/<target_product>", methods=['GET', 'POST'])
def identify_category(target_product):
    # global our_reference_product
    # our_reference_product = target_product
    ctg = find_category(target_product)
    return render_template('identify_category.html', ctg=ctg)

@app.route("/select_categories", methods=['GET', 'POST'])
def select_categories():
    # global our_reference_product
    # global our_reference_model
    if request.method == "POST":
        original_selection = request.form.getlist("original")
        second_selection = request.form.getlist("check1")
        third_selection = request.form.getlist("check2")
        final_selection = request.form.getlist("check3")

        # setting up multi dictionary for the original selection
        next_list = {}
        for selection in original_selection:
            next_list.setdefault(selection , [])

        # Deciding on which selection level we are at
        if(len(second_selection) > 0):
            next_list = {}
            final_list = []
            for selection in second_selection:
                next_list.setdefault(selection , [])
            for product in second_selection:
                product_list = one_level_below_product(product)
                if(len(product_list) == 0):
                    final_list.append(product)
                for k in product_list:
                    next_list[product].append(k)
            
             # Do display the final products from excel file if no 3rd level for all the product selected        
            final_stage = True
            for product in second_selection:
                product_list = one_level_below_product(product)
                if(len(product_list) > 0):
                    final_stage = False
                    break

            if(final_stage):
                for k in second_selection:
                    final_list.append(k)
                next_list2 = {}
                for selection in final_list:
                    next_list2.setdefault(selection, [])
                for selection in final_list:
                    xlx_list = final_product(selection, our_reference_model)
                    
                    for k in xlx_list:
                        next_list2[selection].append(k)
                return render_template('display_products.html' , title='Product Display' , target_ctg=final_list, final_list=final_list , next_level = next_list2)
            else:
                return render_template('select_category_2.html' , title='CategoriesSelection' , original_list=original_selection, next_level=next_list , final_list=final_list )


        if(len(third_selection) > 0):
            next_list = {}
            final_list = request.form.getlist("final_list")
            for selection in third_selection:
                next_list.setdefault(selection , [])
            for product in third_selection:
                product_list = one_level_below_product(product)
                if(len(product_list) == 0):
                    final_list.append(product)
                for k in product_list:
                    next_list[product].append(k)

            # Do display products if no 4th level for all the product selected        
            final_stage = True
            for product in third_selection:
                product_list = one_level_below_product(product)
                if(len(product_list) > 0):
                    final_stage = False
                    break

            if(final_stage):
                for k in third_selection:
                    final_list.append(k)
                next_list3 = {}
                for selection in final_list:
                    next_list3.setdefault(selection, [])
                for selection in final_list:
                    xlx_list = final_product(selection, our_reference_model)
                    # print('For selection {}, its final_product is {}'.format(selection, xlx_list))
                    for k in xlx_list:
                        next_list3[selection].append(k)
                # remove duplicate
                for product, model in next_list3.items():
                    newlist = []
                    for m in model:
                        if m not in newlist:
                            newlist.append(m)
                    next_list3[product] = newlist

                # print('products lists: {}'.format(next_list3))
                return render_template('display_products.html' , title='Product Display' , target_ctg=final_list, final_list=final_list , next_level = next_list3)
            else:
                return render_template('select_category_3.html' , title='CategoriesSelection' , original_list=original_selection, next_level=next_list , final_list=final_list )

        if(len(final_selection) > 0):
            final_list = request.form.getlist("final_list")
            for k in final_selection:
                final_list.append(k)
            next_list = {}
            for selection in final_list:
                next_list.setdefault(selection, [])
            for selection in final_list:
                xlx_list = final_product(selection, our_reference_model)
                for k in xlx_list:
                    next_list[selection].append(k)

            return render_template('display_products.html' , title='Product Display' , target_ctg=final_list, final_list=final_list , next_level = next_list)
        
        for product in original_selection:
            product_list = one_level_below_product(product)
            for k in product_list:
                next_list[product].append(k)
        if(len(original_selection) < 1):
            form = CategoryForm()
            form.categories.choices = [(ctg.name, ctg.name) for ctg in Category.query.filter_by(parent_name=None).all()]
            # print('our_reference_product: ' + our_reference_product)
            return render_template('select_categories.html', title='CategoriesSelection', form=form)
        
        return render_template('select_category_1.html' , title='CategoriesSelection', original=original_selection , next_level=next_list)
        

    form = CategoryForm()
    form.categories.choices = [(ctg.name, ctg.name) for ctg in Category.query.filter_by(parent_name=None).all()]
    # print('2 our_reference_product: ' + our_reference_product)
    return render_template('select_categories.html', title='CategoriesSelection', form=form)

@app.route("/display_products", methods=['GET', 'POST'])
def display_products():
    return render_template('display_products.html', title='Products')

@app.route("/display_products2", methods=['GET', 'POST'])
def display_products2():
    model_selection = request.form.getlist("display_products")
    return render_template('display_products2.html', title='Products' , model_selection=model_selection)

@app.route("/select_category_1", methods=['GET', 'POST'])
def select_category_1():
    return render_template('select_category_1.html' , title='First Selection')

@app.route("/feature_display", methods=['GET', 'POST'])
def feature_display():
    if request.method == "POST":
        selection = request.form.getlist("original")

        selection.insert(0, "Samsung Galaxy S III")
        feature_list = {}

        for s in selection:
            feature_list.setdefault(s , [])    

        for product in selection:
            features = features_display(product)
            for l in features:
                if l in feature_list[product]:
                    continue
                feature_list[product].append(l)
        

    return render_template('feature_display.html' , title='Feature',  selection=feature_list)


@app.route("/matrix_display", methods=['GET', 'POST'])
def matrix_display():
    if request.method == "POST":
        selection = request.form.getlist("original")
        #for i in selection:
        #    print("Matrix display: " + i)
        # Deleting the features that user thinks are redundant

        for i in selection:
            a = "name" + i
            #print(a)
            non_feature = request.form.getlist(a)
            for k in non_feature:
                add_non_feature_term_to_DB(i , k)
        
        
        # Now comparing all the feature between S3 and all product selected by user
        # then calculate cosine similarity
        s3_feature = features_display("Samsung Galaxy S III")
        selection.remove("Samsung Galaxy S III")
        width =  len(selection)
        height = len(s3_feature)+1
        matrix = [[0 for x in range(width)] for y in range(height)] 

        for counter, feature in enumerate(s3_feature):
            for index, product in enumerate(selection):
                matrix[counter][index] = doesFeatureExit(product,feature)

        # Cosine similarity
        s3_feature.append("Cosine Similarity")        
        for counter, product in enumerate(selection):
            matrix[height-1][counter] = round(computeCosineSimilarity("Samsung Galaxy S III" , product),3)

        final_matrix = zip(s3_feature , matrix)
        selection = request.form.getlist("original")
    return render_template('matrix_display.html' , title='Matrix display Selection', selection=selection, matrix=final_matrix )


@app.route("/threshold", methods=['GET', 'POST'])
def threshold():
    if request.method == "POST":
        selection = request.form.getlist("original")
        #for i in selection:
            #print("Threshold: " + i)
        reason=""
        form = ThresholdForm()
        return render_template('threshold.html' , title='Threshold Selection' , form= form , reason=reason, selection=selection)

    selection=[]
    reason=""
    return render_template('threshold.html' , title='Threshold Selection' , form= form , reason=reason, selection=selection)


@app.route("/display_similar_products", methods=['GET', 'POST'])
def display_similar_products():
    if request.method == "POST" :
        selection = request.form.getlist("original")
        form = ThresholdForm(request.form)

        if(len(request.form["lowerlimit"]) < 1 or len(request.form["upperlimit"]) < 1 or not is_convertible_to_float(request.form["lowerlimit"]) or not is_convertible_to_float(request.form["upperlimit"])):
            form1 = ThresholdForm()
            reason = "Threshold wasn't valid. Please re-enter it again"
            return render_template('threshold.html' , title='Threshold Selection' , form= form1, reason=reason, selection= selection)
        

        lowerlimit = float(request.form["lowerlimit"])
        upperlimit = float(request.form["upperlimit"])

        if lowerlimit <0 or lowerlimit >1 or upperlimit >1 or upperlimit < 0:
            form1 = ThresholdForm()
            reason = "Please have the threshold limit inside 0 and 1"
            return render_template('threshold.html' , title='Threshold Selection' , form= form1, reason=reason, selection=selection)
        

        if lowerlimit >= upperlimit:
            form2 = ThresholdForm()
            reason = "Please put lower limit smaller than upperlimt"
            return render_template('threshold.html' , title='Threshold Selection' , form= form2, reason=reason, selection=selection)
        
        #def find_similar(lower_threshold, upper_threshold, shortlisted_model_names, reference_model_name):

        similar_product = find_similar(lowerlimit,upperlimit,selection ,"Samsung Galaxy S III")
        return render_template('display_similar_products.html' , title='Similar Products',selection=similar_product)

def is_convertible_to_float(value):
    try:
        float(value)
        return True
    except:
        return False


@app.route("/evolution_list", methods=['GET', 'POST'])
def evolution_list():
    if request.method == "POST" :
        selection = request.form.getlist("original")
        selection.insert(0 , "Samsung Galaxy S III")

        evolutionlist = {}

        for s in selection:
            evolutionlist.setdefault(s , []) 

        for s in selection:
            evolutionlist[s].append(evolutionList(s))
        return render_template("evolution_list.html" , title = "Evolution List", selection=selection, evolutionlist=evolutionlist)


@app.route("/revolution_list_g1", methods=['GET', 'POST'])
def revolution_list_g1():
    if request.method == "POST" :
        selection = request.form.getlist("original")
        revolutionlist_g1 = {}

        for s in selection:
            revolutionlist_g1.setdefault(s , []) 

        for s in selection:
            revolutionlist_g1[s].append(revolutionG1(s))
        return render_template("revolution_list_g1.html" , title = "Revolution List G1", selection=selection, revolutionlist=revolutionlist_g1)


@app.route("/revolution_list_g2", methods=['GET', 'POST'])
def revolution_list_g2():
    if request.method == "POST" :
        selection = request.form.getlist("original")
        revolutionlist_g2 = {}

        for s in selection: 
            revolutionlist_g2.setdefault(s , []) 

        for s in selection:
            revolutionlist_g2[s].append(revolutionG2(s))
        return render_template("revolution_list_g2.html" , title = "Revolution List G2", selection=selection, revolutionlist=revolutionlist_g2)
        
# @app.route("/display_products", methods=['GET', 'POST'])
# def display_products():
#     cat = request.form["object"]
#     content = ''
#     content = tree_structure_display(cat, 0, len(cat), content)
#     return render_template('display_products.html', title='Products', tree_structure=content)


# Footer Page

@app.route("/faq" , methods=['GET'])
def faq():
    return render_template('faq.html', title='Frequently asked products')

@app.route("/privacypolicy" , methods=['GET'])
def privacypolicy():
    return render_template('privacypolicy.html' , title= 'Privacy Policy')

@app.route("/sitemap" , methods=['GET'])
def sitemap():
    return render_template('sitemap-ideastudio.html' , title= 'Sitemap')

@app.route("/aboutus" , methods=['GET'])
def aboutus():
    return render_template('aboutus-ideastudio.html' , title= 'About us')

@app.route("/contactus" , methods=['GET'])
def contactus():
    return render_template('contactus.html' , title= 'Contact us')

@app.route("/feedback" , methods=['GET'])
def feedback():
    return render_template('feedbackform.html' , title= 'Feed back')



# 1st page reference_product_selection.html
# 2nd category_found.html
# 3rd page select_categories.html 
# 4th page display_products.html