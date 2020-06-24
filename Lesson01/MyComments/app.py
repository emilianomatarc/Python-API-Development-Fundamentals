from flask import Flask, jsonify, request
from http import HTTPStatus

# Create a WSGI server (Web Server Gateway Interface).
# It is used to forward requests from a web server (such as Apache or NGINX) to
# a backend Python web application or framework.
app = Flask(__name__)

recipes = [
    {
        'id': 1,
        'name': 'Egg Salad',
        'description': 'This is a lovely egg salad recipe.'
    },
    {
        'id': 2, 'name': 'Tomato Pasta',
        'description': 'This is a lovely tomato pasta recipe.'
    }
]


@app.route('/recipes', methods=['GET'])
def get_recipes():
    # Converts internal data to json format and
    # puts the recipes information inside 'data' field
    # in the json response
    return jsonify({'data': recipes})


@app.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    # Gets next recipe with id equal to recipe_id
    # Takes an iterator and a default value
    recipe = next((recipe for recipe in recipes if recipe['id'] == recipe_id), None)

    if recipe:
        return jsonify(recipe)

    return jsonify({'message': 'recipe not found'}), HTTPStatus.NOT_FOUND


@app.route('/recipes', methods=['POST'])
def create_recipe():
    # When the Flask application handles a request, it creates a Request object based on
    # the environment it received from the WSGI server (Apache -> WSGIServer -> Request)
    # The method get_json parses the incoming JSON request data and returns it
    data = request.get_json()

    name = data.get('name')
    description = data.get('description')

    recipe = {
        'id': len(recipes) + 1,
        'name': name,
        'description': description
    }

    recipes.append(recipe)

    return jsonify(recipe), HTTPStatus.CREATED


@app.route('/recipes/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    recipe = next((recipe for recipe in recipes if recipe['id'] == recipe_id), None)

    if not recipe:
        return jsonify({'message': 'recipe not found'}), HTTPStatus.NOT_FOUND

    data = request.get_json()

    # The update() method updates the dictionary with the elements from the another dictionary object or
    # from an iterable of key/value pairs
    recipe.update(
        {
            'name': data.get('name'),
            'description': data.get('description')
        }
    )

    return jsonify(recipe)


@app.route('/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    recipe = next((recipe for recipe in recipes if recipe['id'] == recipe_id), None)

    if not recipe:
        return jsonify({'message': 'recipe not found'}), HTTPStatus.NOT_FOUND

    recipes.remove(recipe)

    return '', HTTPStatus.NO_CONTENT


if __name__ == '__main__':
    app.run()
