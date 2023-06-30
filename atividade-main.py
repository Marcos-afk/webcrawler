import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox

from Ui_atividade import Ui_MainWindow

from functions import *


def message_box(title, message):
    msg_box = QMessageBox()
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setStyleSheet('''
                    QMessageBox {
                        background-color: rgb(61, 61, 61);
                        color: rgb(255, 255, 255);
                    }
                    QMessageBox QLabel {
                        color: rgb(255, 255, 255);
                    }
                ''')
    msg_box.exec_()


def open_file():
    urls = []
    with open("websites.txt", "r") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            urls.append(lines[i].strip())
    return urls


def search_documents():
    urls = open_file()
    print("Entrou aqui: ", urls)
    documentos = []

    for url in urls:
        try:
            response = requests.get(url)
            # Se o site aceitar o pedido:
            if response.status_code == 200:
                # Cria o nome do banco de dados a partir da URL atual
                name = urlparse(url).netloc
                new_name = name.replace('.', '-')

                # Adquire todos os dados
                html = get_html(response)
                head_tag = get_head(response)
                body_tag = get_body(response)
                meta_tags = get_meta(response)
                internos, externos = get_links(url)
                termos = get_terms(response)
                vocabulario = vocabulary(termos)

                # Cria dados para matriz
                for termo in vocabulario:
                    documentos.append(termo)

                # Insere todos os dados no banco
                insert_data(new_name, "Código HTML", str(html))
                insert_data(new_name, "Head tag", head_tag)
                insert_data(new_name, "Body tag", body_tag)
                insert_data(new_name, "Meta tag", meta_tags)
                if len(internos) > 0:
                    insert_data(new_name, "Links internos", list(internos))
                if len(externos) > 0:
                    insert_data(new_name, "Links externos", list(externos))
                insert_data(new_name, "Termos", termos)
                insert_data(new_name, "Vocabulário", vocabulario)

                print(new_name + " done!!")

        # Se não houver resposta, continua com o próximo link na lista
        except requests.exceptions.RequestException:
            continue

    return documentos


def search_term(term):
    documents = search_documents()
    print("Entrou aqui, documentos: ", documents)
    result = search(term, documents)
    print("Entrou aqui, resultado: ", result)
    return result


class Tela_Principal(QMainWindow):
    def __init__(self, *args, **argvs):
        super(Tela_Principal, self).__init__(*args, **argvs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.submit_sentence)

    def submit_sentence(self):
        sentence = self.ui.lineEdit.text()

        if len(sentence) < 1:
            message_box("Erro", "Frase não recebida, tente novamente")

        result = search_term(sentence)

        if len(sentence) > 0:
            self.ui.textBrowser.setText(result)
        else:
            self.ui.textBrowser.setText("A sentença retornada possui menos de uma letra")


app = QApplication(sys.argv)
if QDialog.Accepted:
    window = Tela_Principal()
    window.show()
sys.exit(app.exec_())
