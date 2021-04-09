import sys,os
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from datetime import datetime
import alterarEstoqueCod
from estoqueTela import *
from produtoTela import Ui_Form
from testebancosqlite import executarSelect as sel
from testebancosqlite import conexaoBanco as conexao
from sqlite3 import Error
from tkinter import *
flag = "0"

class ProdCad(qtw.QWidget, Ui_Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Your code will go here
        #tabwidget.setCurrentWidget(tabwidget.findChild(QWidget, tabname))
        #self.ui = Ui_Form()  ### Para não usar o .ui tem que declarar o 'Ui_Form' no parametro da classe
        #self.ui.setupUi(self)       self.setupUi(self)
        self.setupUi(self)
        global flag
        flag = "0"
        #self.primeiro.clicked.connect(self.)
        self.primeiro.clicked.connect(self.primeiroItem)
        self.anterior.clicked.connect(self.anteriorItem)
        self.proximo.clicked.connect(self.proximoItem)
        self.ultimo.clicked.connect(self.ultimoItem)
        self.editar.clicked.connect(self.editProduto)
        self.novo.clicked.connect(self.newProd)
        self.imprimir.clicked.connect(self.addProd)
        self.voltarTela.clicked.connect(self.fecharTela)
        #self.estoque.clicked.connect(self.altestoque)
        #self.codigo.bind("<Return>", self.editProduto)
        # Your code ends here
        self.show()

    def teste(self):
        sq = " SELECT * FROM produtos"
        a = sel(sq)
        print(a)

    def fecharTela(self):
        self.close()

    def addProd(self): #Adiciona o produto no Banco de Dados
            ##### Pegar Campos #############
            descricao = self.descricao.text()
            codBarras = self.codBarras.text()
            undMedida = self.undMedida.currentText()
            classe = self.classe.currentText()
            precocusto = self.precocusto.text()
            precofinal = self.precofinal.text()
            lucro = self.lucro.text()
            if (precofinal and precocusto != ""):
                lucro = (float(precofinal) / float(precocusto) - 1) * 100
                print (lucro)
            setor = self.setor.currentText()
            dtCad = self.dtCad.text()

            if (descricao != ""):
                try:
                    con = conexao()
                    c = con.cursor()
                    c.execute("INSERT INTO produtos (prod_desc, prod_cod, prod_med, prod_classe, prod_custo, prod_preco, prod_lucro, prod_setor, prod_dtcad) VALUES (?,?,?,?,?,?,?,?,?)",
                              (descricao, codBarras, undMedida, classe, precocusto, precofinal, lucro, setor, dtCad))
                    con.commit()
                    c.close()
                    QMessageBox.information(self, "Info", "Produto Adicionado com Sucesso")
                except Error as e:
                    print(e)
            else:
                QMessageBox.information(self, "Info", "Preencher Campos Obrigatórios") 

    def editProduto(self):
        try:
            codigo = self.codigo.text()
            con = conexao()
            c = con.cursor()
            c.execute(" SELECT * FROM produtos where prod_id = (?)", (codigo,))
            con.commit()
            resultado = c.fetchall()
            c.close()

            ############## Recebendo Valores ######################
            undMedida = resultado[0][3]
            classe = resultado[0][4]
            setor = resultado[0][7]
            if (undMedida != ""):  ########### Setando o valor da Medida
                if (undMedida == "Unidade"):
                    undMedida = "0"
                elif (undMedida == "Caixa"):
                    undMedida = "1"
                elif (undMedida == "Peça"):
                    undMedida = "2"
                elif (undMedida == "Conjunto"):
                    undMedida = "3"
                else:
                    undMedida = "0"
                self.undMedida.setCurrentIndex(int(undMedida))

            if (classe != ""):  ########### Setando o valor da Classe
                if (classe == "Diverso"):
                    classe = "0"
                elif (classe == "Roupa"):
                    classe = "1"
                elif (classe == "Calçado"):
                    classe = "2"
                else:
                    classe = "0"
                self.classe.setCurrentIndex(int(classe))

            if (setor != ""):  ########### Setando o valor do setor
                if (setor == "Masculino"):
                    setor = "0"
                elif (setor == "Feminino"):
                    setor = "1"
                elif (setor == "Infantil"):
                    setor = "2"
                elif (setor == "Calçado"):
                    setor = "3"
                else:
                    setor = "0"
                self.setor.setCurrentIndex(int(setor))

            dtCad = resultado[0][8]
            print(dtCad)
            if (dtCad != ""):
                data = datetime.strptime(dtCad, '%d/%m/%Y')
            else:
                data = datetime.today()

            ############# Inserindo valores nos Campos ############
            self.descricao.setText(str(resultado[0][1]))
            self.codBarras.setText(str(resultado[0][2]))
            self.precocusto.setText(str(resultado[0][5]))
            self.precofinal.setText(str(resultado[0][6]))
            self.dtCad.setDate(data)
            self.lucro.setText(str(resultado[0][9]))
        except Error as e:
            print(e)
            return e
        pass

        ##################### Desabilitando os Campos para Edição #####################
        self.undMedida.setEnabled(False)
        self.classe.setEnabled(False)
        self.setor.setEnabled(False)
        self.descricao.setEnabled(False)
        self.codBarras.setEnabled(False)
        self.precocusto.setEnabled(False)
        self.precofinal.setEnabled(False)
        self.dtCad.setEnabled(False)
        self.lucro.setEnabled(False)

    def habilitarCampos(self):
        ##################### Habilitando os Campos para Edição #####################
        self.undMedida.setEnabled(True)
        self.classe.setEnabled(True)
        self.setor.setEnabled(True)
        self.descricao.setEnabled(True)
        self.codBarras.setEnabled(True)
        self.precocusto.setEnabled(True)
        self.precofinal.setEnabled(True)
        self.dtCad.setEnabled(True)
        self.lucro.setEnabled(True)

    def newProd(self):
        data = datetime.today()
        self.dtCad.setDate(data)
        self.descricao.setText("")
        self.codBarras.setText("")
        self.precocusto.setText("")
        self.precofinal.setText("")
        self.lucro.setText("")
        self.codigo.setText("")
        self.habilitarCampos()


        """def altestoque(self):
        global flag
        print(flag)
        codProd = self.codigo.text()
        print(codProd)
        if(flag =="0"):
            flag = "1"
            self.newproduto = alterarEstoqueCod.TelaEstoque()
        return codProd"""


    def ultimoItem(self):
        try:
            con = conexao()
            c = con.cursor()
            c.execute(" SELECT * FROM produtos order by prod_id DESC")
            con.commit()
            resultado = c.fetchall()
            c.close()
            self.codigo.setText(str(resultado[0][0]))
            self.editProduto()
        except Exception as e:
            print(e)
        pass

    def primeiroItem(self):
        try:
            con = conexao()
            c = con.cursor()
            c.execute(" SELECT * FROM produtos")
            con.commit()
            resultado = c.fetchone()
            c.close()
            self.codigo.setText(str(resultado[0]))
            self.editProduto()
        except Exception as e:
            print(e)
        pass

    def proximoItem(self):
        try:
            con = conexao()
            c = con.cursor()
            c.execute(" SELECT * FROM produtos order by prod_id DESC")
            con.commit()
            ultimo = c.fetchall()
            c.close()
            ultimo = ultimo[0][0]
            ultimo = int(ultimo)
        except Exception as e:
            print(e)
        pass
        resultado = self.codigo.text()
        if (resultado == ""):
            resultado = 0
        resultado = int(resultado)
        if(resultado < ultimo):
            resultado = int(resultado) + 1
            self.codigo.setText(str(resultado))
            self.editProduto()
        else:
            QMessageBox.information(self, "Info", "Produto Não Localizado")



    def anteriorItem(self):
        resultado = self.codigo.text()
        if (resultado == ""):
            resultado = 1
        resultado = int(resultado)
        if (resultado > 1):
            resultado = resultado - 1
            self.codigo.setText(str(resultado))
            self.editProduto()
        else:
            QMessageBox.information(self, "Info", "Produto Não Localizado")

"""
class TelaEstoque(qtw.QWidget, Ui_Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_AlterarEstoque
        self.ui.setupUi(self)
    def mudaJanela(self):
        self.tela = TelaEstoque()
        self.tela.show()
"""

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = ProdCad()
    sys.exit(app.exec_())
