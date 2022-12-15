import logging
import sys
import os
import PyQt5.QtWidgets as qt
from PyQt5 import uic, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import json

from lissajousgen import LissajousGenerator, LissajousFigure


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Цвета для matplotlib
with open(resource_path("mpl.json"), mode="r") as f:
    mpl_color_dict = json.load(f)


class LissajousWindow(qt.QMainWindow):
    def __init__(self):
        super().__init__()

        self.generator = None
        logging.debug("Load UI...")
        # Загружаем интерфейс из файла
        uic.loadUi(resource_path("main_window.ui"), self)

        logging.debug("Setting Title...")
        # Ставим версию и иконку
        with open(resource_path("version.txt"), "r") as file_with_ver:
            version = file_with_ver.readline()
        self.setWindowTitle("Генератор фигур Лиссажу. Версия {}. CC BY-SA 4.0 Ivanov".format(
            version
        ))
        logging.debug("Setting Icon...")
        self.setWindowIcon(QtGui.QIcon(resource_path("icon.png")))

        # Создаём холст matplotlib
        self._fig = plt.figure(figsize=(4, 3), dpi=72)
        # Добавляем на холст matplotlib область для построения графиков.
        # В общем случае таких областей на холсте может быть несколько
        # Аргументы add_subplot() в данном случае:
        # ширина сетки, высота сетки, номер графика в сетке
        self._ax = self._fig.add_subplot(1, 1, 1)

        # Создаём qt-виджет холста для встраивания холста
        # matplotlib fig в окно Qt.
        self._fc = FigureCanvas(self._fig)
        # Связываем созданный холст c окном
        self._fc.setParent(self)
        # Настраиваем размер и положение холста
        self._fc.resize(400, 400)
        self._fc.move(20, 20)

        # Первичное построение фигуры
        self.plot_lissajous_figure(LissajousFigure())

        logging.debug("Resizing...")
        self.resize(650, 450)

        self.plot_button.clicked.connect(self.plot_button_click_handler)
        self.save_button.clicked.connect(self.save_button_click_handler)

    def plot_button_click_handler(self):
        """
        Обработчик нажатия на кнопку применения настроек
        """
        # Получаем данные из текстовых полей
        settings = {"freq_x": float(self.freq_x_lineedit.text()),
                    "freq_y": float(self.freq_y_lineedit.text()),
                    "color": mpl_color_dict[str(self.color_combobox.currentIndex())],
                    "line_width": int(self.width_combobox.currentText())}
        figure = LissajousFigure(**settings)

        # Перестраиваем график
        self.plot_lissajous_figure(figure)

    def plot_lissajous_figure(self, liss_figure: LissajousFigure):
        """
        Обновление фигуры
        """
        # Удаляем устаревшие данные с графика
        self._ax.cla()

        # Генерируем сигнал для построения
        self.generator = LissajousGenerator()
        logging.debug("Object at {}".format(self.generator))
        self.generator.generate_figure(liss_figure)

        # Строим график
        self._ax.plot(liss_figure.x_arr, liss_figure.y_arr,
                      color=liss_figure.color, linewidth=liss_figure.line_width)

        plt.axis("off")

        # Нужно, чтобы все элементы не выходили за пределы холста
        plt.tight_layout()

        # Обновляем холст в окне
        self._fc.draw()

    def save_button_click_handler(self):
        """
        Обработчик нажатия на кнопку сохранения настроек
        """
        file_path, _ = qt.QFileDialog.getSaveFileName(self, "Сохранение изображения", "picture",
                                                            "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

        if file_path == "":
            return

        plt.savefig(file_path)



if __name__ == "__main__":
    # Инициализируем приложение Qt
    app = qt.QApplication(sys.argv)

    # Создаём и настраиваем главное окно
    main_window = LissajousWindow()

    logging.debug("Show window...")
    # Показываем окно
    main_window.show()

    # Запуск приложения
    # На этой строке выполнение основной программы блокируется
    # до тех пор, пока пользователь не закроет окно.
    # Вся дальнейшая работа должна вестись либо в отдельных потоках,
    # либо в обработчиках событий Qt.
    sys.exit(app.exec_())
