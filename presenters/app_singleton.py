import sys

from PySide2.QtWidgets import QApplication, QMainWindow, QStackedWidget


class AppSingleton(object):
    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = AppSingleton()
        return cls.instance

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.application = QMainWindow()
        self.application.setWindowTitle('Code skeleton builder')
        self.centralWidget = QStackedWidget()
        self.application.setCentralWidget(self.centralWidget)
        self.application.setFixedHeight(600)
        self.application.setFixedWidth(960)
        self.is_showing = False

    def show(self):
        if not self.is_showing:
            self.is_showing = True
            self.application.show()
            sys.exit(self.app.exec_())

    def set_content(self, widget):
        self.centralWidget.addWidget(widget)
        number_of_widgets = self.centralWidget.count()
        self.centralWidget.setCurrentIndex(number_of_widgets - 1)

    def go_back(self, widget):
        self.centralWidget.removeWidget(widget)
        number_of_widgets = self.centralWidget.count()
        self.centralWidget.setCurrentIndex(number_of_widgets - 1)
