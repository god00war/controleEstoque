import sys,os
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets as qtw
from estoqueTela import Ui_AlterarEstoque
from testebancosqlite import conexaoBanco as conexao
#from produtoCod import altestoque as pd

class TelaEstoque(qtw.QWidget, Ui_AlterarEstoque):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.alterar.clicked.connect(self.altEstoque)
        self.show()

    """altEstoque(self):
        id = pd()
        quant = self.codigo.text()
        if (id !=""):
            try:
                con = conexao()
                c = con.cursor()
                c.execute(" UPDATE produtos SET prod_est = (?) WHERE prod_id = (?)", (quant,id))
                con.commit()
                c.close()
            except Exception as e:
                print(e)
            pass
        else:
            QMessageBox.information(self, "Info", "Preencha o Códifo do Produto")
"""
if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = TelaEstoque()
    sys.exit(app.exec_())
