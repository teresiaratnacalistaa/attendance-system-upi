import mysql.connector
from configparser import ConfigParser
# from torch import _fake_quantize_per_tensor_affine_cachemask_tensor_qparams
cnx: mysql.connector.connect(host='localhost', db='data_sistemskripsi', user='root', password='') = None

config = ConfigParser()
def login (userName: str, password: str) -> bool:
    if (userName is None):
        return False
    args = [userName, password, 0]
    result_args = executeSQLQuery ("CheckUser", args)
    return (result_args[2] == 1)
    # returns => ('admin', 'admin', 1)
    # if (result_args[2] == 1):
    #     return True
    # else:
    #     return False;

def executeSQLQuery(query, args):
    global cnx
    if (cnx == None):
        # config = ConfigParser()
        config.read("config.ini")
        _host = config.get('MySQL', 'host')
        _post = config.get('MySQL', 'port')
        _database = config.get('MySQL', 'database')
        _user = config.get('MySQL', 'user')
        _password = config.get('MySQL', 'password')
        cnx = mysql.connector.connect(host=_host, database=_database,
                                    user=_user, passwd=_password)
    
    with cnx.cursor() as cur:
        return cur.callproc(query, args)