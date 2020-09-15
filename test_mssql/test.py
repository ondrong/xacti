import pypyodbc

ip_address="172.17.145.17"
user="user_postgresql"
password="Postgresql"
port="1433"
database="HRD"

#---- connection and create cursor
cs='DRIVER={ODBC Driver 17 for SQL Server};PORT='+port+';SERVER='+ip_address+';DATABASE='+database+';UID='+user+';PWD='+password
cnn = pypyodbc.connect(cs, unicode_results=True)
cur = cnn.cursor()

#---- query database
sql = "select IDNO,CHECKTIME_IN,CHECKTIME_OUT from ANVIZ_ABS_FOR_ODOO where CHECKTIME_IN IS NOT NULL"
cur.execute(sql)
records = cur.fetchall()

#---- process results
sql = """insert into hr_attendance (employee_id, check_in, check_out) VALUES """
values= []
for rec in records:
    IDNO = rec[0]
    CHECKTIME_IN=rec[1]
    CHECKTIME_OUT=rec[2]
    values.append (str(("(select id from hr_employee where x_idno=%s)" % IDNO, CHECKTIME_IN.strftime("%Y-%m-%d %H:%I:%S"), CHECKTIME_OUT.strftime("%Y-%m-%d %H:%I:%S"))) )

sql = sql + ",".join(values)

print(sql)
