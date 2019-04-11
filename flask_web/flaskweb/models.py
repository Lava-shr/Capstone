from datetime import datetime
from flaskweb import db


class Category(db.Model):
    name = db.Column(db.String(100), primary_key=True)
    children = db.relationship('Category', backref='children_categories', remote_side=[name])
    parent_name = db.Column(db.String(100), db.ForeignKey('category.name'))
    # one-to-many relationship with Model
    models = db.relationship('Model', backref='parent_product')



    def __repr__(self):
        return "Category('{self.name}')"

# many-to-many relationship between Model and Term
model_feature = db.Table('model_feature',
                         db.Column('model_name', db.String(100), db.ForeignKey('model.name')),
                         db.Column('feature_name', db.String(100), db.ForeignKey('term.name'))
                         )
# many-to-many relationship between Model and Term
model_non_feature = db.Table('model_non_feature',
                         db.Column('model_name', db.String(100), db.ForeignKey('model.name')),
                         db.Column('nonfeature_name', db.String(100), db.ForeignKey('term.name'))
                             )

# model_evolution_list = db.Table('model_evolution_list',
#                                 db.Column('model_name', db.String(100), db.ForeignKey('model.name')),
#                                 db.Column('evolution_name', db.String(100), db.ForeighKey('excelterm.name'))
#                                 )
#
# model_revolution_g1 = db.Table('model_revolution_g1',
#                                 db.Column('model_name', db.String(100), db.ForeignKey('model.name')),
#                                 db.Column('revolution_g1_name', db.String(100), db.ForeighKey('excelterm.name'))
#                                 )
#
# model_revolution_g2 = db.Table('model_revolution_g2',
#                                 db.Column('model_name', db.String(100), db.ForeignKey('model.name')),
#                                 db.Column('revolution_g2_name', db.String(100), db.ForeighKey('excelterm.name'))
#                                 )

class Model(db.Model):
    name = db.Column(db.String(100), primary_key=True)
    # one-to-many relationship with Category
    product_name = db.Column(db.String(100), db.ForeignKey('category.name'))
    # many-to-many relationship with Term
    w_features = db.relationship('Term', secondary = model_feature, backref=db.backref('featureship_model', lazy='dynamic'))
    # many-to-many relationship with Term
    non_features = db.relationship('Term', secondary = model_non_feature, backref=db.backref('nonfeatureship_model', lazy='dynamic'))

    # evolution_list = db.relationship('ExcelTerm', secondary = model_evolution_list, backref=db.backref('evolutionship_model', lazy='dynamic'))
    # revolution_g1 = db.relationship('ExcelTerm', secondary = model_revolution_g1, backref=db.backref('revolution_g1_ship_model', lazy='dynamic'))
    # revolution_g2 = db.relationship('ExcelTerm', secondary = model_revolution_g2, backref=db.backref('revolution_g2_ship_model', lazy='dynamic'))


    def __repr__(self):
        return "Model('{self.name}')"

class Term(db.Model):
    name = db.Column(db.String(100), primary_key=True)

    def __repr__(self):
        return "Term('{self.name}')"

# class ExcelTerm(db.Model):
#     name = db.Column(db.String(100), primary_key=True)
#
#     def __repr__(self):
#         return "ExcelTerm('{self.name}')"


