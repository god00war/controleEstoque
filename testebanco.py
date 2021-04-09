import fdb
import locale

name ='alisson1'
end ='dlç1'
cod1= int(1)
cod2= int(1)
#outRen = locale.format_string(format, outR, grouping=False, monetary=True)
#outRen = locale.currency(outR, symbol=False) #Troca o float para o padrao local

try:
    con = fdb.connect(
        host="localhost", database="C:/Users/God War/Documents/TCC/Banco de dados/gino14.FDB",
        user='sysdba',
        password='masterkey'
    )

    cur = con.cursor()
    cur.execute("SELECT *FROM t007_produtos ORDER BY T007_NR_CODIGO DESC ")
    ultimoItem = cur.fetchall()[0][0]
    #cur.execute("select *from t007_produtos where T007_NR_CODIGO ="+str(ultimoItem[0]))
    #teste = cur.fetchall()[0]
    print(ultimoItem)
    con.commit()
    con.close
except Exception as e:
    print(e)
pass

con.commit()