import logging

import numpy as np
import time


class LissajousFigure:
    """
    Фигуры Лиссажу.
    Задаётся набором точек с координатами x и y.
    """
    def __init__(self, freq_x: int = 3, freq_y: int = 2, color: str = "midnightblue", line_width: int = 2):
        self.freq_x = freq_x
        self.freq_y = freq_y
        self.color = color
        self.line_width = line_width

        self.x_arr = None
        self.y_arr = None


class LissajousGenerator:
    """
    Генерирует фигуры Лиссажу с заданными параметрами
    """
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            # Эта задержка эмулирует процедуру инициализации следующей версии генератора.
            # Задержка будет убрана после обновления.
            # Пока не трогать.
            # P.S. В новом генераторе задержка будет только при инициализации.
            # Фигуры будут генерироваться так же быстро, как и сейчас.
            time.sleep(1)
            cls.instance = super(LissajousGenerator, cls).__new__(cls)
        return cls.instance
    def __init__(self, resolution=1000):
        self.set_resolution(resolution)

    def set_resolution(self, resolution):
        """
        resolution определяет количество точек в кривой
        """
        self._resolution = resolution

    def generate_figure(self, liss_figure: LissajousFigure):
        """
        Генерирует фигуру (массивы x и y координат точек) с заданными частотами.
        """
        logging.debug("X: {}, Y: {}".format(liss_figure.freq_x, liss_figure.freq_y))

        delta = np.pi/2
        t = np.linspace(0, 2 * np.pi, self._resolution)
        x = np.sin(liss_figure.freq_x * t + delta)
        y = np.sin(liss_figure.freq_y * t)
        liss_figure.x_arr, liss_figure.y_arr = x, y
