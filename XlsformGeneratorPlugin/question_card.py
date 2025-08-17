from qgis.PyQt.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QCheckBox, QPushButton, QGroupBox
)
from qgis.PyQt.QtCore import pyqtSignal

class QuestionCard(QWidget):
    """A widget to represent a single question in the form builder."""
    delete_requested = pyqtSignal(QWidget)

    def __init__(self, question_type, question_name, parent=None):
        super(QuestionCard, self).__init__(parent)
        self.question_type = question_type
        self.choices = []

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        card_frame = QGroupBox(self)
        card_frame.setStyleSheet("QGroupBox { border: 1px solid #ccc; border-radius: 5px; margin-top: 10px; }")
        main_layout.addWidget(card_frame)

        card_layout = QVBoxLayout()
        card_frame.setLayout(card_layout)

        # --- Header ---
        header_layout = QHBoxLayout()
        type_label = QLabel(f"Type: {self.question_type}")
        type_label.setStyleSheet("font-weight: bold;")
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.on_delete_clicked)
        header_layout.addWidget(type_label)
        header_layout.addStretch()
        header_layout.addWidget(self.delete_button)
        card_layout.addLayout(header_layout)

        # --- Basic Inputs ---
        grid_layout = QGridLayout()
        grid_layout.addWidget(QLabel("Name:"), 0, 0)
        self.name_input = QLineEdit(question_name)
        grid_layout.addWidget(self.name_input, 0, 1)

        grid_layout.addWidget(QLabel("Label:"), 1, 0)
        self.label_input = QLineEdit()
        grid_layout.addWidget(self.label_input, 1, 1)
        card_layout.addLayout(grid_layout)

        # --- Options ---
        options_layout = QHBoxLayout()
        self.required_checkbox = QCheckBox("Required")
        self.advanced_button = QPushButton("Advanced")
        self.advanced_button.setCheckable(True)
        self.advanced_button.toggled.connect(self.toggle_advanced_section)
        options_layout.addWidget(self.required_checkbox)
        options_layout.addStretch()
        options_layout.addWidget(self.advanced_button)
        card_layout.addLayout(options_layout)

        # --- Advanced Section ---
        self.advanced_group = QGroupBox("Advanced Options")
        advanced_layout = QGridLayout()
        self.advanced_group.setLayout(advanced_layout)

        advanced_layout.addWidget(QLabel("Hint:"), 0, 0)
        self.hint_input = QLineEdit()
        advanced_layout.addWidget(self.hint_input, 0, 1)

        advanced_layout.addWidget(QLabel("Appearance:"), 1, 0)
        self.appearance_input = QLineEdit()
        advanced_layout.addWidget(self.appearance_input, 1, 1)

        advanced_layout.addWidget(QLabel("Relevant:"), 2, 0)
        self.relevant_input = QLineEdit()
        advanced_layout.addWidget(self.relevant_input, 2, 1)

        advanced_layout.addWidget(QLabel("Calculation:"), 3, 0)
        self.calculation_input = QLineEdit()
        advanced_layout.addWidget(self.calculation_input, 3, 1)

        advanced_layout.addWidget(QLabel("Constraint:"), 4, 0)
        self.constraint_input = QLineEdit()
        advanced_layout.addWidget(self.constraint_input, 4, 1)

        advanced_layout.addWidget(QLabel("Constraint Message:"), 5, 0)
        self.constraint_message_input = QLineEdit()
        advanced_layout.addWidget(self.constraint_message_input, 5, 1)

        card_layout.addWidget(self.advanced_group)
        self.advanced_group.setVisible(False)

        # --- Choices Section (for select questions) ---
        if self.question_type in ['select_one', 'select_multiple']:
            self.choices_group = QGroupBox("Choices")
            choices_main_layout = QVBoxLayout()
            self.choices_group.setLayout(choices_main_layout)

            list_name_layout = QHBoxLayout()
            list_name_layout.addWidget(QLabel("List Name:"))
            self.list_name_input = QLineEdit(f"{question_name}_list")
            list_name_layout.addWidget(self.list_name_input)
            choices_main_layout.addLayout(list_name_layout)

            self.choices_layout = QVBoxLayout()
            choices_main_layout.addLayout(self.choices_layout)

            add_choice_button = QPushButton("Add Choice")
            add_choice_button.clicked.connect(self.add_choice)
            choices_main_layout.addWidget(add_choice_button)

            card_layout.addWidget(self.choices_group)
            self.add_choice()
            self.add_choice()

    def toggle_advanced_section(self, checked):
        self.advanced_group.setVisible(checked)

    def on_delete_clicked(self):
        self.delete_requested.emit(self)

    def add_choice(self):
        choice_count = len(self.choices) + 1
        choice_widget = self._create_choice_widget(f"choice{choice_count}", "")
        self.choices_layout.addWidget(choice_widget)
        self.choices.append(choice_widget)

    def _create_choice_widget(self, name, label):
        widget = QWidget()
        layout = QHBoxLayout()
        widget.setLayout(layout)

        name_input = QLineEdit(name)
        label_input = QLineEdit(label)
        delete_button = QPushButton("X")
        delete_button.setFixedWidth(30)
        delete_button.clicked.connect(lambda: self._delete_choice(widget))

        layout.addWidget(name_input)
        layout.addWidget(label_input)
        layout.addWidget(delete_button)

        widget.name_input = name_input
        widget.label_input = label_input
        return widget

    def _delete_choice(self, choice_widget):
        self.choices_layout.removeWidget(choice_widget)
        choice_widget.deleteLater()
        if choice_widget in self.choices:
            self.choices.remove(choice_widget)

    def get_data(self):
        data = {
            'type': self.question_type,
            'name': self.name_input.text(),
            'label': self.label_input.text(),
            'required': self.required_checkbox.isChecked(),
            'hint': self.hint_input.text(),
            'appearance': self.appearance_input.text(),
            'relevant': self.relevant_input.text(),
            'constraint': self.constraint_input.text(),
            'constraint_message': self.constraint_message_input.text(),
            'calculation': self.calculation_input.text()
        }
        if self.question_type in ['select_one', 'select_multiple']:
            data['list_name'] = self.list_name_input.text()
            data['choices'] = []
            for choice_widget in self.choices:
                data['choices'].append({
                    'list_name': self.list_name_input.text(),
                    'name': choice_widget.name_input.text(),
                    'label': choice_widget.label_input.text()
                })
        return data
