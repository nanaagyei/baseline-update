import inspect
from PySide6.QtWidgets import QFileDialog
import pandas as pd
import pickle
from sqlalchemy import create_engine


class structtype():
    pass


def load(self):
    global df
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly
    file_name, _ = QFileDialog.getOpenFileName(
        self, "Open File", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
    if file_name:
        try:
            # Read the Excel file into a pandas DataFrame
            df = pd.read_excel(file_name)
            # Save the DataFrame to a file using pickle
            with open('df.pkl', 'wb') as f:
                pickle.dump(df, f)
        except Exception as e:
            # Print an error message and return None if there was a problem reading the file
            print(f'Error reading file: {e}')
            return None
    else:
        # Return None if no file was selected
        return None
    # return df


# The purpose of the code is to handle the activation of a combo box and store the selected index and corresponding string value into a database.


# This function is responsible for establishing a connection to a SQLite database.
# It determines the calling function name using the inspect module, and based on that,
# it connects to a specific database (either "on_combo_box_database.db" or "geoid_combo_box_database.db").
# It then creates a table named "combo_box_values" in the selected database if it doesn't already exist. Finally, it returns the database engine.

def connect_to_database():
    # Get the name of the calling function
    calling_function_name = inspect.stack()[1][3]

    if calling_function_name == "on_combo_box_activated":
        # Connect to the on_combo_box_database.db database
        engine = create_engine("sqlite:///on_combo_box_database.db")
    elif calling_function_name == "geoid_combo_box_activated":
        # Connect to the geoid_combo_box_database.db database
        engine = create_engine("sqlite:///geoid_combo_box_database.db")
    else:
        # If the calling function is not recognized, raise an exception
        raise Exception("Unknown calling function: {}".format(
            calling_function_name))

    # Create the combo_box_values table if it does not exist
    engine.execute(
        "CREATE TABLE IF NOT EXISTS combo_box_values (combo_index INTEGER, string_value TEXT, function_name TEXT)")

    return engine


# This function is meant to be triggered when an item in a combo box is activated. The function takes an index as an argument, representing the selected index from the combo box.

def on_combo_box_activated(self, index):
    # Get the selected index and the corresponding string value from the combo box
    # List of options and their indices
    options = [("Normal", 0), ("Tight", 1), ("Loose", 2)]

    # Find the corresponding string for the selected index
    for option, opt_index in options:
        if index == opt_index + 1:
            text_to_print = option
            break
    else:  # If no option is found, set text_to_print to an empty string
        text_to_print = ""

    # Print the index, string value, and function name to the console
    print("index:", index)
    print("string value:", text_to_print)
    print("function name: on_combo_box_activated")

    # Connect to the on_combo_box_database.db database
    engine = create_engine("sqlite:///on_combo_box_database.db")

    # Create a dataframe specific to the on_combo_box_activated function
    on_combo_box_df = pd.DataFrame({"combo_index": [index], "string_value": [
                                   text_to_print], "function_name": ["on_combo_box_activated"]})

    # Write the dataframe to the database
    on_combo_box_df.to_sql("combo_box_values", engine,
                           if_exists="replace", index=False)

    return text_to_print


def geoid_combo_box_activated(self, index):
    options = [("LET OPUS CHOOSE", 0), ("GEOID 18", 1), ("GEOID 12B", 2), ("GEOID 12A", 3), ("GEOID 09", 4),
               ("GEOID 06", 5), ("GEOID 03", 6), ("USGG2012", 7), ("USGG2009", 8)]  # List of options and their indices

    # Find the corresponding string for the selected index
    for option, opt_index in options:
        if index == opt_index + 1:
            text_to_print = option
            break
    else:  # If no option is found, set text_to_print to an empty string
        text_to_print = ""

    # Print the index, string value, and function name to the console
    print("index:", index)
    print("string value:", text_to_print)
    print("function name: geoid_combo_box_activated")

    # Connect to the geoid_combo_box_database.db database
    engine = create_engine("sqlite:///geoid_combo_box_database.db")

    # Create a dataframe specific to the geoid_combo_box_activated function
    geoid_combo_box_df = pd.DataFrame({"combo_index": [index], "string_value": [
                                      text_to_print], "function_name": ["geoid_combo_box_activated"]})

    # Write the dataframe to the database
    geoid_combo_box_df.to_sql(
        "combo_box_values", engine, if_exists="replace", index=False)

    return text_to_print


def elevation_cutoff_activated(self, index):
    options = [("10.0", 0), ("15.0", 1)]  # List of options and their indices

    # Find the corresponding string for the selected index
    for option, opt_index in options:
        if index == opt_index + 1:
            text_to_print = option
            break
    else:  # If no option is found, set text_to_print to an empty string
        text_to_print = ""

    # Print the index, string value, and function name to the console
    print("index:", index)
    print("string value:", text_to_print)
    print("function name: elevation_cutoff_activated")

    # Connect to the geoid_combo_box_database.db database
    engine = create_engine("sqlite:///elevated_cutoff_database.db")

    # Create a dataframe specific to the geoid_combo_box_activated function
    geoid_combo_box_df = pd.DataFrame({"combo_index": [index], "string_value": [
                                      text_to_print], "function_name": ["elevation_cutoff_activated"]})

    # Write the dataframe to the database
    geoid_combo_box_df.to_sql(
        "combo_box_values", engine, if_exists="replace", index=False)

    return text_to_print


def reference_frame_combo_box_activated(self, index):
    options = [("NAD_83(2011)", 0), ("ITRF2014", 1), ("IGS14", 2),
               ("WGS84", 3)]  # List of options and their indices

    # Find the corresponding string for the selected index
    for option, opt_index in options:
        if index == opt_index + 1:
            text_to_print = option
            break
    else:  # If no option is found, set text_to_print to an empty string
        text_to_print = ""

    # Print the index, string value, and function name to the console
    print("index:", index)
    print("string value:", text_to_print)
    print("function name: reference_frame_combo_box_activated")

    # Connect to the geoid_combo_box_database.db database
    engine = create_engine("sqlite:///reference_frame_combo_box_database.db")

    # Create a dataframe specific to the geoid_combo_box_activated function
    geoid_combo_box_df = pd.DataFrame({"combo_index": [index], "string_value": [
                                      text_to_print], "function_name": ["reference_frame_combo_box_activated"]})

    # Write the dataframe to the database
    geoid_combo_box_df.to_sql(
        "combo_box_values", engine, if_exists="replace", index=False)

    return text_to_print


def gnss_combo_box_activated(self, index):
    # List of options and their indices
    options = [("G (GPS- only)", 0), ("GNSS", 1)]

    # Find the corresponding string for the selected index
    for option, opt_index in options:
        if index == opt_index + 1:
            text_to_print = option
            break
    else:  # If no option is found, set text_to_print to an empty string
        text_to_print = ""

    # Print the index, string value, and function name to the console
    print("index:", index)
    print("string value:", text_to_print)
    print("function name: gnss_combo_box_activated")

    # Connect to the geoid_combo_box_database.db database
    engine = create_engine("sqlite:///gnss_combo_box_database.db")

    # Create a dataframe specific to the geoid_combo_box_activated function
    geoid_combo_box_df = pd.DataFrame({"combo_index": [index], "string_value": [
                                      text_to_print], "function_name": ["gnss_combo_box_activated"]})

    # Write the dataframe to the database
    geoid_combo_box_df.to_sql(
        "combo_box_values", engine, if_exists="replace", index=False)

    return text_to_print


def tropo_interval_combo_box_activated(self, index):
    # List of options and their indices
    options = [("7200", 0)]

    # Find the corresponding string for the selected index
    for option, opt_index in options:
        if index == opt_index + 1:
            text_to_print = option
            break
    else:  # If no option is found, set text_to_print to an empty string
        text_to_print = ""

    # Print the index, string value, and function name to the console
    print("index:", index)
    print("string value:", text_to_print)
    print("function name: tropo_interval_combo_box_activated")

    # Connect to the geoid_combo_box_database.db database
    engine = create_engine("sqlite:///tropo_interval_combo_box_database.db")

    # Create a dataframe specific to the geoid_combo_box_activated function
    geoid_combo_box_df = pd.DataFrame({"combo_index": [index], "string_value": [
                                      text_to_print], "function_name": ["tropo_interval_combo_box_activated"]})

    # Write the dataframe to the database
    geoid_combo_box_df.to_sql(
        "combo_box_values", engine, if_exists="replace", index=False)

    return text_to_print


def tropo_model_combo_box_activated(self, index):
    # List of options and their indices
    options = [("Step-Offset", 0), ("Piecewise Linear", 1)]

    # Find the corresponding string for the selected index
    for option, opt_index in options:
        if index == opt_index + 1:
            text_to_print = option
            break
    else:  # If no option is found, set text_to_print to an empty string
        text_to_print = ""

    # Print the index, string value, and function name to the console
    print("index:", index)
    print("string value:", text_to_print)
    print("function name: tropo_model_combo_box_activated")

    # Connect to the geoid_combo_box_database.db database
    engine = create_engine("sqlite:///tropo_model_combo_box_database.db")

    # Create a dataframe specific to the geoid_combo_box_activated function
    geoid_combo_box_df = pd.DataFrame({"combo_index": [index], "string_value": [
                                      text_to_print], "function_name": ["tropo_model_combo_box_activated"]})

    # Write the dataframe to the database
    geoid_combo_box_df.to_sql(
        "combo_box_values", engine, if_exists="replace", index=False)

    return text_to_print
# selected_text = ""

# def on_combo_box_activated(self, index):
#     global selected_text
#     selected_text = self.itemText(index)
#     if index == 1:
#         text_to_print = "Normal"
#         print("Normal")
#     elif index == 2:
#         text_to_print = "Tight"
#         print("Tight")
#     elif index ==3:
#         text_to_print = "Loose"
#         print("Loose")
#     else:
#         text_to_print = ""  # Set text_to_print to an empty string if index is invalid


#     # Connect to the database
#     engine = create_engine("sqlite:///mydatabase.db")

#     # Create a dataframe with the index and string values
#     df = pd.DataFrame({"index": [index], "string_value": [text_to_print]})

#     # Write the dataframe to the database
#     df.to_sql("combo_box_values", engine, if_exists="replace", index=False)


# selected_text = ""

# def geoid_combo_box_activated(self, index):
#     global selected_text
#     selected_text = self.itemText(index)
#     if index == 0:
#         text_to_print = "LET OPUS CHOOSE"
#         print("LET OPUS CHOOSE")
#     elif index == 1:
#         text_to_print =  "GEOID 18"
#         print( "GEOID 18")
#     elif index ==2:
#         text_to_print = "GEOID 12B"
#         print("GEOID 12B")
#     elif index ==3:
#         text_to_print = "GEOID 12A"
#         print("GEOID 12A")
#     elif index ==4:
#         text_to_print =  "GEOID 09"
#         print( "GEOID 09")
#     elif index ==5:
#         text_to_print =  "GEOID 06"
#         print( "GEOID 06")
#     elif index ==6:
#         text_to_print = "GEOID 03"
#         print("GEOID 03")
#     elif index ==7:
#         text_to_print = "USGG2012"
#         print("USGG2012")
#     elif index ==8:
#         text_to_print = "USGG2009"
#         print("USGG2009")
#     else:
#         text_to_print = ""  # Set text_to_print to an empty string if index is invalid


#     # Connect to the database
#     engine = create_engine("sqlite:///mydatabase.db")

#     # Create a dataframe with the index and string values
#     df = pd.DataFrame({"index": [index], "string_value": [text_to_print]})

#     # Write the dataframe to the database
#     df.to_sql("combo_box_values", engine, if_exists="replace", index=False)

# def connect_to_database():
#     engine = create_engine("sqlite:///mydatabase.db")
#     engine.execute("CREATE TABLE IF NOT EXISTS combo_box_values (combo_index INTEGER, string_value TEXT, function_name TEXT)")
#     return engine

# def on_combo_box_activated(self, index):
#     global selected_text
#     selected_text = self.itemText(index)
#     options = [("Normal", 1), ("Tight", 2), ("Loose", 3)]  # List of options and their indices

#     # Find the corresponding string for the selected index
#     for option, opt_index in options:
#         if index == opt_index:
#             text_to_print = option
#             break
#     else:  # If no option is found, set text_to_print to an empty string
#         text_to_print = ""

#     # Connect to the database
#     engine = connect_to_database()

#     # Create a dataframe specific to the on_combo_box_activated function
#     on_combo_box_df = pd.DataFrame({"combo_index": [index], "string_value": [text_to_print], "function_name": ["on_combo_box_activated"]})

#     # Write the dataframe to the database
#     on_combo_box_df.to_sql("combo_box_values", engine, if_exists="append", index=False)


# def geoid_combo_box_activated(self, index):
#     global selected_text
#     selected_text = self.itemText(index)
#     options = [("LET OPUS CHOOSE", 0), ("GEOID 18", 1), ("GEOID 12B", 2), ("GEOID 12A", 3), ("GEOID 09", 4), ("GEOID 06", 5), ("GEOID 03", 6), ("USGG2012", 7), ("USGG2009", 8)]  # List of options and their indices

#         # Find the corresponding string for the selected index
#     for option, opt_index in options:
#         if index == opt_index:
#             text_to_print = option
#             break
#     else:  # If no option is found, set text_to_print to an empty string
#         text_to_print = ""

#     # Connect to the database
#     engine = connect_to_database()

#     # Create a dataframe specific to the geoid_combo_box_activated function
#     geoid_combo_box_df = pd.DataFrame({"combo_index": [index], "string_value": [text_to_print], "function_name": ["geoid_combo_box_activated"]})

#     # Write the dataframe to the database
#     geoid_combo_box_df.to_sql("combo_box_values", engine, if_exists="append", index=False)

# def on_combo_box_activated(self, combo_box, index):
#     selected_index = combo_box.currentIndex()
#     selected_text = combo_box.itemText(selected_index)
#     options = [("Normal", 0), ("Tight", 1), ("Loose", 2)]  # List of options and their indices

#     # Find the corresponding string for the selected index
#     for option, opt_index in options:
#         if index == opt_index:
#             text_to_print = option
#             break
#     else:  # If no option is found, set text_to_print to an empty string
#         text_to_print = ""

#     # Print the index, string value, and function name to the console
#     print("index:", index)
#     print("string value:", text_to_print)
#     print("function name: on_combo_box_activated")

#     # Connect to the on_combo_box_database.db database
#     engine = create_engine("sqlite:///on_combo_box_database.db")

#     # Create a dataframe specific to the on_combo_box_activated function
#     on_combo_box_df = pd.DataFrame({"combo_index": [index], "string_value": [text_to_print], "function_name": ["on_combo_box_activated"]})

#     # Write the dataframe to the database
#     on_combo_box_df.to_sql("combo_box_values", engine, if_exists="replace", index=False)
