import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLineEdit,
    QDesktopWidget, QHBoxLayout, QMessageBox, QLabel, QDialog, QFrame, QGridLayout, QCheckBox
)
from PyQt5.QtCore import Qt, QTimer

# Importez la classe FaceRecognition de votre module
from FaceRecognitionWithIndication import FaceRecognition


class AdminPage(QWidget):
    def __init__(self, face_recognition, name_display_widget):
        super().__init__()
        self.face_recognition = face_recognition
        self.name_display_widget = name_display_widget
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Admin Page")
        self.setGeometry(0, 0, 300, 150)
        self.center()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.id_input = QLineEdit(self)
        self.id_input.setPlaceholderText("Enter ID")
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter Password")
        verify_button = QPushButton("Verify")
        verify_button.clicked.connect(self.verify)

        layout.addWidget(self.id_input)
        layout.addWidget(self.password_input)
        layout.addWidget(verify_button)

        # Ajoutez des gestionnaires de clic pour afficher le clavier virtuel lorsque le champ est cliqué
        self.id_input.mousePressEvent = self.show_virtual_keyboard_id
        self.password_input.mousePressEvent = self.show_virtual_keyboard_password

    def verify(self):
        entered_id = self.id_input.text()
        entered_password = self.password_input.text()

        if self.face_recognition.verify_id(entered_id, entered_password):
            self.open_options_page()
        else:
            QMessageBox.critical(self, "Access Denied", "Incorrect ID or password.")

    def open_options_page(self):
        self.options_page = OptionsPage(self.face_recognition, self.name_display_widget)
        self.options_page.setWindowTitle("Options Page")
        self.options_page.show()
        self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def show_virtual_keyboard_id(self, event):
        virtual_keyboard = VirtualKeyboard(self.id_input)
        virtual_keyboard.exec_()

    def show_virtual_keyboard_password(self, event):
        virtual_keyboard = VirtualKeyboard(self.password_input)
        virtual_keyboard.exec_()


class OptionsPage(QWidget):
    def __init__(self, face_recognition, name_display_widget):
        super().__init__()
        self.face_recognition = face_recognition
        self.name_display_widget = name_display_widget
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Options Page")
        self.setGeometry(0, 0, 400, 50)
        self.center()

        layout = QVBoxLayout()
        self.setLayout(layout)

        register_button = QPushButton("Register")
        delete_button = QPushButton("Delete")

        register_button.clicked.connect(self.register)
        delete_button.clicked.connect(self.delete)

        layout.addWidget(register_button)
        layout.addWidget(delete_button)

    def register(self):
        self.registration_page = RegistrationPage(self.face_recognition, self.name_display_widget)
        self.registration_page.setWindowTitle("Registration Page")
        self.registration_page.show()
        self.close()

    def delete(self):
        self.deletion_page = DeletionPage(self.face_recognition, self.name_display_widget)
        self.deletion_page.setWindowTitle("Deletion Page")
        self.deletion_page.show()
        self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class RegistrationPage(QWidget):
    def __init__(self, face_recognition, name_display_widget):
        super().__init__()
        self.face_recognition = face_recognition
        self.name_display_widget = name_display_widget
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Registration Page")
        self.setGeometry(0, 0, 350, 150)
        self.center()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter Name")
        self.last_name_input = QLineEdit(self)
        self.last_name_input.setPlaceholderText("Enter Last Name")
        self.apartment_number_input = QLineEdit(self)
        self.apartment_number_input.setPlaceholderText("Enter Apartment Number")
        self.house_admin_checkbox = QCheckBox("House administrator")  # Add the checkbox
        register_button = QPushButton("Register")
        register_button.clicked.connect(self.register)

        layout.addWidget(self.name_input)
        layout.addWidget(self.last_name_input)
        layout.addWidget(self.apartment_number_input)
        layout.addWidget(self.house_admin_checkbox)  # Add the checkbox
        layout.addWidget(register_button)

        # Ajoutez des gestionnaires de clic pour afficher le clavier virtuel lorsque le champ est cliqué
        self.name_input.mousePressEvent = self.show_virtual_keyboard_name
        self.last_name_input.mousePressEvent = self.show_virtual_keyboard_last_name
        self.apartment_number_input.mousePressEvent = self.show_virtual_keyboard_apartment

    def register(self):
        name = self.name_input.text()
        last_name = self.last_name_input.text()
        apartment_number = self.apartment_number_input.text()
        is_house_admin = self.house_admin_checkbox.isChecked()  # Check if the checkbox is checked
        self.face_recognition.register_faces(name, last_name, apartment_number, is_house_admin)
        QMessageBox.information(self, "Registration Success", "Person successfully registered.")
        self.close()
        self.name_display_widget.update_name_list()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def show_virtual_keyboard_name(self, event):
        virtual_keyboard = VirtualKeyboard(self.name_input)
        virtual_keyboard.exec_()

    def show_virtual_keyboard_last_name(self, event):
        virtual_keyboard = VirtualKeyboard(self.last_name_input)
        virtual_keyboard.exec_()

    def show_virtual_keyboard_apartment(self, event):
        virtual_keyboard = VirtualKeyboard(self.apartment_number_input)
        virtual_keyboard.exec_()


