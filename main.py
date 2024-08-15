class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OPUS PROJECT BASELINE GENERATOR")

        # # Set the window icon
        # icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
        # self.setWindowIcon(QIcon(icon_path))


        # # Set the size of the window
        # self.resize(800, 600)
        
        # Set the size and position of the window
        self.setGeometry(100, 100, 800, 600)

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

        # Create a menu for the View tab
        self.view_menu = QMenu("View")
        self.menu_bar.addMenu(self.view_menu)

        # Create a submenu for the Zoom action
        self.zoom_menu = QMenu("Zoom", self)

        # Create a menu item for the Zoom In action
        self.zoom_in_action = QAction("Zoom In", self)
        self.zoom_in_action.triggered.connect(self.zoom_in)
        self.zoom_menu.addAction(self.zoom_in_action)

        # Create a menu item for the Zoom Out action
        self.zoom_out_action = QAction("Zoom Out", self)
        self.zoom_out_action.triggered.connect(self.zoom_out)
        self.zoom_menu.addAction(self.zoom_out_action)
        # Add the submenu to the View menu
        self.view_menu.addMenu(self.zoom_menu)

        # Create a menu item for the Pan action
        self.pan_action = QAction("Pan", self)
        self.pan_action.triggered.connect(self.pan)
        self.view_menu.addAction(self.pan_action)

        # Create a menu item for the Zoom to Extent action
        self.zoom_to_extent_action = QAction("Zoom to Extent", self)
        self.zoom_to_extent_action.triggered.connect(self.zoom_to_extent)
        self.view_menu.addAction(self.zoom_to_extent_action)


#%%
#home tab

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



        # Create a small grey frame on the left
        left_frame = QFrame()
        left_frame.setFrameShape(QFrame.StyledPanel)
        # left_frame.setStyleSheet("background-color: grey;")


        # Add the left frame and the main frame to the splitter
        splitter.addWidget(left_frame)
        splitter.addWidget(self.main_frame)

        # Set the stretch factor for each frame
        splitter.setStretchFactor(0, 3)  # left frame
        splitter.setStretchFactor(1, 7)  # main frame

        # Set the splitter as the layout for the home tab
        self.layout1.addWidget(splitter)
        self.home_tab.setLayout(self.layout1)

        # Create a layout for the main frame
        self.main_layout = QVBoxLayout()

        # Set the layout of the main frame
        self.main_frame.setLayout(self.main_layout)

        # Create a run button
        self.run_button = QPushButton("Run")

        # Add the run button to the main layout
        self.main_layout.addWidget(self.run_button)

        
        # Connect the stateChanged signal of the first checkbox to the run function
        self.network_design_checkbox1.stateChanged.connect(self.run)

        # Connect the stateChanged signal of the second checkbox to the run function
        self.network_design_checkbox2.stateChanged.connect(self.run)




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
        left_tab_widget.addTab(tab2, "Parameters")
        left_tab_widget.addTab(tab3, "CORS")


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


#%%
#output tab
        # Create a tab for the Output page
        self.output_tab = QWidget()
        layout2 = QVBoxLayout()
        self.output_tab.setLayout(layout2)

        # Add the Output tab to the tab widget
        self.tab_widget.addTab(self.output_tab, "Output")
#%%
#about tab

        # Create a tab for the about page
        self.about_tab = QWidget()
        layout3 = QVBoxLayout()
        layout3.addWidget(QLabel("Welcome to the about page!"))

        self.about_tab.setLayout(layout3)

        # Add the about tab to the tab widget
        self.tab_widget.addTab(self.about_tab, "About")

        # Set the tab widget as the central widget of the main window
        self.setCentralWidget(self.tab_widget)


    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
        if file_name:
            # Read the Excel file into a pandas DataFrame
            df = pd.read_excel(file_name)
            # Save the DataFrame to a CSV file
            df.to_csv('data.csv', index=False)
            


    def open_folder(self):
        options = QFileDialog.Options()
        options
        # Open a file dialog to select a folder
        folder_name = QFileDialog.getExistingDirectory(self, "Open Folder", options=options)
        if folder_name:
            # Do something with the selected folder
            pass


    def save_file(self):
        options = QFileDialog.Options()
        options
        # Open a file dialog to save a file
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "", options=options)
        if file_name:
            # Do something with the selected file
            pass


    def zoom_in(self):
        # Do something to zoom in
        pass


    def zoom_out(self):
        # Do something to zoom out
        pass


    def pan(self):
        # Do something to pan
        pass


    def zoom_to_extent(self):
        # Do something to zoom to the extent
        pass

    def run(self):
        # Check which checkbox is selected
        if self.network_design_checkbox1.isChecked():
            # Run script A
            subprocess.run(["python", "script_A.py"])
        elif self.network_design_checkbox2.isChecked():
            # Run script B
            subprocess.run(["python", "script_B.py"])

        # Connect the stateChanged signal of the first checkbox to the run function
        self.network_design_checkbox1.stateChanged.connect(self.run)

        # Connect the stateChanged signal of the second checkbox to the run function
        self.network_design_checkbox2.stateChanged.connect(self.run)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
       

