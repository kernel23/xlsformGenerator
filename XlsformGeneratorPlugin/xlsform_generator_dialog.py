import datetime
from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QGroupBox, QScrollArea, QWidget,
    QToolButton, QMenu, QFileDialog, QMessageBox
)
from qgis.PyQt.QtCore import pyqtSignal

from .question_card import QuestionCard

try:
    import openpyxl
except ImportError:
    openpyxl = None

class XLSFormGeneratorDialog(QDialog):
    """The main dialog for the XLSForm Generator plugin."""

    def __init__(self, parent=None):
        super(XLSFormGeneratorDialog, self).__init__(parent)
        self.setWindowTitle("XLSForm Generator")

        self.question_types = [
            'text', 'integer', 'decimal', 'date', 'select_one', 'select_multiple',
            'geopoint', 'image', 'audio', 'video', 'note', 'calculate',
            'acknowledge', 'begin group', 'end group', 'begin repeat', 'end repeat'
        ]
        self.survey_questions = []
        self.question_counter = 0

        main_layout = QVBoxLayout()
        # ... (rest of the __init__ method is the same as before) ...
        # --- Survey Settings ---
        settings_group = QGroupBox("Survey Settings")
        settings_layout = QGridLayout()
        self.form_title_label = QLabel("Form Title:")
        self.form_title_input = QLineEdit("My Awesome Survey")
        settings_layout.addWidget(self.form_title_label, 0, 0)
        settings_layout.addWidget(self.form_title_input, 0, 1)
        self.form_id_label = QLabel("Form ID:")
        self.form_id_input = QLineEdit("my_awesome_survey")
        settings_layout.addWidget(self.form_id_label, 1, 0)
        settings_layout.addWidget(self.form_id_input, 1, 1)
        self.upload_button = QPushButton("Upload Existing XLSForm")
        settings_layout.addWidget(self.upload_button, 2, 0, 1, 2)
        settings_group.setLayout(settings_layout)
        main_layout.addWidget(settings_group)

        # --- Form Builder Area ---
        form_builder_group = QGroupBox("Form Builder")
        form_builder_layout = QVBoxLayout()

        add_question_layout = QHBoxLayout()
        self.add_question_button = QToolButton()
        self.add_question_button.setText("Add Question")
        self.add_question_button.setPopupMode(QToolButton.InstantPopup)
        add_question_menu = QMenu(self)
        for q_type in self.question_types:
            action = add_question_menu.addAction(q_type)
            action.triggered.connect(lambda checked, t=q_type: self.add_question(t))
        self.add_question_button.setMenu(add_question_menu)
        add_question_layout.addWidget(self.add_question_button)
        add_question_layout.addStretch()
        form_builder_layout.addLayout(add_question_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.questions_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)

        form_builder_layout.addWidget(self.scroll_area)
        form_builder_group.setLayout(form_builder_layout)
        main_layout.addWidget(form_builder_group)

        # --- Action Buttons ---
        button_layout = QHBoxLayout()
        self.generate_button = QPushButton("Generate & Download XLSForm")
        self.generate_button.clicked.connect(self.generate_xlsform) # Connect signal
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)

        button_layout.addStretch()
        button_layout.addWidget(self.generate_button)
        button_layout.addWidget(self.close_button)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.resize(800, 700)

    def add_question(self, question_type):
        self.question_counter += 1
        question_name = f"q{self.question_counter}"
        card = QuestionCard(question_type, question_name)
        card.delete_requested.connect(self.delete_question)
        self.questions_layout.addWidget(card)
        self.survey_questions.append(card)

    def delete_question(self, card_widget):
        self.questions_layout.removeWidget(card_widget)
        card_widget.deleteLater()
        if card_widget in self.survey_questions:
            self.survey_questions.remove(card_widget)

    def generate_xlsform(self):
        if openpyxl is None:
            QMessageBox.critical(self, "Dependency Error",
                "The 'openpyxl' library is required to generate XLSX files. "
                "Please install it using 'pip install openpyxl' in your QGIS Python environment.")
            return

        # --- Get Save Path ---
        default_filename = f"{self.form_id_input.text()}.xlsx"
        save_path, _ = QFileDialog.getSaveFileName(self, "Save XLSForm", default_filename, "Excel Files (*.xlsx)")
        if not save_path:
            return

        # --- Collect Data ---
        survey_data = []
        choices_data = []
        for card in self.survey_questions:
            q_data = card.get_data()

            row = {
                'type': q_data['type'],
                'name': q_data['name'],
                'label': q_data['label'],
                'hint': q_data['hint'],
                'required': 'yes' if q_data['required'] else 'no',
                'appearance': q_data['appearance'],
                'relevant': q_data['relevant'],
                'constraint': q_data['constraint'],
                'constraint: message': q_data['constraint_message'],
                'calculation': q_data['calculation']
            }

            if q_data['type'] in ['select_one', 'select_multiple']:
                row['type'] = f"{q_data['type']} {q_data['list_name']}"
                if 'choices' in q_data:
                    choices_data.extend(q_data['choices'])

            survey_data.append(row)

        settings_data = [{
            'form_title': self.form_title_input.text(),
            'form_id': self.form_id_input.text(),
            'version': datetime.date.today().strftime("%Y%m%d%H%M")
        }]

        # --- Write to XLSX ---
        wb = openpyxl.Workbook()

        # Survey Sheet
        ws_survey = wb.active
        ws_survey.title = "survey"
        survey_headers = ['type', 'name', 'label', 'hint', 'required', 'relevant', 'constraint', 'constraint: message', 'calculation', 'appearance']
        ws_survey.append(survey_headers)
        for row_data in survey_data:
            ws_survey.append([row_data.get(h, '') for h in survey_headers])

        # Choices Sheet
        if choices_data:
            ws_choices = wb.create_sheet("choices")
            choices_headers = ['list_name', 'name', 'label']
            ws_choices.append(choices_headers)
            for row_data in choices_data:
                ws_choices.append([row_data.get(h, '') for h in choices_headers])

        # Settings Sheet
        ws_settings = wb.create_sheet("settings")
        settings_headers = ['form_title', 'form_id', 'version']
        ws_settings.append(settings_headers)
        for row_data in settings_data:
            ws_settings.append([row_data.get(h, '') for h in settings_headers])

        # --- Save File ---
        try:
            wb.save(save_path)
            QMessageBox.information(self, "Success", f"XLSForm saved successfully to:\n{save_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save XLSForm:\n{e}")
