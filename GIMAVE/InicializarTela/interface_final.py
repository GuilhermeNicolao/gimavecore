import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QWidget,
    QMessageBox,
    QSpacerItem,
    QSizePolicy,
    QHBoxLayout
)
from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator, QFont


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Programinha (ツ)")
        self.setGeometry(100, 100, 500, 400)

        self.init_ui()

    def init_ui(self):
        # Layout principal
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)  # Centraliza todo o layout

        # Caixa de Data
        self.data_label = QLabel("Data (DD/MM/AAAA)")
        self.data_label.setAlignment(Qt.AlignCenter)  # Centraliza a label
        layout.addWidget(self.data_label)

        # Definindo a fonte maior e em negrito
        font = QFont()
        font.setPointSize(12)  # Tamanho maior
        font.setBold(True)  # Negrito
        self.data_label.setFont(font)

        # Expressão regular para validar o formato DD/MM/YYYY
        data_validator = QRegularExpressionValidator(QRegularExpression(r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$"))

        # Campos de Data (DD/MM/YYYY)
        self.data_fields = []
        for _ in range(5):  # Criando 5 campos de data
            data_field = QLineEdit(self)
            data_field.setMaxLength(10)  # Limitar para 10 caracteres
            data_field.setFont(font)
            data_field.setFixedWidth(300)  # Largura reduzida para o campo de data
            data_field.setValidator(data_validator)
            data_field.setAlignment(Qt.AlignCenter)  # Centraliza o texto dentro do campo
            self.data_fields.append(data_field)
            layout.addWidget(data_field)

        # Adicionando um espaçamento maior entre o último campo de data e a caixa de Natureza
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))  # Espaço maior entre os campos

        # Caixa de Natureza
        self.natureza_label = QLabel("Natureza")
        self.natureza_label.setFont(font)
        self.natureza_label.setAlignment(Qt.AlignCenter)  # Centraliza a label
        layout.addWidget(self.natureza_label)

        self.natureza_field = QLineEdit(self)
        self.natureza_field.setValidator(QRegularExpressionValidator(QRegularExpression("[0-9]{10}")))
        self.natureza_field.setFont(font)
        self.natureza_field.setFixedWidth(300)  # Ajustando a largura para 300, igual aos campos de data
        self.natureza_field.setAlignment(Qt.AlignCenter)  # Centraliza o texto dentro do campo
        layout.addWidget(self.natureza_field)

        # Adicionando um espaçamento entre a caixa de Natureza e os botões
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Layout para os botões (horizontal)
        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignCenter)  # Centraliza os botões

        # Botão de Executar
        self.executar_button = QPushButton("Executar", self)
        self.executar_button.setFont(font)
        self.executar_button.setFixedWidth(150)  # Largura do botão
        self.executar_button.clicked.connect(self.on_execute)
        buttons_layout.addWidget(self.executar_button)

        # Botão de Limpar
        self.limpar_button = QPushButton("Limpar", self)
        self.limpar_button.setFont(font)
        self.limpar_button.setFixedWidth(150)  # Largura do botão
        self.limpar_button.clicked.connect(self.on_clear)
        buttons_layout.addWidget(self.limpar_button)

        # Adicionando os botões ao layout principal
        layout.addLayout(buttons_layout)

        # Configuração da janela
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def on_execute(self):
        # Validação do campo Natureza
        natureza = self.natureza_field.text()
        if natureza != "3141101013":
            QMessageBox.warning(self, "Erro", "A Natureza deve ser 3141101013.", QMessageBox.Ok)
            return

        # Validação dos campos de Data
        data_values = []
        for i, data_field in enumerate(self.data_fields, start=1):
            data = data_field.text()
            if not data:
                QMessageBox.warning(self, "Erro", f"Por favor, preencha o campo de Data {i}.", QMessageBox.Ok)
                return
            data_values.append(data)

        # Armazenar as datas e a natureza em variáveis
        self.dates = data_values  # Lista com as 5 datas
        self.natureza = natureza  # A natureza

        # Exibir mensagem de sucesso
        dados = "\n".join([f"Data {i}: {data}" for i, data in enumerate(self.dates, start=1)])
        QMessageBox.information(self, "Sucesso", f"Dados recebidos:\n{dados}\nNatureza: {self.natureza}", QMessageBox.Ok)

    def on_clear(self):
        # Limpar os campos
        for data_field in self.data_fields:
            data_field.clear()
        self.natureza_field.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())