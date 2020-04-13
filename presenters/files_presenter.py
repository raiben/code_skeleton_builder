import os
from typing import List

from PySide2.QtCore import QFile, Slot
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QListWidget, QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QLabel, QTextBrowser, \
    QDialogButtonBox
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import guess_lexer
from pygments.lexers.javascript import JavascriptLexer
from pygments.lexers.python import PythonLexer

from common.entities import FeatureEntity, FileEntity
from common.interfaces import FilesPresenterInterface
from presenters.app_singleton import AppSingleton
from pygments import highlight


class FilesPresenter(FilesPresenterInterface):
    CURRENT_FOLDER_LIST = __file__.split('/')[:-1]
    UI_FILE = '/'.join(CURRENT_FOLDER_LIST + ['ui', 'files.ui'])
    UI_DETAIL_FILE = '/'.join(CURRENT_FOLDER_LIST + ['ui', 'file.ui'])

    def __init__(self, feature: FeatureEntity, files: List[FileEntity]) -> None:
        self.feature = feature
        self.files = files
        self.list_of_files = None
        self.widget = None
        self.file_widget = None

    def show(self):
        app_singleton = AppSingleton.get_instance()

        file = QFile(self.UI_FILE)
        file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.widget = loader.load(file)

        self.list_of_files = self.widget.findChild(QListWidget, 'list_of_files')  # type: QListWidget
        self.list_of_files.addItems([file.name for file in self.files])
        self.list_of_files.itemClicked.connect(self._file_clicked_builder())
        container = self.widget.findChild(QWidget, 'file_container')  # type: QWidget
        container.setStyleSheet('QWidget: {background-color: transparent; }')

        self.button_box = self.widget.findChild(QDialogButtonBox, 'button_box')  # type: QDialogButtonBox
        self.button_box.rejected.connect(self._cancel)

        app_singleton.set_content(self.widget)
        app_singleton.show()

    def _file_clicked_builder(self):

        def clicked(item):
            print('click -> {}'.format(item.text()))
            container = self.widget.findChild(QWidget, 'file_container')  # type: QWidget

            children = container.children()
            for child in children:
                try:
                    child.hide()
                    container.layout().removeWidget(child)
                except Exception as exception:
                    pass
            if self.file_widget:
                self.file_widget.hide()
                container.layout().removeWidget(self.file_widget)

            file = QFile(self.UI_DETAIL_FILE)
            file.open(QFile.ReadOnly)
            loader = QUiLoader()
            self.file_widget = loader.load(file)

            file_entity = next(file for file in self.files if file.name == item.text())

            title = self.file_widget.findChild(QLabel, 'file_path')  # type: QLabel
            title.setText(file_entity.absolute_path)

            formatted_code = self._get_formatted_code(file_entity)
            content = self.file_widget.findChild(QTextBrowser, 'content')  # type: QTextBrowser
            content.setText(formatted_code)
            content.setStyleSheet('font-size:11px;')

            save_file_button = self.file_widget.findChild(QPushButton, 'save_file')  # type: QPushButton
            save_file_button.clicked.connect(self._save_file_builder(file_entity))
            if os.path.exists(file_entity.absolute_path):
                save_file_button.setDisabled(True)
            else:
                save_file_button.setEnabled(True)

            open_file_button = self.file_widget.findChild(QPushButton, 'open_file')  # type: QPushButton
            open_file_button.clicked.connect(self._open_file_builder(file_entity))
            if os.path.exists(file_entity.absolute_path):
                open_file_button.setEnabled(True)
            else:
                open_file_button.setDisabled(True)

            container.layout().addWidget(self.file_widget)

        return clicked

    def _get_formatted_code(self, fileEntity):
        lexer = None
        if fileEntity.absolute_path.endswith('.py'):
            lexer = PythonLexer()
        elif fileEntity.absolute_path.endswith('.js'):
            lexer = JavascriptLexer()
        else:
            lexer = guess_lexer(fileEntity.content)
        return highlight(fileEntity.content, lexer, HtmlFormatter(noclasses=True, linenos=True))

    def _cancel(self):
        app_singleton = AppSingleton.get_instance()
        app_singleton.go_back(self.widget)

    def _save_file_builder(self, file_entity):
        def clicked():
            folders = '/'.join(file_entity.absolute_path.split('/')[:-1])
            os.makedirs(folders)
            with open(file_entity.absolute_path, 'w') as handler:
                handler.write(file_entity.content)

            save_file_button = self.file_widget.findChild(QPushButton, 'save_file')  # type: QPushButton
            if os.path.exists(file_entity.absolute_path):
                save_file_button.setDisabled(True)
            else:
                save_file_button.setEnabled(True)

            open_file_button = self.file_widget.findChild(QPushButton, 'open_file')  # type: QPushButton
            if os.path.exists(file_entity.absolute_path):
                open_file_button.setEnabled(True)
            else:
                open_file_button.setDisabled(True)
        return clicked

    def _open_file_builder(self, file_entity):
        def clicked():
            os.system(f'charm {file_entity.absolute_path}')
        return clicked