class DeletionPage(QWidget):
    def __init__(self, face_recognition, name_display_widget):
        super().__init__()
        self.face_recognition = face_recognition
        self.name_display_widget = name_display_widget
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Deletion Page")
        self.setGeometry(0, 0, 350, 150)
        self.center()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter Name")
        self.last_name_input = QLineEdit(self)
        self.last_name_input.setPlaceholderText("Enter Last Name")
        self.apartment_number_input = QLineEdit(self)
        self.apartment_number_input.setPlaceholderText("Enter Apartment Number")
        self.house_admin_checkbox = QCheckBox("House administrator")  # Add the checkbox
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete)

        layout.addWidget(self.name_input)
        layout.addWidget(self.last_name_input)
        layout.addWidget(self.apartment_number_input)
        layout.addWidget(self.house_admin_checkbox)  # Add the checkbox
        layout.addWidget(delete_button)

        # Ajoutez des gestionnaires de clic pour afficher le clavier virtuel lorsque le champ est cliqué
        self.name_input.mousePressEvent = self.show_virtual_keyboard_name
        self.last_name_input.mousePressEvent = self.show_virtual_keyboard_last_name
        self.apartment_number_input.mousePressEvent = self.show_virtual_keyboard_apartment

    def delete(self):
        name = self.name_input.text()
        last_name = self.last_name_input.text()
        apartment_number = self.apartment_number_input.text()
        is_house_admin = self.house_admin_checkbox.isChecked()  # Check if the checkbox is checked
        result = self.face_recognition.delete_person(name, last_name, apartment_number, is_house_admin)
        if result:
            QMessageBox.information(self, "Deletion Success", "Person successfully deleted.")
        else:
            QMessageBox.critical(self, "Deletion Failed", "Person not found or deletion failed.")
        self.close()
        self.name_display_widget.update_name_list()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def show_virtual_keyboard_name(self, event):
        virtual_keyboard = VirtualKeyboard(self.name_input)
        virtual_keyboard.exec_()

    def show_virtual_keyboard_last_name(self, event):
        virtual_keyboard = VirtualKeyboard(self.last_name_input)
        virtual_keyboard.exec_()

    def show_virtual_keyboard_apartment(self, event):
        virtual_keyboard = VirtualKeyboard(self.apartment_number_input)
        virtual_keyboard.exec_()


class NameDisplayWidget(QWidget):
    def __init__(self, face_recognition):
        super().__init__()
        self.face_recognition = face_recognition

        self.layout = QHBoxLayout(self)

        self.prev_button = QPushButton("<")
        self.prev_button.clicked.connect(self.show_previous_name)
        self.layout.addWidget(self.prev_button)

        self.name_field = QLineEdit()
        self.name_field.setReadOnly(True)
        self.name_field.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.name_field)

        self.next_button = QPushButton(">")
        self.next_button.clicked.connect(self.show_next_name)
        self.layout.addWidget(self.next_button)

        self.current_name_index = 0
        self.registered_names = list(self.face_recognition.house_administrator_dict.keys())

        self.update_name_display()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_name_display)
        self.timer.start(1000)

    def update_name_list(self):
        self.registered_names = list(self.face_recognition.house_administrator_dict.keys())
        self.current_name_index = 0
        self.update_name_display()

    def update_name_display(self):
        if not self.registered_names:
            self.name_field.setText("Aucun nom enregistré")
            return

        current_name = self.registered_names[self.current_name_index]
        # Supprimez le chiffre à la fin du nom (s'il existe)
        current_name = ''.join(filter(lambda x: not x.isdigit(), current_name))
        # Remplacez les underscores par un espace
        current_name = current_name.replace("_", " ")

        self.name_field.setText(current_name)

    def show_previous_name(self):
        if not self.registered_names:
            return
        self.current_name_index = (self.current_name_index - 1) % len(self.registered_names)
        self.update_name_display()

    def show_next_name(self):
        if not self.registered_names:
            return
        self.current_name_index = (self.current_name_index + 1) % len(self.registered_names)
        self.update_name_display()


