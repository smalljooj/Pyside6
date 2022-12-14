from decimal import Decimal
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel,
    QMainWindow, QGridLayout, QLineEdit,
    QSpinBox, QVBoxLayout, QHBoxLayout,
    QPushButton
)

class main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("my app")
        self.M = []

        layout = QGridLayout()

        layout.addWidget(QLabel("Digite a quantidade de linhas: "), 0, 0)
        self.qtd_l_m = QSpinBox()
        layout.addWidget(self.qtd_l_m, 1, 0)

        layout.addWidget(QLabel("Digite a quantidade de colunas: "), 2, 0)
        self.qtd_c_m = QSpinBox()
        layout.addWidget(self.qtd_c_m, 3, 0)

        self.matriz = QVBoxLayout()
        layout.addLayout(self.matriz, 4, 0)
        button = QPushButton("Go")
        button.clicked.connect(self.calculate_matriz)
        layout.addWidget(button)

        self.answer = QLabel()
        layout.addWidget(self.answer)

        self.qtd_c_m.valueChanged.connect(self.matriz_resize)
        self.qtd_l_m.valueChanged.connect(self.matriz_resize)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def matriz_resize(self, v_arg):
        """ redimensiona o layout de matriz """
        self.clear_layout(self.matriz)
        for i_i in range(self.qtd_l_m.value()):
            array = QHBoxLayout()
            for j_i in range(self.qtd_c_m.value()):
                cel = QLineEdit()
                cel.setMaxLength(3)
                cel.returnPressed.connect(self.calculate_matriz)
                array.addWidget(cel)
            pipe = QLabel("|")
            array.addWidget(pipe)
            cel = QLineEdit()
            cel.setMaxLength(3)
            cel.returnPressed.connect(self.calculate_matriz)
            array.addWidget(cel)
            self.matriz.addLayout(array)

    def clear_layout(self, layout):
        """ limpa o layout de matriz do programa """
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clear_layout(child.layout())

    def calculate_matriz(self):
        """ Funcao que pega os dados inseridos pelo usuario """
        self.M = []
        for i in range(self.matriz.count()):
            child = self.matriz.itemAt(i)
            array = []
            for j in range(child.count()):
                value  = child.itemAt(j).widget().text()
                if value != "|":
                    if value == "":
                        array.append(0)
                    else:
                        array.append(float(value))
            self.M.append(array)
        self.gauss()

    def gauss(self):
        """ Funcao para calculo e impressao do escalonamento de gauss jordan """
        col = 0
        value = 0

        for line in range(len(self.M) - 1):
            for l_i in range(line, len(self.M) - 1):
                if self.M[line][col] == 0:
                    bigger = value
                    count_swap_line = line
                    for m_i in range(line, len(self.M)):
                        if abs(self.M[m_i][col]) > bigger:
                            bigger = abs(self.M[m_i][col])
                            count_swap_line = m_i
                    swap_line = self.M[count_swap_line]
                    self.M[count_swap_line] = self.M[line]
                    self.M[line] = swap_line
                else:
                    value = Decimal(str(self.M[l_i + 1][col])) / Decimal(str(self.M[line][col]))
                for c_i in range(col, len(self.M[0])):
                    self.M[l_i + 1][c_i] = Decimal(str(self.M[l_i + 1][c_i])
                                                   ) - Decimal(str(self.M[line][c_i])) * value
            col += 1
        str_ = ""
        for i in self.M:
            for j in i:
                str_ += f" {j:.2f} "
            str_ += "\n"
        font_ = self.answer.font()
        font_.setBold(True)
        font_.setPointSize(10)
        self.answer.setFont(font_)
        self.answer.setText(str_)

app = QApplication(sys.argv)
window = main_window()
window.show()
sys.exit(app.exec_())
