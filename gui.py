
# gui design
import os
import subprocess
import sys
from PySide6.QtWidgets import QApplication, QButtonGroup, QGroupBox, QRadioButton, QMainWindow, QTabWidget, QLabel, QComboBox, QPushButton, QVBoxLayout, QMenuBar, QMenu, QFileDialog, QHBoxLayout, QTabBar, QFrame, QWidget
from PySide6.QtGui import QAction, QFontMetrics, QIcon
from PySide6.QtWidgets import QSplitter, QCheckBox, QLineEdit, QTextEdit, QInputDialog
from PySide6.QtCore import Qt
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
import pandas as pd

from single_hub import create_single_hub_map, create_default_map, populate_xml_file
from five_hubs import create_five_hubs_map
# import custom_hubs
import fileloader as fl
import importlib


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OPUS PROJECTS RTN BASELINE GENERATOR (Beta)")
        self.setWindowIcon(QIcon("testlogo.png"))

        # Set the size and position of the window
        self.setGeometry(100, 100, 2000, 900)

        # Create a menu bar
        self.menu_bar = QMenuBar()

        # Create a menu for the File tab
        self.file_menu = QMenu("File")
        self.menu_bar.addMenu(self.file_menu)

        # Create a menu item to open a file
        self.open_action = QAction("Open", self)
        self.open_action.triggered.connect(self.open_file)
        self.file_menu.addAction(self.open_action)

        # Create a menu item to open a folder
        self.open_folder_action = QAction("Open Folder", self)
        self.open_folder_action.triggered.connect(self.open_folder)
        self.file_menu.addAction(self.open_folder_action)

        # Create a menu item to save a file
        self.save_action = QAction("Save", self)
        self.save_action.triggered.connect(self.save_file)
        self.file_menu.addAction(self.save_action)


# %%
# Home Tab : CONTAINS MAIN BASELINE GENERATION FEATURES

        # Set the menu bar as the main window's menu bar
        self.setMenuBar(self.menu_bar)

        # Create a tab widget
        self.tab_widget = QTabWidget()

        # Create a tab for the home page
        self.home_tab = QWidget()
        self.layout1 = QVBoxLayout()

        # Create a frame for the main content of the home tab
        self.main_frame = QFrame()

        # Create a splitter to divide the home tab into two frames
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Create a small frame on the left (TO CONTAIN TEXT OR INPUTS)
        left_frame = QFrame()
        left_frame.setFrameShape(QFrame.StyledPanel)

        # Create a splitter to divide the main frame into two frames
        main_splitter = QSplitter(Qt.Orientation.Vertical)

        # Create the map_display frame
        map_display_frame = QFrame()

        # Create the run_button frame
        run_button_frame = QFrame()

        # Create a run button and add it to the run_button frame
        self.run_button = QPushButton("Run")
        run_button_layout = QVBoxLayout()
        run_button_layout.addWidget(self.run_button)
        run_button_frame.setLayout(run_button_layout)

        # Create a reset button and add it to the run_button frame
        self.reset_button = QPushButton("Reset")
        reset_button_layout = QVBoxLayout()
        reset_button_layout.addWidget(self.reset_button)
        run_button_frame.setLayout(reset_button_layout)
        run_button_layout.addWidget(self.reset_button)

        # Create the default map
        default_map = create_default_map()

        # Create a QWebEngineView object and load the default map into it
        self.view = QWebEngineView()
        self.view.setHtml(default_map._repr_html_())

        # Create a layout for the map_display frame
        map_display_layout = QVBoxLayout()

        # Add the view to the layout
        map_display_layout.addWidget(self.view)

        # Set the layout for the map_display frame
        map_display_frame.setLayout(map_display_layout)

        # Add the map_display and run_button frames to the main splitter
        main_splitter.addWidget(map_display_frame)
        main_splitter.addWidget(run_button_frame)

        # Set the stretch factor for each frame
        main_splitter.setStretchFactor(0, 2)  # map_display frame
        main_splitter.setStretchFactor(1, 1)  # run_button frame

        # Set the main splitter as the layout for the main frame
        self.main_frame_layout = QVBoxLayout()
        self.main_frame_layout.addWidget(main_splitter)
        self.main_frame.setLayout(self.main_frame_layout)

        # Add the left frame and the main frame to the splitter
        splitter.addWidget(left_frame)
        splitter.addWidget(self.main_frame)

        # Set the stretch factor for each frame
        splitter.setStretchFactor(0, 3)  # left frame
        splitter.setStretchFactor(1, 7)  # main frame

        # Set the splitter as the layout for the home tab
        self.layout1.addWidget(splitter)
        self.home_tab.setLayout(self.layout1)

        # Connect the run function to the clicked signal of the run button
        self.run_button.clicked.connect(self.run)

        # connect the reset function to the clicked signal of the reset button
        self.reset_button.clicked.connect(self.reset)

        # START ADDING INPUT INFO TO LEFT FRAME (WHERE THE INPUTS ARE REQUIRED)
        # Create a tab widget for the left frame
        left_tab_widget = QTabWidget()
        # Create a layout for the left frame
        left_frame_layout = QVBoxLayout()

        # Add the left tab widget to the layout
        left_frame_layout.addWidget(left_tab_widget)

        # Set the layout of the left frame
        left_frame.setLayout(left_frame_layout)

        # Create three tabs for the left frame
        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget()

        # Add the tabs to the left tab widget
        left_tab_widget.addTab(tab1, "Network Design")
        left_tab_widget.addTab(tab2, "OPUS Projects Parameters")
        left_tab_widget.addTab(tab3, "CORS")

