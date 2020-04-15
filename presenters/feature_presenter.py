import re
from collections import OrderedDict, namedtuple

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import (QLabel, QPushButton,
                               QVBoxLayout, QFormLayout, QHBoxLayout, QLineEdit, QFileDialog)
from PySide2.QtCore import QFile
from PySide2.QtWidgets import QDialogButtonBox
from PySide2.QtWidgets import QWidget

from common.entities import FeatureEntity
from common.interfaces import FeaturePresenterInterface
from presenters.app_singleton import AppSingleton
from use_cases.display_files_use_case import DisplayFilesUseCase


def snake(text: str):
    lower = text.lower()
    words = re.split('[ _-]+', lower)
    return '_'.join(words)


def camel(text: str):
    lower = text.lower()
    words = [word.capitalize() for word in re.split('[ _-]+', lower)]
    return ''.join(words)


def snake_list(text: str):
    items = text.split(',')
    snake_items = [snake(item.strip()) for item in items if item.strip() != '']
    return ', '.join(snake_items)


def path_to_namespace(path: str, parents_to_ignore):
    relative_path = path[len(parents_to_ignore):] if path.startswith(parents_to_ignore) else path
    path_without_extension = relative_path.split('.')[0]
    return path_without_extension.replace('/', '.')


def join_parameters(*args):
    all_the_arguments = []
    for text in args:
        items = text.split(',')
        all_the_arguments = all_the_arguments + [item.strip() for item in items if item.strip() != '']

    return ', '.join(all_the_arguments)


CURRENT_FOLDER_LIST = __file__.split('/')[:-1]
UI_FILE = '/'.join(CURRENT_FOLDER_LIST + ['ui', 'feature.ui'])

Node = namedtuple('Node', ['parent', 'value', 'children'])


