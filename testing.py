from flask import *
import sqlite3
import sqlite3 as sql
conn = sqlite3.connect('toDoList.db')
print "Opened database successfully";
"""
conn.execute('CREATE TABLE table_items5(itemId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, itemList TEXT NOT NULL )')
print "Table created successfully";
conn.close()"""

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/enternew')
def new_task():

    con = sql.connect("toDoList.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from table_items5 ORDER BY itemId")

    rows = cur.fetchall();
    return render_template('student.html', rows=rows)

@app.route('/add', methods=['POST', 'GET'])
def add():
    print "i am alive"
    if request.method == 'POST':
        try:
            itemList = request.form["todoItem"]
            print itemList
            itemId = request.form['itemId']
            #id = 'NULL'

            with sql.connect("toDoList.db") as con:
                cur = con.cursor()

                cur.execute('INSERT INTO table_items5 (itemId,itemList) VALUES(?,?)', (itemId,itemList))
                lid = cur.lastrowid
                print "The last Id of the inserted row is %d" % lid
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "Try using a different item number"

        finally:
            return  redirect(url_for('new_task'))

            con.close()


@app.route('/index')
def updateRecord():
    con = sql.connect("toDoList.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from table_items5 ORDER BY itemId")

    rows = cur.fetchall();
    return render_template('index.html', rows= rows)

@app.route('/task_update', methods=['POST', 'GET'])
def task_update():
    if request.method == 'POST':
        try:
            itemId = request.form['itemId']
            replaceItem = request.form['itemList']

            print itemId
            print replaceItem

            with sql.connect("toDoList.db") as con:
                cur = con.cursor()

                cur.execute("UPDATE table_items5 SET  itemList = ? WHERE itemId = ?", (replaceItem,itemId))

                con.commit()
                msg = "Record successfully updated"
        except:
            con.rollback()
            msg = "error in update operation"

        finally:
            return  redirect(url_for('new_task'))
            con.close()

@app.route('/task_delete', methods=['POST', 'GET'])
def task_delete():

    if request.method == 'POST':
        try:
            itemId = request.form['itemId']
            with sql.connect("toDoList.db") as con:
                cur = con.cursor()

                cur.execute("DELETE FROM  table_items5  WHERE itemId = ?", (itemId))

                con.commit()
                msg = "Record successfully updated"
        except:
            con.rollback()
            msg = "sorry, deleting this item is not possible"

        finally:
            return redirect(url_for('new_task'))
            con.close()

@app.route('/index')
def list():
    con = sql.connect("toDoList.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from table_items5 ORDER BY itemId")

    rows = cur.fetchall();
    return render_template("index.html", rows=rows)

@app.route('/index')
def item_delete():
    con = sql.connect("toDoList.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from table_items5 ORDER BY itemId")

    rows = cur.fetchall();
    return render_template("index.html", rows=rows)


if __name__ == '__main__':
    app.run(debug=True)


