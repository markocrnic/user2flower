from dbquery import querydb


def getAllUsers2Flowers():

    data = 'SELECT * FROM user2flower'
    return querydb(data, operation='GET', check='list')


def postUsers2Flowers(request):

    return querydb("", operation='POST', request=request)


def getUser2flowerByID(user2flower_id):

    data = 'SELECT * FROM user2flower where user2flower_id = ' + str(user2flower_id)
    return querydb(data, 'GET', 'tuple', user2flower_id=user2flower_id)


def putUser2flowerByID(request, user2flower_id):

    return querydb("", 'PUT', user2flower_id=user2flower_id, request=request)


def deleteUser2flowerByID(user2flower_id):

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