# network design tab
        # Create a group box
        group_box = QGroupBox("NETWORK DESIGNS")
        group_box.setStyleSheet("QGroupBox { font-weight: bold; }")

        # Create  labels
        network_design_label1 = QLabel(
            "Constrains a Single Hub in the network:")
        # network_design_label2 = QLabel("Constrains 5 Hubs in the network:")
        network_design_label3 = QLabel("Constrains all Hubs in the network:")
        network_design_label4 = QLabel("Customise your network:")

        # Create Check boxes
        self.network_design_checkbox1 = QCheckBox("Single Hub Network")
        # self.network_design_checkbox2 = QCheckBox("5-Hubs Network")
        self.network_design_checkbox3 = QCheckBox("All-Hubs Network")
        self.network_design_checkbox4 = QCheckBox("Custom Network")

        # Add the check boxes to the group box
        group_box.setLayout(QVBoxLayout())
        group_box.layout().addWidget(self.network_design_checkbox1)
        # group_box.layout().addWidget(self.network_design_checkbox2)
        group_box.layout().addWidget(self.network_design_checkbox3)
        group_box.layout().addWidget(self.network_design_checkbox4)

        # Create a button group and add the radio buttons to it
        button_group = QButtonGroup()
        button_group.addButton(self.network_design_checkbox1)
        # button_group.addButton(self.network_design_checkbox2)
        button_group.addButton(self.network_design_checkbox3)
        button_group.addButton(self.network_design_checkbox4)

        # Make the button group not exclusive
        button_group.setExclusive(False)

        # Define the uncheck_other_buttons function
        def uncheck_other_buttons(button):
            for btn in button_group.buttons():
                if btn != button:
                    btn.setChecked(False)

        # Connect the buttonClicked signal of the button group to the uncheck_other_buttons function
        button_group.buttonClicked.connect(uncheck_other_buttons)

        # Add the entry box to the group box
        group_box.setLayout(QVBoxLayout())
        group_box.layout().addWidget(network_design_label1)
        group_box.layout().addWidget(self.network_design_checkbox1)
        # group_box.layout().addWidget(network_design_label2)
        # group_box.layout().addWidget(self.network_design_checkbox2)
        group_box.layout().addWidget(network_design_label3)
        group_box.layout().addWidget(self.network_design_checkbox3)
        group_box.layout().addWidget(network_design_label4)
        group_box.layout().addWidget(self.network_design_checkbox4)

        # Set the layout of "Tab 1"
        tab1_layout = QVBoxLayout()
        tab1.setLayout(tab1_layout)
        tab1_layout.addWidget(group_box)

       # Create a second group box
        group_box_2 = QGroupBox("CUSTOM NETWORK DESIGN")
        group_box_2.setStyleSheet("QGroupBox { font-weight: bold; }")

        # Create a description label
        description_label1 = QLabel("Specify number of clusters")
        description_label2 = QLabel("Specify number of hubs to constrain")
        # description_label3 = QLabel("Constrain all hubs")

        # Create combo boxes
        combo_box1 = QComboBox()
        combo_box2 = QComboBox()
        # network_design_checkbox3 = QCheckBox("Constrain all hubs")

        # Add options to the combo boxes
        combo_box1.insertItem(0, "Select a number or enter a custom value")
        combo_box2.insertItem(0, "Select a number or enter a custom value")
        for i in range(1, 6):
            combo_box1.addItem(str(i))
            combo_box2.addItem(str(i))
        # combo_box1.addItem("Enter number")
        # combo_box2.addItem("Enter number")

        def handle_combo_box1(self):
            global select_cluster
            for i in range(1, 6):
                if i == combo_box1.currentIndex():
                    select_cluster = i

        def handle_combo_box2(self):
            global select_hub
            for i in range(1, 6):
                if i == combo_box2.currentIndex():
                    select_hub = i

        combo_box1.activated.connect(handle_combo_box1)
        combo_box2.activated.connect(handle_combo_box2)

        # Allow the user to input a custom value
        combo_box1.setEditable(True)
        combo_box2.setEditable(True)

        # Add the combo boxes to the group box
        group_box_2.setLayout(QVBoxLayout())
        group_box_2.layout().addWidget(description_label1)
        group_box_2.layout().addWidget(combo_box1)
        group_box_2.layout().addWidget(description_label2)
        group_box_2.layout().addWidget(combo_box2)
        # group_box_2.layout().addWidget(description_label3)
        # group_box_2.layout().addWidget(network_design_checkbox3)

        # Add the group box to the layout of "Tab 1"
        tab1_layout.addWidget(group_box_2)

        # Define the disable_custom_selection function in the main window class
        def disable_custom_selection(button):
            if self.network_design_checkbox4.isChecked():
                group_box_2.setEnabled(True)

            else:
                group_box_2.setEnabled(False)

        # Connect the buttonClicked signal of the button group to the disable_custom_selection function
        button_group.buttonClicked.connect(disable_custom_selection)

