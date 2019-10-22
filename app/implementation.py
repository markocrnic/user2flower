from dbquery import querydb
from schema import Schema, And, Use


def getAllUsers2Flowers():
    data = 'SELECT * FROM user2flower'
    return querydb(data, operation='GET', check='list')


def postUsers2Flowers(request):
    data = "INSERT INTO user2flower (user_id, flower_id, date_of_inception, email) values ('" + str(
        request.json['user_id']) + "', '" + str(request.json['flower_id']) + "', '" + str(
        request.json['date_of_inception']) + "', '" + str(request.json['email']) + "')"
    return querydb(data, operation='POST')


def getUser2flowerByID(user2flower_id):
    data = 'SELECT * FROM user2flower where user2flower_id = ' + str(user2flower_id)
    return querydb(data, 'GET', 'tuple', user2flower_id=user2flower_id)


def putUser2flowerByID(request, user2flower_id):
    data = getUser2flowerByID(user2flower_id)
    if data == "No data to return.":
        return postUsers2Flowers(request)
    else:
        putData = putDataCheck(request, data)
        if putData == "Something went wrong in mapping data.":
            return {"msg": "Something went wrong in mapping data."}, 500

        data = "UPDATE user2flower SET user2flower_id = '" + str(user2flower_id) + "', user_id = '" + putData[
            0] + "', flower_id = '" + putData[1] + "', date_of_inception = '" + putData[2] + "', email = '" + str(putData[
                   3]) + "' WHERE user2flower_id = '" + str(user2flower_id) + "'"
        return querydb(data, 'PUT', user2flower_id=user2flower_id)


def deleteUser2flowerByID(user2flower_id):

    data = getUser2flowerByID(user2flower_id)
    if data == "No data to return.":
        return {"msg": "User2flower with user2flower_id " + str(user2flower_id) + " does not exist in DB."}
    else:
        data = 'DELETE FROM user2flower WHERE user2flower_id = ' + (str(user2flower_id))
        return querydb(data, 'DELETE', user2flower_id=user2flower_id)


def putDataCheck(request, data):
    try:
        listData = []
        for field in data:
            listData.append(data[field])
        user_id = listData[1]
        flower_id = listData[2]
        date_of_inception = listData[3]
        email = listData[4]
        if 'user_id' in request.json:
            user_id = request.json['user_id']
        if 'flower_id' in request.json:
            flower_id = request.json['flower_id']
        if 'date_of_inception' in request.json:
            date_of_inception = request.json['date_of_inception']
        if 'email' in request.json:
            email = request.json['email']
        updateData = [user_id, flower_id, date_of_inception, email]

        return updateData
    except:
        return "Something went wrong in mapping data."


def getSchema():
    return Schema({'user_id': And(Use(int)),
                   'flower_id': And(Use(int)),
                   'date_of_inception': And(str, len),
                   'email': And(Use(bool))})
