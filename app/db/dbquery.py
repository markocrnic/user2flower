from db.dbconnect import connection
from flask import jsonify


def querydb(data, operation, check=None, user2flower_id=None):
    try:
        c, conn = connection()
        if c == {'msg': 'Circuit breaker is open, reconnection in porgress'}:
            return c, 500

        if operation == 'POST':

            c.execute(data)
            conn.commit()

            c.close()
            conn.close()
            return {"msg": "New user2flower added to DB."}, 201

        if operation == 'GET':

            c.execute(data)

            if check == 'list':
                data = c.fetchall()
                payload = []

                if data is not None and c.rowcount != 0:
                    for userflower in data:
                        date = userflower[3]
                        date = date.strftime('%Y-%m-%d')
                        content = {"user2flower_id": str(userflower[0]), "user_id": str(userflower[1]),
                                   "flower_id": str(userflower[2]), "date_of_inception": date,
                                   "email": userflower[4]}
                        payload.append(content)
                    c.close()
                    conn.close()
                    return jsonify(payload)
                else:
                    return {'msg': 'No data to return.'}

            if check == 'tuple':
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

        if operation == 'PUT':

            c.execute(data)
            conn.commit()
            print("User2flower with user2flower_id " + str(user2flower_id) + " is updated.")

            c.close()
            conn.close()
            return {"msg": "User2flower with user2flower_id " + str(user2flower_id) + " is updated."}

        if operation == 'DELETE':

            c.execute(data)
            conn.commit()
            print("User2flower with user2flower_id " + str(user2flower_id) + " is deleted from DB.")

            c.close()
            conn.close()
            return {"msg": "User2flower with user2flower_id " + str(user2flower_id) + " is deleted from DB."}

    except Exception as e:
        c.close()
        conn.close()
        print(e)
        return {'msg': 'Something went wrong while executing ' + operation + ' operation on users2flowers.'}, 500