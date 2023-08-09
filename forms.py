from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField
from wtforms.fields import StringField, TextAreaField
from wtforms.fields.html5 import DateField, EmailField, TelField
from wtforms.validators import DataRequired, Length

class RecipeForm(FlaskForm):
    recipe_name = StringField('Recipe Name:', validators=[DataRequired()])
    recipe_ingredients = StringField('Recipe Ingredients:', validators=[DataRequired()])
    recipe_prep_instructions = TextAreaField('Preparation Instructions:', validators=[DataRequired()])
    recipe_serving_instructions = TextAreaField('Serving Instructions:', validators=[DataRequired()])
    recipe_picture = FileField('Recipe Picture:', validators=[FileRequired()])

class SearchForm(FlaskForm):
    search_name = StringField('', validators=[DataRequired()])