class VirtualKeyboard(QDialog):
    def __init__(self, target_input):
        super().__init__()
        self.target_input = target_input
        self.setWindowTitle("Virtual Keyboard")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Ajoutez un cadre en bas de l'écran pour le clavier virtuel
        self.keyboard_frame = QFrame()
        self.keyboard_frame.setFrameShape(QFrame.StyledPanel)
        self.keyboard_layout = QGridLayout(self.keyboard_frame)

        buttons = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
            'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
            'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l',
            'z', 'x', 'c', 'v', 'b', 'n', 'm', 'Backspace', 'Space', 'Enter'
        ]

        row, col = 0, 0
        for button_text in buttons:
            button = QPushButton(button_text)
            button.clicked.connect(self.button_click)
            self.keyboard_layout.addWidget(button, row, col)
            col += 1
            if col > 9:
                col = 0
                row += 1

        self.layout.addWidget(self.keyboard_frame)
        self.keyboard_frame.hide()  # Par défaut, masquez le clavier virtuel

    def button_click(self):
        button = self.sender()
        text = button.text()
        if text == 'Backspace':
            current_text = self.target_input.text()
            self.target_input.setText(current_text[:-1])
        elif text == 'Space':
            current_text = self.target_input.text()
            self.target_input.setText(current_text + ' ')
        elif text == 'Enter':
            self.accept()
        else:
            current_text = self.target_input.text()
            self.target_input.setText(current_text + text)

    # Afficher le clavier virtuel lorsque le champ est sélectionné
    def showEvent(self, event):
        self.keyboard_frame.show()

    # Masquer le clavier virtuel lorsque le champ perd le focus
    def hideEvent(self, event):
        self.keyboard_frame.hide()


class MainWindow(QMainWindow):
    def __init__(self, face_recognition):
        super().__init__()
        self.face_recognition = face_recognition
        self.initUI()

    def initUI(self):
        self.setWindowTitle('VisiaScan')
        screen = QDesktopWidget().screenGeometry()

        self.setGeometry(0, 0, screen.width(), screen.height())
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMinimizeButtonHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        pixmap = QPixmap("background.jpg")
        background_label = QLabel(central_widget)
        background_label.setPixmap(pixmap)
        background_label.setGeometry(0, 0, screen.width(), screen.height())

        central_layout = QVBoxLayout(central_widget)
        # Add the name display widget just above the "Sonner" button
        self.name_display_widget = NameDisplayWidget(self.face_recognition)
        central_layout.addWidget(self.name_display_widget, alignment=Qt.AlignCenter)
        button_layout = QHBoxLayout()

        self.admin_button = QPushButton("Admin")
        self.admin_button.clicked.connect(self.open_admin_page)
        button_layout.addWidget(self.admin_button, alignment=Qt.AlignLeft | Qt.AlignBottom)
        button_layout.addStretch(1)

        self.sonner_button = QPushButton("Sonner")
        self.sonner_button.clicked.connect(self.ring_action)
        central_layout.addWidget(self.sonner_button, alignment=Qt.AlignHCenter | Qt.AlignBottom)
        central_layout.addLayout(button_layout)

    def open_admin_page(self):
        self.admin_page = AdminPage(self.face_recognition, self.name_display_widget)
        self.admin_page.setWindowTitle("Admin Page")
        self.admin_page.show()

    def ring_action(self):
        # Add your code for what happens when the "Ring" button is clicked
        pass


def main():
    app = QApplication(sys.argv)
    face_recognition = FaceRecognition()
    window = MainWindow(face_recognition)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
