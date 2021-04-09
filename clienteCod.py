import sys,os
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
import clienteTela
from datetime import datetime
from PIL import Image
from clienteTela import Ui_Form
from testebancosqlite import executarSelect as sel
from testebancosqlite import conexaoBanco as conexao
from sqlite3 import Error
defaultImg ="cliente.png"
# testando git hub
class ClienteLogin(qtw.QWidget, Ui_Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Your code will go here
        #tabwidget.setCurrentWidget(tabwidget.findChild(QWidget, tabname))
        #self.ui = Ui_Form()  ### Para não usar o .ui tem que declarar o 'Ui_Form' no parametro da classe
        #self.ui.setupUi(self)       self.setupUi(self)
        self.setupUi(self)
        self.primeiro.clicked.connect(self.primeiroItem)
        self.anterior.clicked.connect(self.anteriorItem)
        self.proximo.clicked.connect(self.proximoItem)
        self.ultimo.clicked.connect(self.ultimoItem)
        self.salvar.clicked.connect(self.addCliente)
        self.pushButton.clicked.connect(self.uploadImg)
        self.novo.clicked.connect(self.newCliente)
        self.editar.clicked.connect(self.habilitarCampos)
        self.estado.currentIndexChanged.connect(self.getCidades)
        self.voltarTela.clicked.connect(self.fecharTela)
        # Your code ends here
        self.show()


    def uploadImg(self): # Abre os arquivos para procurar a imagem e a salva na pasta
        global defaultImg
        size = (256, 256)
        self.filename, ok = QFileDialog.getOpenFileName(self, "Upload Image", "", "Image Files (*.jpg *.png)")
        if ok:
            print(self.filename)
            defaultImg = os.path.basename(self.filename)
            print(defaultImg)
            img = Image.open(self.filename)
            img = img.resize(size)
            img.save("img/{0}".format(defaultImg))

    def teste(self):
        name = self.nome.text()
        dtCad = self.dtCad.text()
        print(dtCad)

    def fecharTela(self):
        self.close()

    def getEstados(self): ########## Adiciona estados no Combo box ###############
        try:
            con = conexao()
            c = con.cursor()
            c.execute("SELECT est_nome FROM estados")
            con.commit()
            resultado = c.fetchall()
            c.close()
            flag = "0"
        except Error as e:
            flag = "1"
            print(e)
            QMessageBox.information(self, "Info", "Erro ao indexar Estados")
        if(flag == "0"):
            self.cidade.clear()
            self.estado.addItem("Escolha um Estado!!!")
            pos_i = 0  # variável provisória de índice
            for i in range(len(resultado)):  #passar por toda lista
                self.estado.addItem(resultado[i][0])
                pos_i = i  # guardamos o índice i
            return (pos_i)  # e retornamos o índice

    def getCidades(self): ############# Adiciona cidades ao combo box ###############
        estadoid = self.estado.currentIndex()
        estadoid = int(estadoid)
        try:
            con = conexao()
            c = con.cursor()
            c.execute("SELECT cid_nome FROM cidades where est_id = (?)", (estadoid,))
            con.commit()
            resultado = c.fetchall()
            c.close()
            flag = "0"
        except Error as e:
            flag = "1"
            print(e)
            QMessageBox.information(self, "Info", "Erro ao indexar Cidades")

        if (flag == "0"):
            self.cidade.clear()
            self.cidade.addItem("Escolha uma Cidade!!!")
            if(estadoid > 1):
                pos_i = 0  # variável provisória de índice
                for i in range(len(resultado)):  # passar por toda lista
                    self.cidade.addItem(resultado[i][0])
                    pos_i = i  # guardamos o índice i
                return (pos_i)  # e retornamos o índice

    def addCliente(self): ############# Adiciona o cliente no Banco de Dados ##################
        global defaultImg  # Define uma variavel para a imagem do cliente

        ##### Dados Pessoais #############
        dtCad = self.dtCad.text()
        name = self.nome.text()
        nameFan = self.nomeFan.text()
        dtNasc = self.dtNasc.text()
        rg = self.rg.text()
        dtemiss = self.dateEdit.text()
        cpf = self.cpf.text()
        sexo = self.sexo.currentText()
        obser = self.obs.toPlainText()
        cliTel = self.telefone.text()
        cliCel = self.celular_2.text()
        empresa = self.empresa.text()
        empTel = self.telEmp.text()
        profissao = self.profissao.text()
        salario = self.salario.text()
        estCivil = self.estCivil.text()
        outR = self.outrasRendas.text()

        ###### Endereço ########################
        end = self.end.text()
        numCasa = self.numero.text()
        comp = self.complemento.text()
        cep = self.cep.text()
        bairro = self.bairro.text()
        cidNome = self.cidade.currentText()
        estId = self.estado.currentIndex()

        ###### Referência/ Limite ##############
        ref1 = self.ref1.text()
        tel1 = self.tel1.text()
        ref2 = self.ref2.text()
        tel2 = self.tel2.text()
        limite = self.limite.text()

        if (estId and cidNome != ""):  ############ Pegando o ID da cidade ###########
            try:
                con = conexao()
                c = con.cursor()
                c.execute(" SELECT cid_id FROM cidades where est_id= (?) AND cid_nome like (?)", (estId, cidNome,))
                con.commit()
                resultado = c.fetchall()
                cidId = resultado[0][0]
                print(cidId)
                c.close()
                flag = "0"
            except Error as e:
                flag = "1"
                print(e)
        else:
            QMessageBox.information(self, "Info", "Estado ou Cidade não Preenchidos")
        if (flag == "0"):
            if ((end != "")):  ########### Inserindo Endereço ##################
                try:
                    con = conexao()
                    c = con.cursor()
                    c.execute(
                        """INSERT INTO endereco (end_nome, end_num, end_comp, end_cep, end_bairro, cid_id) 
                           VALUES (?,?,?,?,?,?)""",
                        (end, numCasa, comp, cep, bairro, cidId))
                    con.commit()
                    c.close()
                    flag = "0"
                except Error as e:
                    flag = "1"
                    print(e)
            else:
                QMessageBox.information(self, "Info", "Preencher Campos Obrigatórios")
            if (flag == "0"):
                con = conexao()
                c = con.cursor()
                c.execute(" SELECT * FROM endereco order by end_id DESC")
                con.commit()
                resultado = c.fetchall()
                endId = resultado[0][0]
                c.close()

                if (name and cpf != ""):  ########### Inserindo Cliente ##################
                    try:
                        con = conexao()
                        c = con.cursor()
                        c.execute(
                            """INSERT INTO clientes (cli_nome, cli_nomefan, cli_dtnasc, cli_rg, cli_cpf, cli_sexo, cli_obs, cli_emprego, cli_empresa, cli_empresacel, cli_salario, cli_estadocivil, cli_outrasrendas, cli_cel, cli_tel, end_id, cli_dtemiss, cli_dtcad, cli_ref1, cli_ref1cel, cli_ref2, cli_ref2cel, cli_limite) 
                               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                            (name, nameFan, dtNasc, rg, cpf, sexo, obser, profissao, empresa, empTel, salario, estCivil,
                             outR, cliCel, cliTel, endId, dtemiss, dtCad, ref1, tel1, ref2, tel2, limite))
                        con.commit()
                        c.close()
                        QMessageBox.information(self, "Info", "Cliente Adicionado com Sucesso")
                    except Error as e:
                        print(e)
                        QMessageBox.information(self, "Info", "Erro ao adicionar Cliente")
                else:
                    QMessageBox.information(self, "Info", "Preencher Campos Obrigatórios")
            else:
                QMessageBox.information(self, "Info", "Erro ao Adicionar Endereço")
        else:
            QMessageBox.information(self, "Info", "Erro ao adicionar Cliente")

    def editCliente(self):
        try:
            codigo = self.codigo.text()
            con = conexao()
            c = con.cursor()
            c.execute(" SELECT * FROM clientes where cli_id = (?)", (codigo,))
            con.commit()
            resultado = c.fetchall()
            c.close()
            print(resultado)
            flag= "0"
        except Error as e:
            flag = "1"
            print(e)

        if (flag == "0"):
            ############## Recebendo Valores ######################
            dtCad = resultado[0][25]
            name = resultado[0][1]
            nameFan = resultado[0][2]
            dtNasc = resultado[0][3]
            rg = resultado[0][4]
            dtemiss = resultado[0][5]
            cpf = resultado[0][6]
            sexo = resultado[0][7]
            obser = resultado[0][8]
            endId = resultado[0][17]
            cliTel = resultado[0][18]
            cliCel = resultado[0][19]
            empresa = resultado[0][20]
            empTel = resultado[0][21]
            profissao = resultado[0][9]
            salario = resultado[0][22]
            estCivil = resultado[0][23]
            outR = resultado[0][24]

            ###### Referência/ Limite ##############
            ref1 = resultado[0][10]
            tel1 = resultado[0][11]
            ref2 = resultado[0][12]
            tel2 = resultado[0][13]
            limite = resultado[0][26]

        if (flag == "0"):
            try:
                con = conexao()
                c = con.cursor()
                c.execute(" SELECT * FROM endereco where end_id = (?)", (endId,))
                con.commit()
                resultado = c.fetchall()
                c.close()
            except Error as e:
                flag = "1"
                print(e)

        if (flag == "0"):
            ###### Endereço ########################
            end = resultado[0][1]
            numCasa = resultado[0][2]
            comp = resultado[0][3]
            cep = resultado[0][4]
            bairro = resultado[0][5]
            cidId = resultado[0][6]

        if (flag == "0"):
            try:
                con = conexao()
                c = con.cursor()
                c.execute(" SELECT * FROM cidades where cid_id= (?)", (cidId,))
                con.commit()
                resultado = c.fetchall()
                cidNome = resultado[0][1]
                c.close()
            except Error as e:
                flag = "1"
                print(e)
        estId = resultado[0][2]
        ############# Inserindo valores nos Campos ############

        if (dtCad != ""): ########### string to date ##################
            data = datetime.strptime(dtCad, '%d/%m/%Y')
            self.dtCad.setDate(data)
        if (dtNasc != ""): ########### string to date ##################
            dtNasc = datetime.strptime(dtNasc, '%d/%m/%Y')
            self.dtNasc.setDate(dtNasc)
        if (dtemiss != ""): ########### string to date ##################
            dtemiss = datetime.strptime(dtemiss, '%d/%m/%Y')
            self.dateEdit.setDate(dtemiss)
        if (sexo != ""):  ########### Setando o index do sexo ##################
            if (sexo == "Masculino"):
                sexo = "0"
            else:
                sexo = "1"
            self.sexo.setCurrentIndex(int(sexo))

        self.nome.setText(str(name))
        self.nomeFan.setText(str(nameFan))
        self.rg.setText(str(rg))
        self.cpf.setText(str(cpf))
        self.obs.setText(obser)
        self.telefone.setText(str(cliTel))
        self.celular_2.setText(str(cliCel))
        self.empresa.setText(str(empresa))
        self.telEmp.setText(str(empTel))
        self.profissao.setText(str(profissao))
        self.salario.setText(str(salario))
        self.estCivil.setText(str(estCivil))
        self.outrasRendas.setText(str(outR))

        ###### Endereço ########################
        self.end.setText(str(end))
        self.numero.setText(str(numCasa))
        self.complemento.setText(str(comp))
        self.cep.setText(str(cep))
        self.bairro.setText(str(bairro))
        #cidNome = self.cidade.currentText()
        #estId = self.estado.currentIndex()

        ###### Referência/ Limite ##############
        self.ref1.setText(str(ref1))
        self.tel1.setText(str(tel1))
        self.ref2.setText(str(ref2))
        self.tel2.setText(str(tel2))
        self.limite.setText(str(limite))
        self.getEstados()
        self.estado.setCurrentIndex(int(estId))

        if (flag == "0"): ############ colocando as cidades numa lista #############
            try:
                con = conexao()
                c = con.cursor()
                c.execute("SELECT cid_nome FROM cidades where est_id = (?)", (estId,))
                con.commit()
                cidadesbusca = c.fetchall()
                print(cidadesbusca)
                c.close()
            except Error as e:
                flag = "1"
                print(e)
                QMessageBox.information(self, "Info", "Erro ao indexar Cidades")

        if (flag == "0"): ############ pegando o numero da cidade na lista #############
            pos_i = 0  # variável provisória de índice
            pos_j = 0  # idem

            for i in range(len(cidadesbusca)):  # procurar em todas as listas internas
                for j in range(i):  # procurar em todos os elementos nessa lista
                    if cidNome in cidadesbusca[i][j]:  # se encontrarmos elemento
                        cidNum = i
                        break  # saímos do loop interno
                    break  # e do externo
        if (flag == "0"):
            self.cidade.setCurrentIndex(int(cidNum)+1)

        ##################### Desabilitando os Campos para Edição #####################
        self.dtCad.setEnabled(False)
        self.dtNasc.setEnabled(False)
        self.dateEdit.setEnabled(False)
        self.sexo.setEnabled(False)
        self.nome.setEnabled(False)
        self.nomeFan.setEnabled(False)
        self.rg.setEnabled(False)
        self.cpf.setEnabled(False)
        self.obs.setEnabled(False)
        self.telefone.setEnabled(False)
        self.celular_2.setEnabled(False)
        self.empresa.setEnabled(False)
        self.telEmp.setEnabled(False)
        self.profissao.setEnabled(False)
        self.salario.setEnabled(False)
        self.estCivil.setEnabled(False)
        self.outrasRendas.setEnabled(False)

        ###### Endereço ########################
        self.end.setEnabled(False)
        self.numero.setEnabled(False)
        self.complemento.setEnabled(False)
        self.cep.setEnabled(False)
        self.bairro.setEnabled(False)

        ###### Referência/ Limite ##############
        self.ref1.setEnabled(False)
        self.tel1.setEnabled(False)
        self.ref2.setEnabled(False)
        self.tel2.setEnabled(False)
        self.limite.setEnabled(False)
        self.estado.setEnabled(False)
        self.cidade.setEnabled(False)

    def habilitarCampos(self):
        ##################### Habilitando os Campos para Edição #####################
        self.dtCad.setEnabled(True)
        self.dtNasc.setEnabled(True)
        self.dateEdit.setEnabled(True)
        self.sexo.setEnabled(True)
        self.nome.setEnabled(True)
        self.nomeFan.setEnabled(True)
        self.rg.setEnabled(True)
        self.cpf.setEnabled(True)
        self.obs.setEnabled(True)
        self.telefone.setEnabled(True)
        self.celular_2.setEnabled(True)
        self.empresa.setEnabled(True)
        self.telEmp.setEnabled(True)
        self.profissao.setEnabled(True)
        self.salario.setEnabled(True)
        self.estCivil.setEnabled(True)
        self.outrasRendas.setEnabled(True)

        ###### Endereço ########################
        self.end.setEnabled(True)
        self.numero.setEnabled(True)
        self.complemento.setEnabled(True)
        self.cep.setEnabled(True)
        self.bairro.setEnabled(True)

        ###### Referência/ Limite ##############
        self.ref1.setEnabled(True)
        self.tel1.setEnabled(True)
        self.ref2.setEnabled(True)
        self.tel2.setEnabled(True)
        self.limite.setEnabled(True)
        self.estado.setEnabled(True)
        self.cidade.setEnabled(True)

    def newCliente(self):
        data = datetime.today()
        self.dtCad.setDate(data)
        #self.dtNasc.setDate(dtNasc)
        #self.dateEdit.setDate(dtemiss)
        self.sexo.setCurrentIndex(2)
        self.nome.setText("")
        self.nomeFan.setText("")
        self.rg.setText("")
        self.cpf.setText("")
        self.obs.setText("")
        self.telefone.setText("")
        self.celular_2.setText("")
        self.empresa.setText("")
        self.telEmp.setText("")
        self.profissao.setText("")
        self.salario.setText("")
        self.estCivil.setText("")
        self.outrasRendas.setText("")

        ###### Endereço ########################
        self.end.setText("")
        self.numero.setText("")
        self.complemento.setText("")
        self.cep.setText("")
        self.bairro.setText("")

        ###### Referência/ Limite ##############
        self.ref1.setText("")
        self.tel1.setText("")
        self.ref2.setText("")
        self.tel2.setText("")
        self.limite.setText("")
        self.getEstados()
        self.habilitarCampos()

    def ultimoItem(self):
        try:
            con = conexao()
            c = con.cursor()
            c.execute(" SELECT * FROM clientes order by cli_id DESC")
            con.commit()
            resultado = c.fetchall()
            c.close()
            self.codigo.setText(str(resultado[0][0]))
            self.editCliente()
        except Exception as e:
            print(e)
        pass

    def primeiroItem(self):
        try:
            con = conexao()
            c = con.cursor()
            c.execute(" SELECT * FROM clientes")
            con.commit()
            resultado = c.fetchone()
            c.close()
            self.codigo.setText(str(resultado[0]))
            self.editCliente()
        except Exception as e:
            print(e)
        pass

    def proximoItem(self):
        try:
            con = conexao()
            c = con.cursor()
            c.execute(" SELECT * FROM clientes order by cli_id DESC")
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
            self.editCliente()
        else:
            QMessageBox.information(self, "Info", "Cliente Não Localizado")



    def anteriorItem(self):
        resultado = self.codigo.text()
        if (resultado == ""):
            resultado = 1
        resultado = int(resultado)
        if (resultado > 1):
            resultado = resultado - 1
            self.codigo.setText(str(resultado))
            self.editCliente()
        else:
            QMessageBox.information(self, "Info", "Cliente Não Localizado")

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = ClienteLogin()
    sys.exit(app.exec_())
