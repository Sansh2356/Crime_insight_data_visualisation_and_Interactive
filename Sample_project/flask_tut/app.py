from psycopg2 import sql
from flask import Flask,redirect,url_for,render_template,request
import mysql.connector
from mysql.connector import Error
app = Flask(__name__)


#creating a server connection through mysql
def create_server_connection(hostname,username,userpassword):

  try:
    connection=mysql.connector.connect(
        host=hostname,
        user=username,
        passwd=userpassword
    )
    print('MySql Database connection success')
  except Error as err:
    print('Error  ')
    print(err)
  return connection


pw = "Shweta@123"
db="project_schema"
connection=create_server_connection("localhost","root",pw)




#Creating database connection
def create_db_connection(host_name,user_name,user_password,db_name):
  connection=None
  try:
    connection=mysql.connector.connect(
      host=host_name,
      user=user_name,
      passwd=user_password,
      database = db_name 
    )
    print("Mysql database connection successful")
  except Error as err:
    print(err)
  return connection



#Executing query
def execute_query(connection,query):
    
    cursor=connection.cursor()
    try:
      cursor.execute(query)
      connection.commit()
      print('Query executed successfully')
    except Error as err:
      print(err)

connection=create_db_connection("localhost","root",pw,db)
# BAD EXAMPLE. DON'T DO THIS!
def count_rows(table_name: str) -> int:
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                count(*)
            FROM
                %(table_name)s
        """, {
            'table_name': table_name,
        })
        result = cursor.fetchone()

    rowcount, = result
    return rowcount


  #A Decent example using sql composition by psycopg2 module
def count_rows(table_name: str) -> int:
    with connection.cursor() as cursor:
        stmt = sql.SQL("""
            SELECT
                count(*)
            FROM
                {table_name}
        """).format(
            table_name = sql.Identifier(table_name),
        )
        cursor.execute(stmt)
        result = cursor.fetchone()

    rowcount, = result
    return rowcount

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/auto_theft",methods=["POST","GET"])
def page_1():
   
   if request.method == "POST":
        
        state=request.form["nm"]
        user_index=request.form["nd"]
        user_year=request.form["np"]
        user_query_opt=request.form["btn"]
        user_cases=request.form["nw"]
        user_zone=request.form["ns"]
        print("POST request success")
        if user_query_opt=="Insertion":
            
            insert_demo_table=f"""
    insert into autotheft_data values({user_index},"{state}",{user_year},"{user_zone}",{user_cases})
        """
            execute_query(connection,insert_demo_table)

        if user_query_opt=="Deletion":
            
            deletion_demo_table=f"""
        delete from autotheft_data where index_at={user_index}
        """
            execute_query(connection,deletion_demo_table)

            if user_query_opt=="Updation":
               
            
              insert_demo_table=f"""
              update autotheft_data set state="{state}" where index_at={user_index}; 
              """
            execute_query(connection,insert_demo_table)
        
        return render_template("auto_theft.html")
   else:
      return render_template("auto_theft.html")
   
     

@app.route("/murders",methods=["POST","GET"])
def page_2():
   if request.method == "POST":
        
        user_state=request.form["nm"]
        user_zone=request.form["nd"]
        user_year=request.form["np"]
        user_query_opt=request.form["btn"]
        user_victims=request.form["ns"]
        print("POST request success")
        if user_query_opt=="Insertion":
            
            insert_demo_table=f"""
    insert into murders_data values("{user_state}","{user_zone}",{user_year},{user_victims})
        """
            execute_query(connection,insert_demo_table)

        if user_query_opt=="Deletion":
            
            deletion_demo_table=f"""
        delete from murders_data where state="{user_state}"
        """
            execute_query(connection,deletion_demo_table)
        
        return render_template("murders.html")
   else:
      return render_template("murders.html")


@app.route("/cyber_security",methods=["POST","GET"])
def page_3():
   return render_template("cyber_security.html")


@app.route("/kidnapping",methods=["POST","GET"])
def page_4():
   if request.method == "POST":
        
        user_state=request.form["nm"]
        user_index=request.form["nd"]
        user_year=request.form["np"]
        user_query_opt=request.form["btn"]
        user_zone=request.form["ns"]
        user_victims=request.form["nw"]
        print("POST request success")
        if user_query_opt=="Insertion":
            
            insert_demo_table=f"""
    insert into kidnapping_data values({user_index},"{user_state}",{user_year},"{user_zone}",{user_victims})
        """
            execute_query(connection,insert_demo_table)

        if user_query_opt=="Deletion":
            
            deletion_demo_table=f"""
        delete from kidnapping_data where index_k={user_index}
        """
            execute_query(connection,deletion_demo_table)
            if user_query_opt=="Updation":
               
            
              insert_demo_table=f"""
              update autotheft_data set state="{user_state}" where index_at={user_index}; 
              """
        
        return render_template("kidnapping.html")
   else:
      return render_template("kidnapping.html")

@app.route("/rape",methods=["POST","GET"])
def page_5():
   if request.method == "POST":
        
        user_state=request.form["nm"]
        user_index=request.form["nw"]
        user_year=request.form["np"]
        user_query_opt=request.form["btn"]
        user_zone=request.form["nd"]
        user_victims=request.form["ns"]
        print("POST request success")
        if user_query_opt=="Insertion":
            
            insert_demo_table=f"""
    insert into rape_victims_data values({user_index},"{user_state}",{user_year},"{user_zone}",{user_victims})
        """
            execute_query(connection,insert_demo_table)

        if user_query_opt=="Deletion":
            
            deletion_demo_table=f"""
        delete from rape_victims_data where index_r={user_index}
        """
            execute_query(connection,deletion_demo_table)
            if user_query_opt=="Updation":
               
            
              insert_demo_table=f"""
              update autotheft_data set state="{user_state}" where index_at={user_index}; 
              """
        
        return render_template("rape.html")
   else:
      return render_template("rape.html")

   

@app.route("/login",methods=["POST","GET"])
def login():
      return render_template("login.html")
@app.route("/<usr>")
def user(usr):
  return f"<h1>{usr}</h1>"

if __name__=="__main__":
    app.run(debug=True)