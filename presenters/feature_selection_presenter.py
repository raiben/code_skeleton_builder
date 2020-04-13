from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import (QTextBrowser)
from PySide2.QtCore import QFile
from PySide2.QtWidgets import QDialogButtonBox
from PySide2.QtWidgets import QListWidget

from common.interfaces import FeatureSelectionPresenterInterface
from presenters.app_singleton import AppSingleton
from use_cases.display_skeleton_use_case import DisplaySkeletonUseCase

CURRENT_FOLDER_LIST = __file__.split('/')[:-1]
UI_FILE = '/'.join(CURRENT_FOLDER_LIST + ['ui', 'feature_selection.ui'])
CSS_FILE = '/'.join(CURRENT_FOLDER_LIST + ['ui', 'feature_selection.css'])
DEFAULT_INFO_FILE = '/'.join(CURRENT_FOLDER_LIST + ['ui', 'default_info.html'])


class FeatureSelectionPresenter(FeatureSelectionPresenterInterface):
    STYLESHEET = "QTextBrowser { background-color: transparent; }"

    def __init__(self, features):
        self.features = features

    def show(self):
        app_singleton = AppSingleton.get_instance()

        file = QFile(UI_FILE)
        file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.widget = loader.load(file)

        with open(CSS_FILE, 'r') as css_file:
            css = css_file.read()

        self.widget.setStyleSheet(css)
        self.feature_info = self.widget.findChild(QTextBrowser, 'feature_info')  # type: QTextBrowser

        with open(DEFAULT_INFO_FILE, 'r') as info_file:
            info_text = info_file.read()
        self.feature_info.setText(info_text)

        self.button_box = self.widget.findChild(QDialogButtonBox, 'button_box')  # type: QDialogButtonBox
        self.button_box.setDisabled(True)
        self.button_box.accepted.connect(self._accept)

        self.feature_list = self.widget.findChild(QListWidget, 'feature_list')  # type: QListWidget
        self.feature_list.addItems([feature.name for feature in self.features])
        self.feature_list.itemClicked.connect(self._item_clicked)

        #self.widget.show()

        app_singleton.set_content(self.widget)
        app_singleton.show()

    def _item_clicked(self, item):
        self.button_box.setEnabled(True)
        name = item.text()
        feature = next(feature for feature in self.features if feature.name == name)

        items = ''.join(
            [f'<li><strong>{item.name}</strong>: <i>{item.description}</i></li>' for item in feature.resources])
        new_content = f'<h3 style="color:darkred">{feature.name}</h3><p><i>{feature.description}</i></p><p>Content: </p><ol>{items}</ol>'

        self.feature_info.setText(new_content)

    def _accept(self):
        feature_name = self.feature_list.selectedItems()[0].text()
        feature = next(feature for feature in self.features if feature.name == feature_name)
        use_case = DisplaySkeletonUseCase(feature)
        use_case.run()
