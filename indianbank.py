from flask import Flask, jsonify, abort
import sqlite3

app = Flask(__name__)


@app.route('/ifsc/<string:ifsc>', methods=['GET'])
def get_by_ifsc(ifsc):
    ifsc = str(ifsc)
    con, cur = sqlite3, sqlite3.Connection
    try:
        con = sqlite3.connect('indian_banks.db')
        cur = con.cursor()
        data = cur.execute('SELECT * FROM branches WHERE ifsc=?', (ifsc,)).fetchone()
        data1 = cur.execute('pragma table_info(branches);').fetchall()
        if len(data) == 0:
            abort(404)
    except TypeError:
        abort(404)
    finally:
        cur.close()
        con.close()
    header = []
    for i in data1:
        header.append(i[1])
    result = {}
    for i in range(8):
        result[header[i]] = data[i]
    return jsonify(result)


@app.route('/branches/<string:city>/<string:bank_name>', methods=['GET'])
def get_by_city(city, bank_name):
    qcity = str(city).replace("+", " ")
    qbank_name = str(bank_name).replace("+", " ")
    con = sqlite3.connect('indian_banks.db')
    cur = con.cursor()
    data = cur.execute('SELECT * FROM branches WHERE city=? and bank_name=?', (qcity, qbank_name,)).fetchall()
    data1 = cur.execute('pragma table_info(branches);').fetchall()
    cur.close()
    con.close()
    header = []
    for i in data1:
        header.append(i[1])
    result = []
    for i in data:
        branch = {}
        for j in range(8):
            branch[header[j]] = i[j]
        result.append(branch)
    return jsonify({'data': result})


if __name__ == '__main__':
    app.run()
