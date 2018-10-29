import MySQLdb 

def connection():
    conn = MySQLdb.connect(host="filedrive.cqutf1eg2abx.us-west-2.rds.amazonaws.com", user = "amrutha", passwd = "Amrutha1", db = "filedrivedb")
    c = conn.cursor()
    return c, conn
