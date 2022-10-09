import ibm_db
dictionary={}
def printTableData(conn):
    sql = "SELECT * FROM userdetails"
    out = ibm_db.exec_immediate(conn, sql)
    document = ibm_db.fetch_assoc(out)
    while document != False:
        dictionary.update({document['USERNAME']:document['PASSWORD']})
        document = ibm_db.fetch_assoc(out)
def insertTableData(conn,rollno,username,email,password):
    sql="INSERT INTO userdetails(rollno,username,email,password) VALUES ({},'{}','{}','{}')".format(rollno,username,email,password)
    out = ibm_db.exec_immediate(conn,sql)
    print('Number of affected rows : ',ibm_db.num_rows(out),"\n")


def updateTableData(conn,rollno,username,email,password):
    sql = "UPDATE userdetails SET (username,email,password)=('{}','{}','{}') WHERE rollno={}".format(username,email,password,rollno)
    out = ibm_db.exec_immediate(conn, sql)
    print('Number of affected rows : ', ibm_db.num_rows(out), "\n")

def deleteTableData(conn,username):
    sql = "DELETE FROM userdetails WHERE username={}".format(username)
    out = ibm_db.exec_immediate(conn, sql)
    print('Number of affected rows : ', ibm_db.num_rows(out), "\n")

try:
    conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=ba99a9e6-d59e-4883-8fc0-d6a8c9f7a08f.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=31321;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;PROTOCOL=TCPIP;UID=cll33761;PWD=JHRHpRtT82zDR0z6;", "", "")
    print("Db connected")

except:
    print("Error")



from flask import *
app=Flask(__name__)

@app.route("/")
@app.route("/login",methods=['POST','GET'])
def login(pbkdf2_sha256=None):
    if request.method=="POST":
        printTableData(conn)
        username=request.form['username']
        password=request.form['password']
        if dictionary[username] == password:
            return render_template('user.html',uname=username)
    return render_template('loginpage.html')


@app.route("/register",methods=['POST','GET'])
def register():
    if request.method=="POST":
        rollno = request.form['rollno']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        insertTableData(conn, rollno, username, email, password)
        #printTableData(conn)
        return render_template('loginpage.html')
    return render_template('registerpage.html')
@app.route("/delected")
def delected():

    return render_template('delectuser.html')
@app.route("/logout")
def logout():
    return redirect(url_for('login'))

#printTableData(conn)
#print(dictionary)


if __name__=="__main__":
    app.run(debug=True)