# opus projects processing parameters tab
        # Create a group box in "Tab 2"
        group_box_3 = QGroupBox("OPUS PROJECT PROCESSING PREFERENCES ")
        group_box_3.setStyleSheet("QGroupBox { font-weight: bold; }")

        # Create combo boxes
        combo_tab2_box1 = QComboBox()
        combo_tab2_box2 = QComboBox()
        combo_tab2_box3 = QComboBox()
        combo_tab2_box4 = QComboBox()
        combo_tab2_box5 = QComboBox()
        combo_tab2_box6 = QComboBox()
        combo_tab2_box7 = QComboBox()

        # Create description labels
        description_tab2_label1 = QLabel("Constraint Weight")
        description_tab2_label2 = QLabel("Elevation Cutoff (deg)")
        description_tab2_label3 = QLabel("Geoid Model")
        description_tab2_label4 = QLabel("Reference Frame")
        description_tab2_label5 = QLabel("GNSS")
        description_tab2_label6 = QLabel("Troposphere Interval (s)")
        description_tab2_label7 = QLabel("Troposphere Model")

        # Add options to the combo boxes
        combo_tab2_box1.insertItem(0, "Select an option ")
        combo_tab2_box2.insertItem(0, "Select an option ")
        combo_tab2_box3.insertItem(0, "Select an option ")
        combo_tab2_box4.insertItem(0, "Select an option ")
        combo_tab2_box5.insertItem(0, "Select an option ")
        combo_tab2_box6.insertItem(0, "Select an option ")
        combo_tab2_box7.insertItem(0, "Select an option ")

        # Disable the "Option 2" option
        combo_tab2_box1.setItemData(0, Qt.NoItemFlags, Qt.UserRole - 1)
        combo_tab2_box2.setItemData(0, Qt.NoItemFlags, Qt.UserRole - 1)
        combo_tab2_box3.setItemData(0, Qt.NoItemFlags, Qt.UserRole - 1)
        combo_tab2_box4.setItemData(0, Qt.NoItemFlags, Qt.UserRole - 1)
        combo_tab2_box5.setItemData(0, Qt.NoItemFlags, Qt.UserRole - 1)
        combo_tab2_box6.setItemData(0, Qt.NoItemFlags, Qt.UserRole - 1)
        combo_tab2_box7.setItemData(0, Qt.NoItemFlags, Qt.UserRole - 1)

    # constraint weight
        # Add options to the combo boxes
        combo_tab2_box1.addItem("Normal")
        combo_tab2_box1.addItem("Tight")
        combo_tab2_box1.addItem("Loose")

        def handle_on_combo_box_activated(self):
            global on_combo_box_text
            on_combo_box_text = fl.on_combo_box_activated(
                combo_tab2_box1, combo_tab2_box1.currentIndex())

        # Connect the combo box's activated signal to a slot
        combo_tab2_box1.activated.connect(handle_on_combo_box_activated)

        # elevation cutoff
        combo_tab2_box2.addItem("10.0")
        combo_tab2_box2.addItem("15.0")

        def handle_elevation_cutoff_activated(self):
            global selected_elevation_cutoff_text
            selected_elevation_cutoff_text = fl.elevation_cutoff_activated(
                combo_tab2_box2, combo_tab2_box2.currentIndex())

        # Connect the combo box's activated signal to a slot
        combo_tab2_box2.activated.connect(handle_elevation_cutoff_activated)

    # Geiod Model
        # Add options to the combo boxes
        combo_tab2_box3.addItem("LET OPUS CHOOSE")
        combo_tab2_box3.addItem("GEOID 18")
        combo_tab2_box3.addItem("GEOID 12B")
        combo_tab2_box3.addItem("GEOID 12A")
        combo_tab2_box3.addItem("GEOID 09")
        combo_tab2_box3.addItem("GEOID 06")
        combo_tab2_box3.addItem("GEOID 03")
        combo_tab2_box3.addItem("USGG2012")
        combo_tab2_box3.addItem("USGG2009")

        def handle_geoid_combo_box_activation(self):
            global selected_geoid_text
            selected_geoid_text = fl.geoid_combo_box_activated(
                combo_tab2_box3, combo_tab2_box3.currentIndex())

        # Connect the combo box's activated signal to a slot
        combo_tab2_box3.activated.connect(handle_geoid_combo_box_activation)

    # Reference Frame
        combo_tab2_box4.addItem("LET OPUS CHOOSE")
        combo_tab2_box4.addItem("NAD_83(2011)")
        combo_tab2_box4.addItem("ITRF2014")
        combo_tab2_box4.addItem("IGS14")
        combo_tab2_box4.addItem("WGS84")

        def reference_frame_combo_box_activation(self):
            global selected_reference_frame_text
            selected_reference_frame_text = fl.reference_frame_combo_box_activated(
                combo_tab2_box4, combo_tab2_box4.currentIndex())

        # Connect the combo box's activated signal to a slot
        combo_tab2_box4.activated.connect(reference_frame_combo_box_activation)

    # GNSS
        combo_tab2_box5.addItem("G (GPS- only) ")
        combo_tab2_box5.addItem("GNSS")

        def gnss_combo_box_activation(self):
            global selected_gnss_text
            selected_gnss_text = fl.gnss_combo_box_activated(
                combo_tab2_box5, combo_tab2_box5.currentIndex())

        # Connect the combo box's activated signal to a slot
        combo_tab2_box5.activated.connect(gnss_combo_box_activation)

    # Tropo Interval
        combo_tab2_box6.addItem("7200")

        def tropo_interval_combo_box_activation(self):
            global selected_tropo_interval_text
            selected_tropo_interval_text = fl.tropo_interval_combo_box_activated(
                combo_tab2_box6, combo_tab2_box6.currentIndex())

        combo_tab2_box6.activated.connect(tropo_interval_combo_box_activation)

    # Tropo Model
        combo_tab2_box7.addItem("Step-Offset")
        combo_tab2_box7.addItem("Piecewise Linear")

        def tropo_model_combo_box_activation(self):
            global selected_tropo_model_text
            selected_tropo_model_text = fl.tropo_model_combo_box_activated(
                combo_tab2_box7, combo_tab2_box7.currentIndex())

        combo_tab2_box7.activated.connect(tropo_model_combo_box_activation)

    # Disable the option for the user to enter their own value
        combo_tab2_box1.setEditable(False)
        combo_tab2_box2.setEditable(False)
        combo_tab2_box3.setEditable(False)
        combo_tab2_box4.setEditable(False)
        combo_tab2_box5.setEditable(False)
        combo_tab2_box6.setEditable(False)
        combo_tab2_box7.setEditable(False)

        # Add the combo boxes to the group box
        group_box_3.setLayout(QVBoxLayout())
        group_box_3.layout().addWidget(description_tab2_label1)
        group_box_3.layout().addWidget(combo_tab2_box1)
        group_box_3.layout().addWidget(description_tab2_label2)
        group_box_3.layout().addWidget(combo_tab2_box2)
        group_box_3.layout().addWidget(description_tab2_label3)
        group_box_3.layout().addWidget(combo_tab2_box3)
        group_box_3.layout().addWidget(description_tab2_label4)
        group_box_3.layout().addWidget(combo_tab2_box4)
        group_box_3.layout().addWidget(description_tab2_label5)
        group_box_3.layout().addWidget(combo_tab2_box5)
        group_box_3.layout().addWidget(description_tab2_label6)
        group_box_3.layout().addWidget(combo_tab2_box6)
        group_box_3.layout().addWidget(description_tab2_label7)
        group_box_3.layout().addWidget(combo_tab2_box7)


