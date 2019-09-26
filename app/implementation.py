from dbconnect import connection

import json


def getAllUsers2Flowers():
    try:
        c, conn = connection()

        data = c.execute('SELECT * FROM user2flower')
        data = c.fetchall()
        payload = []

        if data is not None and c.rowcount != 0:
            for userflower in data:
                date = userflower[3]
                date = date.strftime('%Y-%m-%d')
                content = {"user2flower_id": str(userflower[0]), "user_id": str(userflower[1]), "flower_id": str(userflower[2]), "date_of_inception": date,
                           "email": userflower[4]}
                payload.append(content)
            c.close()
            conn.close()
            return payload
        else:
            return {'msg': 'No data to return.'}
    except Exception as e:
        c.close()
        conn.close()
        print(e)
        return {'msg': 'Something went wrong while fetching users with flowers.'}, 500


def postUsers2Flowers(request):
    try:
        c, conn = connection()

        c.execute('INSERT INTO user2flower (user_id, flower_id, date_of_inception, email) values (%s, %s, %s, %s)', (str(request.json['user_id']), str(request.json['flower_id']), str(request.json['date_of_inception']), str(request.json['email'])))
        conn.commit()

        c.close()
        conn.close()
        return {"msg": "New user2flower added to DB."}, 201

    except Exception as e:
        c.close()
        conn.close()
        print(e)
        return {"msg": "Something went wrong while inserting user2flower to DB."}, 500


def getUser2flowerByID(user2flower_id):
    try:
        c, conn = connection()
        data = c.execute('SELECT * FROM user2flower where user2flower_id = ' + str(user2flower_id))
        data = c.fetchone()
        if data is not None and c.rowcount != 0:
            date = data[3]
            date = date.strftime('%Y-%m-%d')
            content = {"user2flower_id": str(data[0]), "user_id": str(data[1]),
                       "flower_id": str(data[2]), "date_of_inception": date,
                       "email": data[4]}
            c.close()
            conn.close()
            return content
        else:
            c.close()
            conn.close()
            return "No data to return."

    except Exception as e:
        c.close()
        conn.close()
        print(e)
        return {"msg": "Something went wrong while fetching user2flower by id."}, 500


def putUser2flowerByID(request, user2flower_id):
    try:
        c, conn = connection()

        data = getUser2flowerByID(user2flower_id)
        if data == "No data to return.":
            return postUsers2Flowers(request)
        else:
            putData = putDataCheck(request, data)
            if putData == "Something went wrong in mapping data.":
                return {"msg": "Something went wrong in mapping data."}, 500
            c.execute('UPDATE user2flower SET user2flower_id = %s, user_id = %s, flower_id = %s, date_of_inception = %s, email = %s WHERE user2flower_id = %s',(str(user2flower_id), putData[0], putData[1], putData[2], putData[3],  str(user2flower_id)))
            conn.commit()
            print("User2flower with user2flower_id " + str(user2flower_id) + " is updated.")

            c.close()
            conn.close()
            return {"msg": "User2flower with user2flower_id " + str(user2flower_id) + " is updated."}

    except Exception as e:
        c.close()
        conn.close()
        print(e)
        return {"msg": "Something went wrong while updating user2flower."}, 500


def deleteUser2flowerByID(user2flower_id):
    try:
        c, conn = connection()

        data = getUser2flowerByID(user2flower_id)
        if data == "No data to return.":
            return {"msg": "User2flower with user2flower_id " + str(user2flower_id) + " does not exist in DB."}
        else:
            c.execute('DELETE FROM user2flower WHERE user2flower_id = %s', (str(user2flower_id)))
            conn.commit()
            print("User2flower with user2flower_id " + str(user2flower_id) + " is deleted from DB.")

            c.close()
            conn.close()
            return {"msg": "User2flower with user2flower_id " + str(user2flower_id) + " is deleted from DB."}

    except Exception as e:
        c.close()
        conn.close()
        print(e)
        return {"msg": "Something went wrong while deleting user2flower"}, 500


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