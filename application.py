import os
from flask import Flask, redirect, url_for, request, render_template, current_app
from forms import RecipeForm, SearchForm
import pandas as pd
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asfhdasfhbakwjbkfefr7y57y47rjbfkabzfcbhafbka'
app.config['SUBMITTED_DATA'] = os.path.join('static', 'data_dir','')
app.config['SUBMITTED_IMG'] = os.path.join('static', 'image_dir','')

@app.route('/')
def hello_world():
    """
    Function to show example instance
    :return:
    """
    return render_template('index.html')

@app.route('/add_recipe', methods = ['POST', 'GET'])
def add_recipe():
    """
    Function add a Recipe using a manual form
    :return:
    """
    if request.method == 'POST':
        recipename = request.form['fname']
        print(recipename)
        return "Recipe added successfully"
    else:
        return render_template('add_recipe_manual.html')

@app.route('/add_recipe_auto', methods = ['POST', 'GET'])
def add_recipe_auto():
    """
    Function to use in built methods to add a recipe, with file handling
    :return:
    """
    form = RecipeForm()
    if form.validate_on_submit():
        recipe_name = form.recipe_name.data
        recipe_ingredients = form.recipe_ingredients.data
        recipe_prep_instructions = form.recipe_prep_instructions.data
        recipe_serving_instructions = form.recipe_serving_instructions.data
        pic_filename = recipe_name.lower().replace(" ", "_") + '.' + secure_filename(form.recipe_picture.data.filename).split('.')[-1]
        form.recipe_picture.data.save(os.path.join(app.config['SUBMITTED_IMG'] + pic_filename))
        df = pd.DataFrame([{'name': recipe_name, 'ingredients': recipe_ingredients, 'preparations': recipe_prep_instructions, 'instructions':recipe_serving_instructions, 'pic': pic_filename}])
        df.to_csv(os.path.join(app.config['SUBMITTED_DATA'] + recipe_name.lower().replace(" ", "_") + '.csv'))
        return redirect(url_for('hello_world'))
    else:
        return render_template('add_recipe_auto.html', form=form)


@app.route('/display_data/<name>')
def render_information(name):
    """
    Function to return the required information
    :param name: Name of the recipe
    :return:
    """
    df = pd.read_csv(os.path.join(app.config['SUBMITTED_DATA'] + name.lower().replace(" ", "_") + '.csv'), index_col=False)
    return render_template('view_recipe.html', recipe=df.iloc[0])

@app.route('/view_all_recipes_auto')
def view_all_recipes_auto():
    """
    Shows all recipes added
    :return:
    """
    files = os.listdir(app.config['SUBMITTED_DATA'])
    viewRecipes = []
    counter = 0
    df = pd.DataFrame()
    for file in files:
        if counter == 0:
            df = pd.read_csv('static/data_dir/' + file)
        else:
            newDF = df
            df = pd.read_csv('static/data_dir/' + file)
            df = pd.concat([df, newDF])
        counter += 1
    for counter in range(0, len(df.index)):
        viewRecipes.append([df.iloc[counter][5], df.iloc[counter][1], df.iloc[counter][1].replace(" ", "_")])
    return render_template('view_all_recipes_auto.html', recipes=viewRecipes)

@app.route('/search_recipe_auto', methods = ['GET', 'POST'])
def search_recipe_auto():
    """
    Function to use in built methods to search recipe based on stored CSV.
    Search for recipe by name or by ingredient. Search names first, then try
    ingredients.
    :return:
    """
    search_form = SearchForm()
    if search_form.validate_on_submit():
        search_name = request.form['search_name']
        files = os.listdir(app.config['SUBMITTED_DATA'])
        for file in files:
            df = pd.read_csv('static/data_dir/' + file)
            if df['name'][0].lower() == search_name.lower():
                return render_template('view_recipe.html', recipe=df.iloc[0])
            else:
                return render_template('search_recipe_auto.html', search_form=search_form)
    else:
        return render_template('search_recipe_auto.html', search_form=search_form)


@app.route('/remove_recipe_auto', methods= ['GET', 'POST'])
def remove_recipe_auto():
    """
    Function to remove recipe based on stored CSV.
    :return:
    """
    search_form = SearchForm()
    if search_form.validate_on_submit():
        search_name = request.form['search_name']
        files = os.listdir(app.config['SUBMITTED_DATA'])
        for file in files:
            df = pd.read_csv('static/data_dir/' + file)
            if df['name'][0].lower() == search_name.lower():
                os.remove(app.config['SUBMITTED_DATA'] + search_name.lower().replace(" ", "_") + '.csv')
                return render_template('index.html')
            else:
                return render_template('remove_recipe_auto.html', search_form=search_form)
    else:
        return render_template('remove_recipe_auto.html', search_form=search_form)


@app.route('/admin')
def hello_admin():
    """
    Example for a sample page
    :return: string
    """
    return "Hello Admin"

@app.errorhandler(404)
def page_not_found(e):
    """
    Standard error handling mechanism
    :param e: Error details
    :return:
    """
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)