# CORS tab
        # Set the layout of "Tab 2"
        tab2_layout = QVBoxLayout()
        tab2.setLayout(tab2_layout)
        # Add the group box to the layout of "Tab 2"
        tab2_layout.addWidget(group_box_3)

        # Create a group box
        group_box_cors1 = QGroupBox("SUGGESTED CORS")
        group_box_cors1.setStyleSheet("QGroupBox { font-weight: bold; }")

        # Create a label
        cors_tab_label1 = QLabel("Do you want to use suggested CORS?:")

        # Create check boxes
        cors_check_box1 = QCheckBox("Yes")
        cors_check_box2 = QCheckBox("No")

        # Add the check boxes to the button group, and set the id parameter for each check box
        button_group_cors1 = QButtonGroup()
        button_group_cors1.addButton(cors_check_box1)
        button_group_cors1.addButton(cors_check_box2)

        # Make the button group not exclusive
        button_group_cors1.setExclusive(False)

        # Define the uncheck_other_buttons_cors function in the main window class
        def uncheck_other_buttons_cors(button):
            for btn in button_group_cors1.buttons():
                if btn != button:
                    btn.setChecked(False)

        # Connect the buttonClicked signal of the button group to the uncheck_other_buttons function
        button_group_cors1.buttonClicked.connect(uncheck_other_buttons_cors)

        # Add the check boxes to the group box
        group_box_cors1.setLayout(QVBoxLayout())
        group_box_cors1.layout().addWidget(cors_tab_label1)
        group_box_cors1.layout().addWidget(cors_check_box1)
        group_box_cors1.layout().addWidget(cors_check_box2)

        # Create a group box
        group_box_cors2 = QGroupBox("CUSTOM HUB SELECTION")
        group_box_cors2.setStyleSheet("QGroupBox { font-weight: bold; }")

        # Create  labels
        cors_tab_label2 = QLabel("For a Single hub")
        cors_tab_label2.setStyleSheet("QLabel { font-weight: bold; }")
        cors_tab_label3 = QLabel("Enter the hub you want to constrain:")
        cors_tab_label4 = QLabel("For multiple hubs")
        cors_tab_label4.setStyleSheet("QLabel { font-weight: bold; }")
        cors_tab_label5 = QLabel(
            "Enter the hubs you want to constrain (press enter button for next line):")

        # Create an entry box 1
        entry_box_single_hub = QLineEdit()

        # Add the entry box to the group box
        group_box_cors2.setLayout(QVBoxLayout())
        group_box_cors2.layout().addWidget(cors_tab_label2)
        group_box_cors2.layout().addWidget(cors_tab_label3)
        group_box_cors2.layout().addWidget(entry_box_single_hub)

       # Create an entry box
        entry_box_multi_hubs = QTextEdit()

        # Set the fixed height of the entry box to the height of two lines of text
        font = entry_box_multi_hubs.font()
        metrics = QFontMetrics(font)
        line_height = metrics.lineSpacing()
        entry_box_multi_hubs.setFixedHeight(4 * line_height)

        # Add the entry box to the group box
        group_box_cors2.setLayout(QVBoxLayout())
        group_box_cors2.layout().addWidget(cors_tab_label4)
        group_box_cors2.layout().addWidget(cors_tab_label5)
        group_box_cors2.layout().addWidget(entry_box_multi_hubs)

        # Create a group box
        group_box_cors3 = QGroupBox("EXCLUDE HUBS ")
        group_box_cors3.setStyleSheet("QGroupBox { font-weight: bold; }")

        # Create  labels
        cors_tab_label6 = QLabel(
            "Do you want to exclude Hubs from the Network?")
        cors_tab_label7 = QLabel(
            "Enter the hubs you want to exclude (press enter button for next line):")

        # Create check boxes
        cors_check_box3 = QCheckBox("Yes")
        cors_check_box4 = QCheckBox("No")

        # Add the check boxes to the button group, and set the id parameter for each check box
        button_group_cors3 = QButtonGroup()
        button_group_cors3.addButton(cors_check_box3)
        button_group_cors3.addButton(cors_check_box4)

        # Make the button group not exclusive
        button_group_cors3.setExclusive(False)

        # Define the uncheck_other_buttons_cors function in the main window class
        def uncheck_other_buttons_cors(button):
            for btn in button_group_cors3.buttons():
                if btn != button:
                    btn.setChecked(False)

        # Connect the buttonClicked signal of the button group to the uncheck_other_buttons function
        button_group_cors3.buttonClicked.connect(uncheck_other_buttons_cors)

        # Create an entry box 1
        entry_box_hub_exclusion = QTextEdit()

        # Set the fixed height of the entry box to the height of two lines of text
        font = entry_box_hub_exclusion.font()
        metrics = QFontMetrics(font)
        line_height = metrics.lineSpacing()
        entry_box_hub_exclusion.setFixedHeight(10 * line_height)

        # Add the entry box to the group box
        group_box_cors3.setLayout(QVBoxLayout())
        group_box_cors3.layout().addWidget(cors_tab_label6)
        group_box_cors3.layout().addWidget(cors_check_box3)
        group_box_cors3.layout().addWidget(cors_check_box4)
        group_box_cors3.layout().addWidget(cors_tab_label7)
        group_box_cors3.layout().addWidget(entry_box_hub_exclusion)

        # Create a layout for the CORS tab
        tab3_layout = QVBoxLayout()
        # Set the layout of the CORS tab
        tab3.setLayout(tab3_layout)
        # Add the group box to the layout
        tab3_layout.addWidget(group_box_cors1)
        # Add the group box to the layout
        tab3_layout.addWidget(group_box_cors2)
        # Add the group box to the layout
        tab3_layout.addWidget(group_box_cors3)

        # Define the disable_custom_selection function in the main window class

        def disable_custom_selection(button):
            if cors_check_box1.isChecked():
                group_box_cors2.setEnabled(False)

            else:
                group_box_cors2.setEnabled(True)

        def uncheck_other_buttons_cors(button):
            for btn in button_group_cors3.buttons():
                if btn != button:
                    btn.setChecked(False)

            # Disable the entry_box_hub_exclusion text edit box if "No" check box is checked
            if button == cors_check_box4:
                entry_box_hub_exclusion.setEnabled(False)
            # Enable the entry_box_hub_exclusion text edit box if "Yes" check box is checked
            else:
                entry_box_hub_exclusion.setEnabled(True)

        # Connect the buttonClicked signal of the button group to the disable_custom_selection function
        button_group_cors1.buttonClicked.connect(disable_custom_selection)

        # Connect the buttonClicked signal of the button group to the uncheck_other_buttons_cors function
        button_group_cors3.buttonClicked.connect(uncheck_other_buttons_cors)

        # Add the home tab to the tab widget
        self.tab_widget.addTab(self.home_tab, "Home")


