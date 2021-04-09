import fdb


class Conexao(object):
    con = fdb.connect(
        host="localhost",database="C:/Users/God War/Documents/TCC/Banco de dados/gino14.FDB", user='sysdba', password='masterkey'
    )

    cur = con.cursor()
    cur.execute(object)

    print(cur.fetchall())

