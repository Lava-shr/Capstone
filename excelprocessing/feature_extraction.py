import xlrd
import xlsxwriter
from difflib import SequenceMatcher
import sys
import itertools
import os


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def readStopFile():
    file_location = 'stop words.xlsx'

    workbook = xlrd.open_workbook(file_location)

    sheet = workbook.sheet_by_name('Sheet1')
    x = []
    for rownum in range(sheet.nrows):
        x.append(sheet.cell(rownum, 0).value.lower())
    return x


def find_feature(product_name, model_column):
    sheet = workbook.sheet_by_name(product_name)
    x = []
    month = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
             'november', 'december']
    column = [0, 1, model_column]
    # model_name = sheet.cell(0, model_column).value #todo
    xsheet = xbook.add_worksheet(product_name)
    for rownum in range(1, sheet.nrows):

        for col in column:
            term = sheet.cell(rownum, col).value
            if is_number(term):
                print('term is float')
                continue
            term = term.lower().split()
            for t in term:
                # remove digits
                result = ''.join(i for i in t if not i.isdigit())
                if len(result) <= 2:
                    continue
                if result in month:
                    continue
                if result in x:
                    continue
                if result == 'yes' or result == 'no':
                    continue
                if result in stopping_words:
                    continue
                if result[0] == '-':
                    result = result[1:]
                if result[-1] == '-':
                    result = result[:-1]
                x.append(result)

    for i in range(len(x)):
        xsheet.write(i, 0, x[i])


def feature_to_tree(product_name, model_column):
    sheet = workbook.sheet_by_name(product_name)
    tree = {}
    current = 0
    for rownum in range(1, sheet.nrows):
        basic = sheet.cell(rownum, 0).value
        if not basic == '':
            current = basic
            tree[basic] = 0
        second = sheet.cell(rownum, 1).value
        third = sheet.cell(rownum, model_column).value
        if not second == '':
            tree[second] = current
        if not third == '':
            tree[third] = second
    return tree


def get_child_from_tree(tree, parent):
    children = []
    for key in tree:
        if tree[key] == parent:
            children.append(key)
    return children


def get_basic_from_tree(tree):
    return get_child_from_tree(tree, 0)


def compare_product_excel(product_one, product_two, model_one, model_two):
    tree_one = feature_to_tree(product_one, model_one)
    tree_two = feature_to_tree(product_two, model_two)

    basic_one = get_basic_from_tree(tree_one)
    basic_two = get_basic_from_tree(tree_two)
    evolution = []
    G1 = []
    G2 = []
    for x in basic_one:
        for y in basic_two:
            if check_synonym(x, y):
                child_x = get_child_from_tree(tree_one, x)
                child_y = get_child_from_tree(tree_two, y)
                basic = y
                child_list = check_child_list(child_x, child_y)
                for c in child_list[0]:
                    second = c
                    thirdlist = get_child_from_tree(tree_two, c)
                    third = ""
                    if (len(thirdlist) == 1):
                        third += str(thirdlist[0])
                    evolution.append([basic, second, third])
                    # print('evolution append: {}'.format([basic, second, third]))
                for c in child_list[1]:
                    second = c
                    thirdlist = get_child_from_tree(tree_two, c)
                    third = ""
                    if (len(thirdlist) == 1):
                        third += str(thirdlist[0])
                    G2.append([basic, second, third])
                    # print('G2 append: {}'.format([basic, second, third]))

                basic_two.remove(y)

    for b in basic_two:
        for second in get_child_from_tree(tree_two, b):
            thirdlist = get_child_from_tree(tree_two, second)
            third = ""
            if (len(thirdlist) == 1):
                third += str(thirdlist[0])
            G1.append([tree_two[second], second, third])
    evolution, G2, G1 = remove_duplicate(evolution, G2, G1)
    result = {'evolution': evolution, 'G1': G1, 'G2': G2}
    return result


def remove_duplicate(list1, list2, list3):
    new_list1 = []
    new_list2 = []
    new_list3 = []
    for x in list3:
        if x not in new_list3 and x not in list2 and x not in list1:
            new_list3.append(x)
    for x in list2:
        if x not in new_list2 and x not in list1:
            new_list2.append(x)
    for x in list1:
        if x not in new_list1:
            new_list1.append(x)
    return new_list1, new_list2, new_list3


def compare_two_string(string1, string2):
    return SequenceMatcher(None, string1.lower(), string2.lower()).quick_ratio()


def check_synonym(word1, word2):
    if compare_two_string(word1, word2) >= 0.7: #and len(word1) > 2 and len(word2) > 2:
        return 1
    else:
        return 0


def check_child(word1, word2):
    if compare_two_string(word1, word2) >= 0.5:# and len(word1) > 2 and len(word2) > 2:
        return 1
    else:
        return 0


def check_child_list(list1, list2):
    list = [[], []]
    # for x in list1:
    #     for y in list2:
    #         if check_child(x, y):
    #             list[0].append(y)
    #         else:
    #             list[1].append(y)
    for y in list2:
        flag = 0
        for x in list1:
            if check_child(x, y):
                list[0].append(y)
                flag = 1
        if not flag:
            list[1].append(y)
    return list


def display_list(result):
    evolution = result['evolution']
    G1 = result['G1']
    G2 = result['G2']
    print("Evolution")
    for x in evolution:
        print(x[0] + " -> " + x[1] + " -> " + x[2])
    print("Revolution-G1")
    for x in G1:
        print(x[0] + " -> " + x[1] + " -> " + x[2])
    print("Revolution-G2")
    for x in G2:
        print(x[0] + " -> " + x[1] + " -> " + x[2])


stopping_words = readStopFile()
file_location = 'All products.xlsx'
workbook = xlrd.open_workbook(file_location)
products = ['Mobile', 'CAMERA', 'Monitors', 'TV', 'Tablet', 'Mp3 Player', 'Video Game console', 'Desktop PC', 'Printer',
            'Laptop1']
model = [3, 3, 4, 4, 3, 3, 3, 5, 2, 3]
# xbook = xlsxwriter.Workbook('features_from_excel.xlsx')
# for i in range(10):
#     print(str(i) + ': Finding features for ' + products[i])
#     find_feature(products[i], model[i])

for i in range(10):
    txtpath = 'lists/' + products[i]+".txt"
    sys.stdout = open(txtpath, "w+", encoding='utf-8')
    display_list(compare_product_excel(products[0], products[i], model[0], model[i]))

# xbook.close()
