
def fetch_db_cred():
    db_name = 'splitwise'
    port= '5432'
    host = 'localhost'
    password='Qwerty%40111'
    return "postgresql://postgres:" + password + "@" + host + ":" + str(port) + "/" + db_name