# %%
# DATA DIRECTORY INFO :  THIS TAB WILL BE ABOUT WHERE THE RINEX INFO WILL BE STORED

        # Create a tab for the about page
        self.about_tab = QWidget()
        layout3 = QVBoxLayout()
        layout3.addWidget(QLabel("CLOUD STORAGE PART"))

        self.about_tab.setLayout(layout3)

        # Add the about tab to the tab widget
        self.tab_widget.addTab(self.about_tab, "Data Directory")

        # Set the tab widget as the central widget of the main window
        self.setCentralWidget(self.tab_widget)

    def open_file(self):
        fl.load(self)
    #     options = QFileDialog.Options()
    #     options |= QFileDialog.ReadOnly
    #     file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
    #     if file_name:
    #         try:
    #             # Read the Excel file into a pandas DataFrame
    #             df = pd.read_excel(file_name)
    #             # Save the DataFrame to a CSV file
    #             # df.to_csv('data.csv', index=False)
    #         except Exception as e:
    #             # Print an error message and return None if there was a problem reading the file
    #             print(f'Error reading file: {e}')
    #             return None
    #     else:
    #         # Return None if no file was selected
    #         return None
    #     return df

    def open_folder(self):
        options = QFileDialog.Options()
        options
        # Open a file dialog to select a folder
        folder_name = QFileDialog.getExistingDirectory(
            self, "Open Folder", options=options)
        if folder_name:
            # Do something with the selected folder
            pass

    def save_file(self):
        options = QFileDialog.Options()
        options
        # Open a file dialog to save a file
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save File", "", "", options=options)
        if file_name:
            if self.network_design_checkbox1.isChecked():
                # Do something with the selected file
                populate_xml_file(file_name, on_combo_box_text, selected_elevation_cutoff_text, email, selected_geoid_text,
                                  selected_reference_frame_text, selected_gnss_text, selected_tropo_interval_text, selected_tropo_model_text)
            elif self.network_design_checkbox4.isChecked():
                # site_code_dictionaries, selected_hubs, hub_baselines_df, cors_dict, df_clusters = custom_hubs.load_custom_hub(
                #     select_cluster, select_hub)
                # custom_hubs.populate_xml(
                #     site_code_dictionaries, selected_hubs, hub_baselines_df, cors_dict)
                pass

    # def run(self):
    #     print("test")
    #     # Check which checkbox is selected
    #     if self.network_design_checkbox1.isChecked():
    #         # Run script A
    #         subprocess.run(["python", "single_hub.py"])
    #     elif self.network_design_checkbox2.isChecked():
    #         # Run script B
    #         subprocess.run(["python", "five_hubs.py"])

    #     # Create the map with markers and lines
    #     map = create_map()

    #     # Update the view with the map
    #     self.view.setHtml(map._repr_html_())

    def run(self):
        global email
        # Check which checkbox is selected
        if self.network_design_checkbox1.isChecked():
            # Run script A
            # subprocess.run(["python", "single_hub.py"])
            # module = importlib.import_module("single_hub")
            # create_default_map = module.create_default_map
            # create_map = module.create_map
            # Create the map with markers and lines
            map = create_single_hub_map()
        elif self.network_design_checkbox3.isChecked():
            # Run script B
            # subprocess.run(["python", "five_hubs.py"])
            # module = importlib.import_module("five_hubs")
            # create_default_map = module.create_default_map
            # create_map = module.create_map
            # Create the map with markers and lines
            map = create_five_hubs_map()
        elif self.network_design_checkbox4.isChecked():
            # site_code_dictionaries, selected_hubs, hub_baselines_df, cors_dict, df_clusters = custom_hubs.load_custom_hub(
            #     select_cluster, select_hub)
            # # subprocess.run(["python", "custom_hubs.py"])
            # # module = importlib.import_module("custom_hubs")
            # create_default_map = custom_hubs.create_default_map()
            # # create_map = module.create_map
            # map = custom_hubs.create_map(site_code_dictionaries,
            #                              hub_baselines_df, df_clusters)
            pass

        # Show a pop-up window asking the user to enter their email address
        input_email, ok = QInputDialog.getText(
            None, 'Email Address', "Please enter your email address: ")
        if ok and input_email:
            # Do something with the email address (e.g. send it to a server)
            print("Email address: ", input_email)
            email = input_email

        # Update the view with the map
        self.view.setHtml(map._repr_html_())

    def reset(self):
        self.network_design_checkbox1.setChecked(False)
        self.network_design_checkbox3.setChecked(False)
        default_map = create_default_map()
        self.view.setHtml(default_map._repr_html_())

        if os.path.exists("df.pkl"):
            os.remove("df.pkl")

    # def run(self):
    #     print("test")
    #     current_checkbox = None
    #     # Check which checkbox is selected
    #     if self.network_design_checkbox1.isChecked():
    #         current_checkbox = "checkbox1"
    #         # Run script A
    #         subprocess.run(["python", "single_hub.py"])
    #         module = importlib.import_module("single_hub")
    #         create_default_map = module.create_default_map
    #         create_map = module.create_map
    #         # Create the map with markers and lines
    #         map = create_map()
    #     elif self.network_design_checkbox2.isChecked():
    #         current_checkbox = "checkbox2"
    #         # Run script B
    #         subprocess.run(["python", "five_hubs.py"])
    #         module = importlib.import_module("five_hubs")
    #         create_default_map = module.create_default_map
    #         create_map = module.create_map
    #         # Create the map with markers and lines
    #         map = create_map()
    #     elif self.network_design_checkbox3.isChecked():
    #         current_checkbox = "checkbox3"
    #         # Run script C
    #         subprocess.run(["python", "all_hubs.py"])
    #         module = importlib.import_module("all_hubs")
    #         create_default_map = module.create_default_map
    #         create_map = module.create_map
    #         # Create the map with markers and lines
    #         map = create_map()
    #     elif self.network_design_checkbox4.isChecked():
    #         current_checkbox = "checkbox4"
    #         # Run script D
    #         subprocess.run(["python", "custom_network.py"])
    #         module = importlib.import_module("custom_network")
    #         create_default_map = module.create_default_map
    #         create_map = module.create_map
    #         # Create the map with markers and lines
    #         map = create_map()

    #     # check if run button is clicked
    #     if self.run_button.isChecked():
    #         # Update the view with the map
    #         self.view.setHtml(map._repr_html_())

        # # Connect the stateChanged signal of the first checkbox to the run function
        # self.network_design_checkbox1.stateChanged.connect(self.run)

        # # Connect the stateChanged signal of the second checkbox to the run function
        # self.network_design_checkbox2.stateChanged.connect(self.run)

    def closeEvent(self, event):
        # Update the view with the default map
        default_map = create_default_map()
        self.view.setHtml(default_map._repr_html_())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
