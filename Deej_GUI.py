from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QCheckBox, QLineEdit, QLabel, QSpinBox, QMessageBox, QComboBox, QGridLayout
from PyQt5.QtWidgets import QFileDialog
import psutil
import yaml
import sys

class App(QWidget):

    def __init__(self):
        super().__init__()

        self.title = 'Deej Config App'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)

        self.layout = QVBoxLayout()

        # Create a dictionary to hold the user's configurations
        self.config = {
            "slider_mapping": {},
            "invert_sliders": False,
            "com_port": "COM4",
            "baud_rate": "9600",
            "noise_reduction": "default"
        }

        # Define special options
        special_options = ['master', 'mic', 'deej.unmapped', 'deej.current', 'system']

        # Create a list of running applications, remove duplicates and exclude the special options
        app_processes = list(set(proc.info["name"] for proc in psutil.process_iter(["name"])) - set(special_options))

        # Sort application processes, keep special options at the top
        self.apps = special_options + sorted(app_processes, key=str.lower)

        # Input field for the number of sliders
        self.layout.addWidget(QLabel("Number of sliders"))
        self.slider_count = QSpinBox()

        self.slider_count.setRange(1, 10)  # allow 1-10 sliders
        self.slider_count.setValue(5)  # default value
        self.layout.addWidget(self.slider_count)

        # Create a separate grid layout for the lists
        self.list_layout = QGridLayout()
        self.layout.addLayout(self.list_layout)

        # Create separate lists for the labels and lists
        self.labels = []
        self.lists = []

        for i in range(self.slider_count.value()):
            # Add a label before each list
            label = QLabel(f"Slider {i}")
            self.list_layout.addWidget(label, i % 4, 2 * (i // 4))
            self.labels.append(label)

            list_widget = QListWidget()
            list_widget.addItems(self.apps)
            list_widget.setSelectionMode(QListWidget.MultiSelection)  # allow multiple selection
            list_widget.setFixedHeight(100)  # set the height to show approximately 5 lines
            self.list_layout.addWidget(list_widget, i % 4, 2 * (i // 4) + 1)
            self.lists.append(list_widget)

        # Update the lists when the slider count changes
        self.slider_count.valueChanged.connect(self.update_lists)

        # Checkbox for invert_sliders
        self.invert_sliders = QCheckBox("Invert sliders")
        self.layout.addWidget(self.invert_sliders)

        # Input field for COM port
        self.layout.addWidget(QLabel("COM port"))
        self.com_port = QLineEdit()
        self.com_port.setText("COM4")  # default value
        self.layout.addWidget(self.com_port)

        # Input field for baud rate
        self.layout.addWidget(QLabel("Baud rate"))
        self.baud_rate = QLineEdit()
        self.baud_rate.setText("9600")  # default value
        self.layout.addWidget(self.baud_rate)

        # Dropdown menu for noise reduction
        self.layout.addWidget(QLabel("Noise reduction"))
        self.noise_reduction = QComboBox()
        self.noise_reduction.addItems(["low", "default", "high"])
        self.layout.addWidget(self.noise_reduction)

        # Create a save button
        button = QPushButton('Save', self)
        button.setToolTip('Click here to save config')
        button.clicked.connect(self.save_config)
        self.layout.addWidget(button)

        self.setLayout(self.layout)

        self.show()
        self.setFixedWidth(self.width())



    def update_lists(self):
        # Remove all existing labels and lists
        for label in self.labels:
            self.list_layout.removeWidget(label)
            label.deleteLater()
        self.labels = []

        for list_widget in self.lists:
            self.list_layout.removeWidget(list_widget)
            list_widget.deleteLater()
        self.lists = []

        # Add new labels and lists based on the slider count
        for i in range(self.slider_count.value()):
            label = QLabel(f"Slider {i}")
            self.list_layout.addWidget(label, i % 4, 2 * (i // 4))
            self.labels.append(label)

            list_widget = QListWidget()
            list_widget.addItems(self.apps)
            list_widget.setSelectionMode(QListWidget.MultiSelection)  # allow multiple selection
            list_widget.setFixedHeight(100)  # set the height to show approximately 5 lines
            self.list_layout.addWidget(list_widget, i % 4, 2 * (i // 4) + 1)
            self.lists.append(list_widget)

        # Adjust the height of the window to fit the contents
            #self.setFixedHeight(self.layout.sizeHint().height())
            self.show()
            self.setFixedHeight(self.height())
            self.adjustSize()

    def save_config(self):
        # Get the save location from the user
        save_location = QFileDialog.getSaveFileName(self, "Save config file", "", "Config Files (*.yaml)")[0]

        # Proceed only if a save location was selected
        if save_location:
            # Append .yaml if not already there
            if not save_location.endswith('.yaml'):
                save_location += '.yaml'

            # Update the config dictionary based on the UI inputs
            self.config["slider_mapping"] = {i: [item.text() for item in self.lists[i].selectedItems()] for i in
                                             range(self.slider_count.value())}
            self.config["invert_sliders"] = self.invert_sliders.isChecked()
            self.config["com_port"] = self.com_port.text()
            self.config["baud_rate"] = self.baud_rate.text()
            self.config["noise_reduction"] = self.noise_reduction.currentText()

            # Write the config dictionary to a YAML file
            with open(save_location, 'w') as file:
                yaml.dump(self.config, file)

            # Confirmation message
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Config saved successfully!")
            msg.setWindowTitle("Success")
            msg.exec_()

def main():
        app = QApplication(sys.argv)
        ex = App()
        sys.exit(app.exec_())

if __name__ == '__main__':
        main()

