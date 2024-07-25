import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, ttk, messagebox, font
from db.db_processing import InspectionsTable, fixedInfoTable, get_processed_excel, process_excel
from functions.data_processing import pullInsPoints, combineData
from functions.filter_data_error import filter_data_error
from functions.qc_processing import QC_data
import pandas as pd
import json
import os

def run_app():
    toggle_button = None
    # noti_button = None
    displayed_dataframe = None  # To keep track of the currently displayed dataframe
    db_file_path = None
    apm_file_path = None
    default_criteria_file = "default_criteria.json"

    def upload_file(label):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
            if file_path:
                label.configure(text=file_path)
                return file_path
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload file: {str(e)}")
            return None

    def upload_db_file():
        nonlocal db_file_path
        db_file_path = upload_file(db_file_label)
        return db_file_path

    def upload_apm_file():
        nonlocal apm_file_path
        apm_file_path = upload_file(file_label)
        return apm_file_path


    def add_criteria(criteria=None):

        def update_value_type(selected_criteria):
            if selected_criteria in ['Remaining Life', 'Corrosion rate (ST)', 'Corrosion rate (LT)']:
                value_type_dropdown.set('number')
                value_type_dropdown.configure(state='disabled')
            else:
                value_type_dropdown.configure(state='normal')

        def on_criteria_selected(value):
            update_value_type(value)

        def delete_criteria(criteria_frame, widgets_tuple):
            criteria_frame.destroy()
            if widgets_tuple in criteria_widgets_list:
                criteria_widgets_list.remove(widgets_tuple)


        criteria_frame = ctk.CTkFrame(criteria_container)
        criteria_frame.pack(fill='x', pady=5)
        
        criteria_dropdown = ctk.CTkComboBox(criteria_frame, values=criteria_options, width=300, command=on_criteria_selected)
        criteria_dropdown.set(criteria.get('criteria') if criteria else criteria_options[0])
        criteria_dropdown.pack(side='left', padx=5)
        
        operator_dropdown = ctk.CTkComboBox(criteria_frame, values=operator_options, width=200)
        operator_dropdown.set(criteria.get('operator') if criteria else operator_options[0])
        operator_dropdown.pack(side='left', padx=5)
        
        value_input = ctk.CTkEntry(criteria_frame)
        value_input.insert(0, criteria.get('value') if criteria else "")
        value_input.pack(side='left', padx=5)
        
        value_type_dropdown = ctk.CTkComboBox(criteria_frame, values=value_type_options, width=100)
        value_type_dropdown.set(criteria.get('value_type') if criteria else value_type_options[0])
        value_type_dropdown.pack(side='left', padx=5)

        # Tuple of widgets to be added to criteria_widgets_list
        widgets_tuple = (criteria_dropdown, operator_dropdown, value_input, value_type_dropdown)

        delete_button = ctk.CTkButton(
            criteria_frame,
            text="Delete",
            command=lambda: delete_criteria(criteria_frame, widgets_tuple),
            fg_color="#2B2B2B", 
            hover_color="#2B2B2B", 
            text_color="#1F6AA5",  
        )
        delete_button.pack(side='left', padx=5)

        
        criteria_widgets_list.append(widgets_tuple)

        # Call update_value_type with the initial value of criteria_dropdown
        initial_criteria = criteria_dropdown.get()
        update_value_type(initial_criteria)



    def set_default_criteria():
        criteria_list.clear()
        for widgets in criteria_widgets_list:
            criteria, operator, value, value_type = widgets
            criteria_list.append({
                'criteria': criteria.get(),
                'operator': operator.get(),
                'value': value.get(),
                'value_type': value_type.get()
            })
        try:
            with open(default_criteria_file, 'w') as file:
                json.dump(criteria_list, file)
            messagebox.showinfo("Success", "Default criteria set successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to set default criteria: {str(e)}")

    def load_default_criteria():
        if os.path.exists(default_criteria_file):
            try:
                with open(default_criteria_file, 'r') as file:
                    default_criteria = json.load(file)
                for criteria in default_criteria:
                    add_criteria(criteria)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load default criteria: {str(e)}")
        else:
            add_criteria()


    def process_criteria():
        nonlocal qc_result, filtered_result, toggle_button, noti_button, displayed_dataframe

        if not db_file_path:
            messagebox.showerror("Error", "APM Export file not selected.")
            return
        
        if not apm_file_path:
            messagebox.showerror("Error", "APM Upload Sheet file not selected.")
            return

        db_sheet_name = db_sheetname_entry.get().strip()
        apm_sheet_name = apm_sheetname_entry.get().strip()
        if not db_sheet_name or not apm_sheet_name:
            messagebox.showerror("Error", "Sheet name cannot be blank.")
            return

        criteria_list.clear()
        for widgets in criteria_widgets_list:
            try:
                criteria, operator, value, value_type = widgets
                if not value.get().strip():
                    messagebox.showerror("Error", "All value inputs must be filled.")
                    return
                criteria_list.append({
                    'criteria': criteria.get(),
                    'operator': operator.get(),
                    'value': value.get(),
                    'value_type': value_type.get()
                })
            except Exception as e:
                messagebox.showerror("Error", f"Invalid criteria input: {str(e)}")
                return

        db_input_unit = db_unit_combobox.get()
        apm_input_unit = apm_unit_combobox.get()
        output_unit = output_unit_combobox.get()

        try:
            # df = process_excel(db_file_path, db_sheet_name, db_input_unit, output_unit)
            df = get_processed_excel(db_file_path, db_sheet_name, db_input_unit, output_unit)
            fixed = fixedInfoTable(df)
            inspections = InspectionsTable(df)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process APM Export file: {str(e)}")
            return

        try:
            complete_table = combineData(apm_file_path, apm_sheet_name, db_input_unit, apm_input_unit, output_unit, fixed, inspections)
            qc_result = QC_data(criteria_list, complete_table)
            filtered_result = filter_data_error(qc_result)
            displayed_dataframe = qc_result  # Set the displayed dataframe to qc_result by default
            display_result(displayed_dataframe)  # Default display
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process QC data: {str(e)}")
            return

        if toggle_button is None:
            toggle_button = ctk.CTkButton(root, text="Show Filtered Results", command=toggle_display, fg_color="#FFFFFF", hover_color="#cccccc", text_color="#0072bc")
            toggle_button.pack(pady=10)  # Adjust pack position

        save_as_button.pack(pady=10)  # Show the Save As button after QC processing

        # if noti_button is None:
        #     email_label = ctk.CTkLabel(root, text="Enter Emails (comma separated):")
        #     email_label.pack(pady=5)
        #     email_entry = ctk.CTkEntry(root, width=300)
        #     email_entry.pack(pady=5)

        #     noti_button = ctk.CTkButton(root, text="Send via Ms Teams", command=lambda: notification(displayed_dataframe, email_entry.get()), fg_color="#FFFFFF", hover_color="#cccccc", text_color="#0072bc")
        #     noti_button.pack(pady=10)


        email_label.pack(pady=5)
        email_entry.pack(pady=5)
        noti_button.pack(pady=10)
            

    def display_result(dataframe):
        nonlocal displayed_dataframe
        displayed_dataframe = dataframe

        # Clear any previous results
        for widget in result_frame.winfo_children():
            widget.destroy()

        tree = ttk.Treeview(result_frame, height=4, show="headings")
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

        # Treeview Customisation (theme colors are selected)
        bg_color = root._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
        text_color = root._apply_appearance_mode(ctk.ThemeManager.theme["CTkLabel"]["text_color"])
        selected_color = root._apply_appearance_mode(ctk.ThemeManager.theme["CTkButton"]["fg_color"])

        treestyle = ttk.Style()
        treestyle.theme_use('default')
        treestyle.configure("Treeview",
                            background=bg_color,
                            foreground=text_color,
                            fieldbackground=bg_color,
                            borderwidth=0,
                            font=(font.nametofont('TkTextFont').actual(), 18),
                            rowheight=40)
        treestyle.configure("Treeview.Heading",
                        font=(font.nametofont('TkTextFont').actual(), 18))  # Set the font and size for the headings
        treestyle.map('Treeview',
                    background=[('selected', bg_color)],
                    foreground=[('selected', selected_color)])
        root.bind("<<TreeviewSelect>>", lambda event: root.focus_set())

    def toggle_display():
        nonlocal display_qc_result, displayed_dataframe
        display_qc_result = not display_qc_result
        if display_qc_result:
            displayed_dataframe = qc_result
            display_result(qc_result)
            toggle_button.configure(text="Show Filtered Results")
        else:
            displayed_dataframe = filtered_result
            display_result(filtered_result)
            toggle_button.configure(text="Show QC Results")

    def save_as():
        if displayed_dataframe is not None:
            try:
                save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
                if save_path:
                    displayed_dataframe.to_excel(save_path, index=False)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")

    # notification / send via ms teams
    def notification(dataframe, emails):
        try:
            email_list = [email.strip() for email in emails.split(",") if email.strip()]
            
            messagebox.showinfo("Success", "Notification sent successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send notification: {str(e)}")



    ctk.set_appearance_mode("dark")  # Other options: "light", "system"
    ctk.set_default_color_theme("blue")  # Other options: "dark-blue", "green"

    root = ctk.CTk()
    root.title("UTM QC Process Application")

    # Main frame for two columns, centered horizontally
    main_frame = ctk.CTkFrame(root)
    main_frame.pack(pady=10, padx=10)

    # APM Export file upload section
    db_frame = ctk.CTkFrame(main_frame)
    db_frame.pack(side='left', padx=10, pady=10)

    db_file_label = ctk.CTkLabel(db_frame, text="No file selected")
    db_file_label.pack()
    upload_db_button = ctk.CTkButton(db_frame, text="Upload APM Export File", command=upload_db_file)
    upload_db_button.pack(pady=5)

    db_sheetname_label = ctk.CTkLabel(db_frame, text="APM Export's Sheet Name:")
    db_sheetname_label.pack()
    db_sheetname_entry = ctk.CTkEntry(db_frame)
    db_sheetname_entry.pack(pady=5)

    db_unit_label = ctk.CTkLabel(db_frame, text="Input Unit (in or mm):")
    db_unit_label.pack()
    db_unit_combobox = ctk.CTkComboBox(db_frame, values=["in", "mm"])
    db_unit_combobox.set("in")
    db_unit_combobox.pack(pady=5)

    # APM upload sheet file upload section
    apm_frame = ctk.CTkFrame(main_frame)
    apm_frame.pack(side='left', padx=10, pady=10)

    file_label = ctk.CTkLabel(apm_frame, text="No file selected")
    file_label.pack()
    upload_button = ctk.CTkButton(apm_frame, text="Upload APM Upload Sheet", command=upload_apm_file)
    upload_button.pack(pady=5)

    apm_sheetname_label = ctk.CTkLabel(apm_frame, text="APM Uploader's Sheet Name:")
    apm_sheetname_label.pack()
    apm_sheetname_entry = ctk.CTkEntry(apm_frame)
    apm_sheetname_entry.pack(pady=5)

    apm_unit_label = ctk.CTkLabel(apm_frame, text="Input Unit (in or mm):")
    apm_unit_label.pack()
    apm_unit_combobox = ctk.CTkComboBox(apm_frame, values=["in", "mm"])
    apm_unit_combobox.set("in")
    apm_unit_combobox.pack(pady=5)

    # Criteria section
    criteria_container = ctk.CTkScrollableFrame(root, width=850, height=100)
    criteria_container._scrollbar.configure(height=0)
    criteria_container.pack(pady=5)

    # button frame
    button_frame = ctk.CTkFrame(root)
    button_frame.pack(pady=5)

    add_criteria_button = ctk.CTkButton(button_frame, text="Add Criteria", command=add_criteria)
    add_criteria_button.pack(side='left', padx=5)

    set_default_button = ctk.CTkButton(button_frame, text="Set Default Criteria", command=set_default_criteria)
    set_default_button.pack(side='left', padx=5)


    output_unit_label = ctk.CTkLabel(root, text="Output Unit (in or mm):")
    output_unit_label.pack()
    output_unit_combobox = ctk.CTkComboBox(root, values=["in", "mm"])
    output_unit_combobox.set("in")
    output_unit_combobox.pack(pady=5)

    finalize_button = ctk.CTkButton(root, text="Finalize Criteria and Run QC", command=process_criteria)
    finalize_button.pack(pady=10)

    save_as_button = ctk.CTkButton(root, text="Save As Excel", command=save_as)
    # Initially do not pack the save_as_button

    email_label = ctk.CTkLabel(root, text="Enter Emails (comma separated):")
    email_entry = ctk.CTkEntry(root, width=300)
    noti_button = ctk.CTkButton(root, text="Send via Ms Teams", command=lambda: notification(displayed_dataframe, email_entry.get()), fg_color="#FFFFFF", hover_color="#cccccc", text_color="#0072bc")

    criteria_options = [    
        'nominal thickness difference (Tn - Ta)',     
        'critical thickness difference (Ta - Tr)',     
        'last reading difference (Tprev - Ta)',     
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

    result_frame = ctk.CTkFrame(root)
    result_frame.pack(expand=True, fill='both', padx=10, pady=10)

    display_qc_result = True  # Track which result is being displayed
    qc_result = pd.DataFrame()
    filtered_result = pd.DataFrame()

    # Load default criteria if exists
    load_default_criteria()

    root.mainloop()

run_app()
