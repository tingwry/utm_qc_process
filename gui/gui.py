import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from db.db_processing import InspectionsTable, fixedInfoTable, process_excel
from functions.data_processing import pullInsPoints, combineData
from functions.filter_data_error import filter_data_error
from functions.qc_processing import QC_data
import pandas as pd

def run_app():
    toggle_button = None
    displayed_dataframe = None  # To keep track of the currently displayed dataframe

    def upload_file():
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
            if file_path:
                file_label.config(text=file_path)
                return file_path
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload file: {str(e)}")


    def add_criteria():
        criteria_frame = ttk.Frame(criteria_container)
        criteria_frame.pack(fill='x', pady=5)
        
        criteria_dropdown = ttk.Combobox(criteria_frame, values=criteria_options)
        criteria_dropdown.set(criteria_options[0])
        criteria_dropdown.pack(side='left', padx=5)
        
        operator_dropdown = ttk.Combobox(criteria_frame, values=operator_options)
        operator_dropdown.set(operator_options[0])
        operator_dropdown.pack(side='left', padx=5)
        
        value_input = ttk.Entry(criteria_frame)
        value_input.pack(side='left', padx=5)
        
        value_type_dropdown = ttk.Combobox(criteria_frame, values=value_type_options)
        value_type_dropdown.set(value_type_options[0])
        value_type_dropdown.pack(side='left', padx=5)
        
        criteria_widgets_list.append((criteria_dropdown, operator_dropdown, value_input, value_type_dropdown))

    def process_criteria():
        nonlocal qc_result, filtered_result, toggle_button, displayed_dataframe

        try:
            db_file_path = 'TML_APM.xlsx'
            df = process_excel(db_file_path, "Table1")
            fixed = fixedInfoTable(df)
            inspections = InspectionsTable(df)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process database file: {str(e)}")
            return
        
        criteria_list.clear()
        for widgets in criteria_widgets_list:
            try:
                criteria, operator, value, value_type = widgets
                criteria_list.append({
                    'criteria': criteria.get(),
                    'operator': operator.get(),
                    'value': value.get(),
                    'value_type': value_type.get()
                })
            except Exception as e:
                messagebox.showerror("Error", f"Invalid criteria input: {str(e)}")
                return
            
        file_path = file_label.cget("text")
        sheet_name = sheetname_entry.get()
        input_unit = unit_combobox.get()
        output_unit = output_unit_combobox.get()
        
        try:
            complete_table = combineData(file_path, sheet_name, input_unit, output_unit, fixed, inspections)
            qc_result = QC_data(criteria_list, complete_table)
            filtered_result = filter_data_error(qc_result)
            displayed_dataframe = qc_result  # Set the displayed dataframe to qc_result by default
            display_result(displayed_dataframe)  # Default display
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process QC data: {str(e)}")
            return

        if toggle_button is None:
            toggle_button = tk.Button(root, text="Show Filtered Results", command=toggle_display)
            toggle_button.pack(pady=10)

        save_as_button.pack(pady=10)  # Show the Save As button after QC processing

    def display_result(dataframe):
        nonlocal displayed_dataframe
        displayed_dataframe = dataframe

        # Clear any previous results
        for widget in result_frame.winfo_children():
            widget.destroy()

        tree = ttk.Treeview(result_frame)
        tree.pack(expand=True, fill='both')

        # Define columns
        tree["column"] = list(dataframe.columns)
        tree["show"] = "headings"

        # Define column headings
        for col in tree["columns"]:
            tree.heading(col, text=col)

        # Add data to the treeview
        for index, row in dataframe.iterrows():
            tree.insert("", "end", values=list(row))

    def toggle_display():
        nonlocal display_qc_result, displayed_dataframe
        display_qc_result = not display_qc_result
        if display_qc_result:
            displayed_dataframe = qc_result
            display_result(qc_result)
            toggle_button.config(text="Show Filtered Results")
        else:
            displayed_dataframe = filtered_result
            display_result(filtered_result)
            toggle_button.config(text="Show QC Results")

    def save_as():
        if displayed_dataframe is not None:
            try:
                save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
                if save_path:
                    displayed_dataframe.to_excel(save_path, index=False)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")

    root = tk.Tk()
    root.title("QC Data Processing Application")

    file_label = tk.Label(root, text="No file selected")
    file_label.pack()
    upload_button = tk.Button(root, text="Upload APM Upload Sheet", command=upload_file)
    upload_button.pack(pady=5)

    sheetname_label = tk.Label(root, text="Sheet Name:")
    sheetname_label.pack()
    sheetname_entry = tk.Entry(root)
    sheetname_entry.pack(pady=5)

    unit_label = tk.Label(root, text="Input Unit (in or mm):")
    unit_label.pack()
    unit_combobox = ttk.Combobox(root, values=["in", "mm"])
    unit_combobox.set("in")
    unit_combobox.pack(pady=5)

    criteria_container = tk.Frame(root)
    criteria_container.pack(pady=5)

    add_criteria_button = tk.Button(root, text="Add Criteria", command=add_criteria)
    add_criteria_button.pack(pady=5)

    output_unit_label = tk.Label(root, text="Output Unit (in or mm):")
    output_unit_label.pack()
    output_unit_combobox = ttk.Combobox(root, values=["in", "mm"])
    output_unit_combobox.set("in")
    output_unit_combobox.pack(pady=5)

    finalize_button = tk.Button(root, text="Finalize Criteria and Run QC", command=process_criteria)
    finalize_button.pack(pady=10)

    save_as_button = tk.Button(root, text="Save As Excel", command=save_as)
    # Initially do not pack the save_as_button
    # save_as_button.pack(pady=10)  # Will pack it later in process_criteria

    criteria_options = [
        'nominal thickness difference (Tn - Ta)', 
        'critical thickness difference (Ta - Tr)', 
        'last reading difference (Tprev - Ta)', 
        # 'last reading difference (Ta - Tprev)', 
        'Remaining Life', 
        'Corrosion rate (ST)', 
        'Corrosion rate (LT)'
    ]
    operator_options = [
        'equals', 
        'does not equal', 
        'is greater than', 
        'is greater than or equal to', 
        'is less than', 
        'is less than or equal to'
    ]
    value_type_options = ['%', 'number']

    criteria_list = []
    criteria_widgets_list = []

    result_frame = ttk.Frame(root)
    result_frame.pack(expand=True, fill='both', padx=10, pady=10)

    display_qc_result = True  # Track which result is being displayed
    qc_result = pd.DataFrame()
    filtered_result = pd.DataFrame()

    root.mainloop()

run_app()
