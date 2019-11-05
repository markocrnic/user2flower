from flask import Flask, request
from flask_cors import CORS
from api_management.jaeger import initializejaeger
from flask_opentracing import FlaskTracing
import implementation as implementation

app = Flask(__name__)
CORS(app)

jaeger_tracer = initializejaeger()
tracing = FlaskTracing(jaeger_tracer)


@app.route('/users2flowers/', methods=['GET', 'POST'])
@tracing.trace()
def user2flowerGlobal():
    with jaeger_tracer.start_active_span(
            'Users2flowers-API endpoint /users2flowers/') as scope:
        scope.span.log_kv({'event': 'Calling endpoint /users2flowers/', 'request_method': request.method})
        try:
            if request.method == 'GET':
                data = implementation.getAllUsers2Flowers()
                return data
            elif request.method == 'POST':
                try:
                    schema = implementation.getSchema()
                    schema.validate(request.json)
                except:
                    return {'msg': 'Data is not valid.'}, 403
                pass
                return implementation.postUsers2Flowers(request)
        except:
            return {'msg': 'Something went wrong at /users2flowers/'}, 500


@app.route('/users2flowers/<int:user2flower_id>/', methods=['GET', 'PUT', 'DELETE'])
@tracing.trace()
def user2flowerWithID(user2flower_id):
    with jaeger_tracer.start_active_span(
            'Users2flowers-API endpoint /users2flowers/<int:user2flower_id>/') as scope:
        scope.span.log_kv({'event': 'Calling endpoint /users2flowers/<int:user2flower_id>/', 'request_method': request.method})
        try:
            if request.method == 'GET':
                return implementation.getUser2flowerByID(user2flower_id)
            elif request.method == 'PUT':
                return implementation.putUser2flowerByID(request, user2flower_id)
            elif request.method == 'DELETE':
                pass
                return implementation.deleteUser2flowerByID(user2flower_id)
            else:
                return {"msg": "Check request again."}, 403
        except Exception as e:
            print(e)
            return {"msg": "Something went wrong at /users2flowers/<int:user2flower_id>"}, 500


@app.route('/users2flowers/user/<int:user_id>/', methods=['GET'])
@tracing.trace()
def usersFlowersByUserID(user_id):
    with jaeger_tracer.start_active_span(
            'Users2flowers-API endpoint /users2flowers/user/<int:user_id>/') as scope:
        scope.span.log_kv({'event': 'Calling endpoint /users2flowers/user/<int:user_id>/', 'request_method': request.method})
        try:
            if request.method == 'GET':
                return implementation.getUsersFlowersByUserID(user_id)
            else:
                return {"msg": "Check request again."}, 403
        except Exception as e:
            print(e)
            return {"msg": "Something went wrong at /users2flowers/<int:user_id>"}, 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)