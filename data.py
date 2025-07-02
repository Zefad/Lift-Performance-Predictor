import csv
import os
import pandas as pd
import customtkinter as ctk
from tkinter import ttk, messagebox

# Configure appearance
ctk.set_appearance_mode("System")  # "Light", "Dark", or "System"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue", "green", "dark-blue"

CSV_FILE = 'data.csv'

# Define the headers for the CSV file
CSV_HEADERS = ['ID', 'sex', 'experience_years', 'age', 'bodyweightkg', 'Squat', 'Deadlift', 'Bench']

# Ensure CSV file exists with headers if it's new
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(CSV_HEADERS)

class PerformanceApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Performance Database GUI")
        self.geometry("800x600")
        self.minsize(600, 400)

        # Responsive grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        header = ctk.CTkLabel(self, text="🏋️ Performance Records", font=ctk.CTkFont(size=24, weight="bold"))
        header.grid(row=0, column=0, pady=(20, 10))

        # Table frame
        table_frame = ctk.CTkFrame(self)
        table_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # Treeview
        cols = CSV_HEADERS
        self.tree = ttk.Treeview(table_frame, columns=cols, show='headings')
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        # Input frame
        input_frame = ctk.CTkFrame(self, corner_radius=10)
        input_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        # Two rows, four columns layout
        for i in range(4): input_frame.grid_columnconfigure(i, weight=1)

        fields = ['ID','sex','experience_years','age','bodyweightkg','Squat','Deadlift','Bench']
        self.entry_vars = {}
        for idx, field in enumerate(fields):
            row = (idx // 4) * 2
            col = idx % 4
            # Label
            label = ctk.CTkLabel(input_frame, text=field)
            label.grid(row=row, column=col, padx=5, pady=(5,2), sticky="w")
            # Entry
            entry = ctk.CTkEntry(input_frame, placeholder_text=field)
            entry.grid(row=row+1, column=col, padx=5, pady=(0,5), sticky="ew")
            self.entry_vars[field] = entry

        # Buttons frame
        btn_frame = ctk.CTkFrame(self)
        btn_frame.grid(row=3, column=0, pady=(0,20), sticky="ew")
        for i in range(3): btn_frame.grid_columnconfigure(i, weight=1)

        insert_btn = ctk.CTkButton(btn_frame, text="Insert", command=self.insert_record)
        insert_btn.grid(row=0, column=0, padx=10, pady=10)
        delete_btn = ctk.CTkButton(btn_frame, text="Delete by ID", command=self.delete_record)
        delete_btn.grid(row=0, column=1, padx=10, pady=10)
        refresh_btn = ctk.CTkButton(btn_frame, text="Refresh", command=self.refresh_table)
        refresh_btn.grid(row=0, column=2, padx=10, pady=10)

        # Initial load
        self.refresh_table()

    def refresh_table(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        try:
            with open(CSV_FILE, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row_dict in reader:
                    # Convert dictionary to list in the order of CSV_HEADERS
                    row_list = [row_dict[header] for header in CSV_HEADERS]
                    self.tree.insert('', 'end', values=row_list)
        except FileNotFoundError:
            messagebox.showerror("Error", f"CSV file not found: {CSV_FILE}")

    def insert_record(self):
        try:
            # Get values from entry fields
            new_record = {
                'ID': int(self.entry_vars['ID'].get()),
                'sex': self.entry_vars['sex'].get().strip(),
                'experience_years': float(self.entry_vars['experience_years'].get()),
                'age': float(self.entry_vars['age'].get()),
                'bodyweightkg': float(self.entry_vars['bodyweightkg'].get()),
                'Squat': float(self.entry_vars['Squat'].get()),
                'Deadlift': float(self.entry_vars['Deadlift'].get()),
                'Bench': float(self.entry_vars['Bench'].get())
            }

            # Read existing data to check for duplicate ID
            df = pd.read_csv(CSV_FILE)
            if new_record['ID'] in df['ID'].values:
                messagebox.showwarning("Duplicate ID", f"Record with ID {new_record['ID']} already exists.")
                return

            # Append the new record to the CSV file
            with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
                writer.writerow(new_record)

            self.refresh_table()
            messagebox.showinfo("Success", "Record inserted.")
        except ValueError:
            messagebox.showerror("Input Error", "Please ensure all fields are correctly filled and are numbers where expected.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_record(self):
        try:
            rec_id_to_delete = int(self.entry_vars['ID'].get())

            # Read all records, filter out the one to delete, and write back
            df = pd.read_csv(CSV_FILE)
            original_rows = len(df)
            df = df[df['ID'] != rec_id_to_delete]

            if len(df) == original_rows:
                messagebox.showwarning("Not found", f"No record with ID {rec_id_to_delete}")
            else:
                df.to_csv(CSV_FILE, index=False, encoding='utf-8')
                self.refresh_table()
                messagebox.showinfo("Deleted", f"Record {rec_id_to_delete} deleted.")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid ID to delete.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == '__main__':
    app = PerformanceApp()
    app.mainloop()
