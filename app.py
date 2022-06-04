from flask import Flask, request, render_template
import psycopg2

app = Flask(__name__)

def connect():
    """ Connect to the database.
    :return connection: object - connection to the database
    :return cursor: object - cursor to write queries
    """
    # Establish a connection.
    connection = psycopg2.connect(
        host="postgres.biocentre.nl",
        database="bio_jaar_2_pg_5",
        user="BI2_PG5",
        password="blaat1234",
        port="5900")

    # Open a cursor.
    cursor = connection.cursor()

    # Return the connection and cursor.
    return connection, cursor


def disconnect(connection, cursor):
    """ Disconnect from the database.
    :param connection: object - connection to the database
    :param cursor: object - cursor to write queries
    """
    # Close the cursor and disconnect from the database.
    cursor.close()
    connection.close()


@app.route('/', methods=['GET', 'POST'])
def home_page():

    # Connect to the database.
    connection, cursor = connect()

    cursor.execute("select distinct patient_id from patient")
    data = cursor.fetchall()
    patient = []
    for i in data:
        i = i[0].replace('_Zscore', '')
        patient.append(i)

    if request.method == "POST":
        op1 = request.form.get('zScoreMin').replace(",", ".")
        op2 = request.form.get('zScoreMax').replace(",", ".")
        cursor.execute(f'select * from patient where zscore >= {op1} and zscore <= {op2}')
        data = cursor.fetchall()
        zscore = []
        for i in data:
            zscore.append(i)


    # Disconnect from the database.
    disconnect(connection, cursor)
    return render_template("home.html", patients=patient)

@app.route('/database.html', methods=['GET', 'POST'])
def database_page():
    return render_template("database.html")


if __name__ == '__main__':
    app.run()
