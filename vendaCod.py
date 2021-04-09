from PyQt5.QtWidgets import *
import sys,os
from PyQt5 import QtWidgets as qtw
from vendasTela import Ui_Form
from testebancosqlite import executarSelect as sel
from testebancosqlite import conexaoBanco as conexao
from sqlite3 import Error
import clienteCod
import produtoCod


class Venda(qtw.QWidget, Ui_Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.tableWidget.setColumnWidth(0,150) #### Setar o tamanho da coluna
        self.prodbuscar.clicked.connect(self.addProd)
        self.voltarTela.clicked.connect(self.fecharTela)
        #self.cadcliente.clicked.connect(self.cadcliente)
        self.show()

    #def cadcliente(self):
        #self.newclientes = clienteCod.ClienteLogin()

    def fecharTela(self):
        self.close()

    def addProd(self):
        rowcount = 0
        codigo = self.prodcod.text()
        qtde = int(self.prodqtde.text())
        try:
            con = conexao()
            c = con.cursor()
            c.execute(" SELECT prod_cod, prod_desc, prod_preco FROM produtos where prod_id = (?)", (codigo,))
            con.commit()
            resultado = c.fetchall()
            c.close()
            print(resultado[0])
        except Error as e:
            print(e)
            return e
        pass
        preco = float(resultado[0][2])
        total = preco * qtde
        self.tableWidget.setRowCount(len(resultado))
        for row in range(len(resultado)):
            self.tableWidget.setItem(0, 0, QTableWidgetItem(resultado[0][0]))
            self.tableWidget.setItem(0, 1, QTableWidgetItem(resultado[0][1]))
            self.tableWidget.setItem(0, 2, QTableWidgetItem(str(qtde)))
            self.tableWidget.setItem(0, 3, QTableWidgetItem(str(resultado[0][2])))
            self.tableWidget.setItem(0, 4, QTableWidgetItem(str(total)))



if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = Venda()
    sys.exit(app.exec_())
