import pymysql
from flask import jsonify, request

from app import app
from config import mysql


@app.route('/orderdetails', methods=['POST'])
def orderdetails():
    try:
        if request.method == 'POST':
            if not request.is_json:
                return jsonify({"msg": "Missing JSON in request"}), 400
            ordnum = request.json.get('ordnum', None)
            if not ordnum:
                return jsonify({"msg": "Missing ordnum parameter"}), 400
            try:
                conn = mysql.connect()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                cursor.execute("SELECT * FROM orderdetails WHERE orderNumber = %s", ordnum)
                ordrows = cursor.fetchall()
                if not ordrows:
                    return '', 404
                response = jsonify(ordrows)
                return response, 200
            except Exception as e:
                print(e)
            finally:
                cursor.close()
                conn.close()
        else:
            return 'Hello', 200
    except Exception as e:
        print(e)
        return 'Bad Request', 400

@app.route('/ordersummary', methods=['POST'])
def ordersummary():
    try:
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        custnum = request.json.get('custnum', None)
        if not custnum:
            return jsonify({"msg": "Missing custnum parameter"}), 400
        try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM orders WHERE customerNumber = %s", custnum)
            custordrows = cursor.fetchall()
            if not custordrows:
                return '', 404
            response = jsonify(custordrows)
            return response, 200
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
    except Exception as e:
        print(e)
        return 'Bad Request', 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
