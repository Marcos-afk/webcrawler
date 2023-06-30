import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox
from bs4 import BeautifulSoup
from django.contrib.sites import requests
from nltk import word_tokenize
from nltk.corpus import stopwords

from Ui_atividade import Ui_MainWindow
import requests
import re


def message_box(title, message):
    msg_box = QMessageBox()
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setStyleSheet(
        """
                    QMessageBox {
                        background-color: rgb(61, 61, 61);
                        color: rgb(255, 255, 255);
                    }
                    QMessageBox QLabel {
                        color: rgb(255, 255, 255);
                    }
                """
    )
    msg_box.exec_()


def open_file():
    urls = []
    with open("websites.txt", "r") as f:
        lines = f.readlines()
        for i in range(len(lines)):
            urls.append(lines[i].strip())
    return urls


def vocabulary(termos):
    lower_vocab = []
    vocab = sorted(list(set(termos)))
    for wrd in vocab:
        lower_vocab.append(wrd.lower())

    return lower_vocab


def get_html(response):
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "lxml")
    return soup


def get_terms(url):
    soup = get_html(url)

    clean_text = soup.get_text(separator=" ")
    clean_text = re.sub(r"\s+", " ", clean_text).strip()
    clean_text = re.sub(r"\d", "", clean_text)
    clean_text = re.sub(r"\W+", " ", clean_text).strip()

    termos = word_tokenize(clean_text)
    connectors = set(stopwords.words("portuguese") + stopwords.words("english"))
    termos_filtrados = [termo for termo in termos if termo not in connectors]

    return termos_filtrados


def search_documents():
    urls = open_file()
    documentos = []

    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                termos = get_terms(response)
                vocabulario = vocabulary(termos)
                for termo in vocabulario:
                    documentos.append(termo)

        except requests.exceptions.RequestException:
            continue

    return documentos


def search(consulta, documentos):
    termosConsulta = consulta.split(" ")
    resultados = []

    for documento in documentos:
        presente = any(termo in termosConsulta for termo in documento)
        resultados.append(presente)
    return resultados


def search_term(term):
    documents = search_documents()
    result = search(term, documents)
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
            return

        self.ui.pushButton.setText("Buscando....")
        self.ui.pushButton.setDisabled(True)

        try:
            QApplication.processEvents()
            result = search_term(sentence)

            if any(result):
                message_box("Sem resultados", "A matriz contém pelo menos um termo")
            else:
                message_box("Resultados", "A matriz não possui nenhum termo")
        except:
            message_box("Erro com a submissão", "Erro ao realizar busca de termos")
        finally:
            self.ui.pushButton.setText("Submeter")
            self.ui.pushButton.setDisabled(False)


app = QApplication(sys.argv)
if QDialog.Accepted:
    window = Tela_Principal()
    window.show()
sys.exit(app.exec_())
