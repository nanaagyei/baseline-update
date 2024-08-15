import sys
from PySide6.QtWidgets import QApplication,QButtonGroup, QGroupBox, QRadioButton, QMainWindow, QTabWidget, QLabel, QComboBox, QPushButton, QVBoxLayout, QMenuBar, QMenu, QFileDialog, QHBoxLayout, QTabBar, QFrame, QWidget
from PySide6.QtGui import QAction
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QSplitter
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OPUS PROJECT BASELINE GENERATOR")

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

        # Add the left frame to the splitter
        splitter.addWidget(left_frame)

        # Create a layout for the left frame
        left_layout = QVBoxLayout()
        left_frame.setLayout(left_layout)

        # Create a button to create a new project
        self.new_project_button = QPushButton("New Project")
        self.new_project_button.clicked.connect(self.new_project)
        left_layout.addWidget(self.new_project_button)

        # Create a button to open a project
        self.open_project_button = QPushButton("Open Project")
        self.open_project_button.clicked.connect(self.open_project)
        left_layout.addWidget(self.open_project_button)

        # Create a button to save a project
        self.save_project_button = QPushButton("Save Project")
        self.save_project_button.clicked.connect(self.save_project)
        left_layout.addWidget(self.save_project_button)

        # Create a button to export a project
        self.export_project_button = QPushButton("Export Project")
        self.export_project_button.clicked.connect(self.export_project)
        left_layout.addWidget(self.export_project_button)

        # Create a button to close a project
        self.close_project_button = QPushButton("Close Project")
        self.close_project_button.clicked.connect(self.close_project)
        left_layout.addWidget(self.close_project_button)

        # Create a button to import data
        self.import_data_button = QPushButton("Import Data")
        self.import_data_button.clicked.connect(self.import_data)
        left_layout.addWidget(self.import_data_button)

        # Create a button to create a new layer
        self.new_layer_button = QPushButton("New Layer")
        self.new_layer_button.clicked.connect(self.new_layer)
        left_layout.addWidget(self.new_layer_button)

        # Create a button to delete a layer
        self.delete_layer_button = QPushButton("Delete Layer")
        self.delete_layer_button.clicked.connect(self.delete_layer)
        left_layout.addWidget(self.delete_layer_button)

        # Create a button to rename a layer
        self.rename_layer_button = QPushButton("Rename Layer")
        self.rename_layer_button.clicked.connect(self.rename_layer)
        left_layout.addWidget(self.rename_layer_button)

        # Create a button to reorder layers
        self.reorder_layers_button = QPushButton("Reorder Layers")
        self.reorder_layers_button.clicked.connect(self.reorder_layers)
        left_layout.addWidget(self.reorder_layers_button)

        # Create a button to create a new group
        self.new_group_button = QPushButton("New Group")
        self.new_group_button.clicked.connect(self.new_group)
        left_layout.addWidget(self.new_group_button)

        # Create a button to delete a group
        self.delete_group_button = QPushButton("Delete Group")
        self.delete_group_button.clicked.connect(self.delete_group)
        left_layout.addWidget(self.delete_group_button)

        # Create a button to rename a group
        self.rename_group_button = QPushButton("Rename Group")
        self.rename_group_button.clicked.connect(self.rename_group)
        left_layout.addWidget(self.rename_group_button)

        # Create a button to reorder groups
        self.reorder_groups_button = QPushButton("Reorder Groups")
        self.reorder_groups_button.clicked.connect(self.reorder_groups)
        left_layout.addWidget(self.reorder_groups_button)

        # Add a spacer item to the left layout to push the buttons to the top
        left_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))

        #
# Create a frame on the right to display the map and tools
        right_frame = QFrame()
        right_frame.setFrameShape(QFrame.StyledPanel)

        # Add the right frame to the splitter
        splitter.addWidget(right_frame)

        # Create a layout for the right frame
        right_layout = QVBoxLayout()
        right_frame.setLayout(right_layout)

        # Create a toolbar for the map tools
        self.toolbar = QToolBar()
        right_layout.addWidget(self.toolbar)

        # Add a spacer item to the toolbar
        self.toolbar.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Create a zoom in button
        self.zoom_in_button = QPushButton()
        self.zoom_in_button.setIcon(QIcon(":/icons/zoom_in.png"))
        self.zoom_in_button.setToolTip("Zoom In")
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.toolbar.addWidget(self.zoom_in_button)

        # Create a zoom out button
        self.zoom_out_button = QPushButton()
        self.zoom_out_button.setIcon(QIcon(":/icons/zoom_out.png"))
        self.zoom_out_button.setToolTip("Zoom Out")
        self.zoom_out_button.clicked.connect(self.zoom_out)
        self.toolbar.addWidget(self.zoom_out_button)

        # Create a pan button
        self.pan_button = QPushButton()
        self.pan_button.setIcon(QIcon(":/icons/pan.png"))
        self.pan_button.setToolTip("Pan")
        self.pan_button.clicked.connect(self.pan)
        self.toolbar.addWidget(self.pan_button)

        # Create a zoom to extent button
        self.zoom_to_extent_button = QPushButton()
        self.zoom_to_extent_button.setIcon(QIcon(":/icons/zoom_to_extent.png"))
        self.zoom_to_extent_button.setToolTip("Zoom to Extent")
        self.zoom_to_extent_button.clicked.connect(self.zoom_to_extent)
        self.toolbar.addWidget(self.zoom_to_extent_button)

        # Add the splitter to the home tab layout
        self.layout1.addWidget(splitter)

        # Set the layout of the home tab
        self.home_tab.setLayout(self.layout)
# Create a tab for the output page
        self.output_tab = QWidget()
        self.layout2 = QVBoxLayout()

        # Create a frame for the main content of the output tab
        self.output_frame = QFrame()

        # Create a layout for the output frame
        output_layout = QVBoxLayout()
        self.output_frame.setLayout(output_layout)

        # Add the QWebEngineView widget to the output layout
        output_layout.addWidget(web_view)

        # Set the layout of the output tab
        self.output_tab.setLayout(self.layout2)

        # Add the home and output tabs to the tab widget
        self.tab_widget.addTab(self.home_tab, "Home")
        self.tab_widget.addTab(self.output_tab, "Output")

        # Set the central widget of the main window to be the tab widget
        self.setCentralWidget(self.tab_widget)
    def show_html_map(self):
        # Create a QWebEngineView widget to display the HTML map
        self.web_view = QWebEngineView()

        # Load the HTML map file from a file path
        file_path = r"D:\baseline creation\index_1.html"
        self.web_view.load(QUrl.fromLocalFile(file_path))

        # Add the web view widget to the main window's layout
        self.layout().addWidget(self.web_view)
        # Connect the currentChanged signal of the tab widget to a slot
        self.tab_widget.currentChanged.connect(self.on_tab_changed)

    # Define the on_tab_changed slot
    def on_tab_changed(self, index):
        # If the output tab is selected, show the HTML map
        if index == 2:
            self.show_html_map()
    def open_file(self):
            options = QFileDialog.Options()
            options
            # Open a file dialog to select a file
            file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "", options=options)
            if file_name:
                # Do something with the selected file
                pass


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
    def new_project(self):
    # Add code here to handle the New Project button being clicked
        pass
    def open_project(self):
    # Add code here to handle the Open Project button being clicked
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
       