class FeaturePresenter(FeaturePresenterInterface):
    def __init__(self, feature: FeatureEntity):
        self.feature = feature
        self.variable_widget_map = OrderedDict()
        self.variable_nodes_map = OrderedDict()
        self.first_node = Node(None, None, [])

    def show(self):
        app_singleton = AppSingleton.get_instance()

        file = QFile(UI_FILE)
        file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.widget = loader.load(file)

        self.parameters_form = self.widget.findChild(QWidget, 'parameters_form')  # type: QWidget

        self.form_layout = QFormLayout()
        self.parameters_form.setLayout(self.form_layout)

        self._add_variables()

        self._fill_tree()
        self._calculate_variables()

        self.button_box = self.widget.findChild(QDialogButtonBox, 'button_box')  # type: QDialogButtonBox
        self.button_box.rejected.connect(self._cancel)
        self.button_box.accepted.connect(self._accept)
        self.button_box.clicked.connect(self._clicked)

        app_singleton.set_content(self.widget)
        app_singleton.show()

    def _add_variables(self):
        layout = self.parameters_form.layout()
        for variable in self.feature.variables:
            if variable.type == 'file':
                self._add_file_variable(layout, variable)
            else:
                self._add_string_variable(layout, variable)

    def _add_file_variable(self, layout, variable):
        name = QLabel(variable.name)
        edit = QWidget()
        edit_layout = QVBoxLayout()
        edit_layout.setMargin(5)
        edit_layout.setSpacing(1)

        file_chooser_container = QWidget()
        file_chooser_layout = QHBoxLayout()
        file_chooser_layout.setMargin(0)
        file_chooser_container.setLayout(file_chooser_layout)

        line_edit = QLineEdit()
        line_edit.textChanged.connect(self._key_pressed_builder(variable))
        line_edit.setMinimumWidth(420)

        choose_button = QPushButton('browse')
        choose_button.clicked.connect(self._file_chooser_button_clicked_builder(line_edit))

        file_chooser_layout.addWidget(line_edit)
        file_chooser_layout.addWidget(choose_button)

        edit_layout.addWidget(file_chooser_container)
        description = QLabel(variable.description)
        description.setStyleSheet('font: italic; font-size: 10px')
        edit_layout.addWidget(description)
        edit.setLayout(edit_layout)
        self.variable_widget_map[variable] = line_edit
        if variable.depends_on != "":
            line_edit.setStyleSheet('color:#999;')
        else:
            name.setText(f'{name.text()} (*)')
            name.setStyleSheet('font-weight: bold;')
        layout.addRow(name, edit)

    def _add_string_variable(self, layout, variable):
        name = QLabel(variable.name)
        edit = QWidget()
        edit_layout = QVBoxLayout()
        edit_layout.setMargin(5)
        edit_layout.setSpacing(1)
        line_edit = QLineEdit()
        line_edit.textChanged.connect(self._key_pressed_builder(variable))
        line_edit.setMinimumWidth(500)
        edit_layout.addWidget(line_edit)
        description = QLabel(variable.description)
        description.setStyleSheet('font: italic; font-size: 10px')
        edit_layout.addWidget(description)
        edit.setLayout(edit_layout)
        self.variable_widget_map[variable] = line_edit
        if variable.depends_on != "":
            line_edit.setStyleSheet('color:#999;')
        else:
            name.setText(f'{name.text()} (*)')
            name.setStyleSheet('font-weight: bold;')
        layout.addRow(name, edit)

    def _key_pressed_builder(self, variable):
        the_variable = variable

        def key_pressed(text):
            self._update_values(the_variable, text)

        return key_pressed

    def _url_selected_builder(self, variable):
        the_variable = variable

        def url_selected(text):
            self._update_values(the_variable, text)

        return url_selected

    def _file_chooser_button_clicked_builder(self, line_edit):
        widget = line_edit

        def button_clicked():
            # url, _ = QFileDialog.getOpenFileUrl(line_edit, 'Select directory','~', 'Only directories', '*')
            directory = QFileDialog.getExistingDirectory(widget, "Select Folder", '')
            widget.setText(directory)

        return button_clicked

    def _update_values(self, variable, text):
        node = self.variable_nodes_map[variable]
        for child in node.children:
            self._calculate_variable_by_tree(child)

    def _fill_tree(self):
        for variable in self.feature.variables:
            node = Node(self.first_node, variable, [])
            self.variable_nodes_map[variable] = node

        for variable, node in self.variable_nodes_map.items():
            if variable.depends_on == '':
                self.first_node.children.append(node)
            else:
                dependencies = [dependency.strip() for dependency in variable.depends_on.split(',')]
                for dependency in dependencies:
                    for candidate_parent_variable in self.feature.variables:
                        if candidate_parent_variable.variable_name == dependency:
                            parent_node = self.variable_nodes_map[candidate_parent_variable]
                            parent_node.children.append(node)

        print('Nodes')
        self._print_node(self.first_node, '')

    def _print_node(self, node, spacing):
        if node == self.first_node:
            print('first node')
        else:
            print(spacing + node.value.variable_name)
        for child in node.children:
            self._print_node(child, spacing + '\t')

    def _calculate_variables(self):
        self._calculate_variable_by_tree(self.first_node)

    def _calculate_variable_by_tree(self, node):
        if node != self.first_node:
            local_variables = {}
            for variable in self.variable_widget_map.keys():
                value = self.variable_widget_map[variable].text()
                local_variables[variable.variable_name] = value
            try:
                code = node.value.autofill if node.value.autofill else "''"
                value = eval(code, globals(), local_variables)
            except Exception as exception:
                print(f'Error when evaluating: {code}')
                raise exception

            widget = self.variable_widget_map[node.value]
            widget.setText(value)

        for child in node.children:
            self._calculate_variable_by_tree(child)

    def _cancel(self):
        app_singleton = AppSingleton.get_instance()
        app_singleton.go_back(self.widget)

    def _accept(self):
        variable_values = {}
        for variable, widget in self.variable_widget_map.items():
            value = widget.text()

            variable_values[variable.variable_name] = value
            if variable.type == 'List[str]':
                items = [item.strip() for item in value.split(',')]
                variable_values[variable.variable_name + '__items'] = items

        use_case = DisplayFilesUseCase(self.feature, variable_values)
        use_case.run()

    def _clicked(self, button=None):
        if button.text() == 'Reset':
            for node in self.first_node.children:
                widget = self.variable_widget_map[node.value]
                widget.setText('')
