import pandas as pd
from sklearn.linear_model import LinearRegression
import customtkinter as ctk

# Configure appearance
ctk.set_appearance_mode("System")  # "Light", "Dark", or "System"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue", "green", "dark-blue"

CSV_FILE = 'data.csv'


def load_data_from_csv():
    try:
        df = pd.read_csv(CSV_FILE)
        return df.dropna()
    except FileNotFoundError:
        print(f"Error: {CSV_FILE} not found. Please ensure it exists.")
        return pd.DataFrame()


def train_model():
    df = load_data_from_csv()
    if df.empty:
        return None # Or handle more gracefully, e.g., raise an error
    # Convert sex to numerical values (1 for M, 0 for F)
    df['sex'] = df['sex'].map({'M': 1, 'F': 0})
    X = df[['sex', 'experience_years', 'age', 'bodyweightkg']]
    y = df[['Squat', 'Deadlift', 'Bench']]
    return LinearRegression().fit(X, y)

class LiftPredictorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Lift Predictor")
        # Initial size
        self.geometry("600x500")
        # Allow full resizing
        self.resizable(True, True)

        # Center window on screen
        self.center_window()

        # Train the regression model
        self.model = train_model()

        # Check if model was trained successfully
        if self.model is None:
            ctk.CTkLabel(self, text="Error: Could not train model. Data file might be empty or missing.", text_color="red").pack(pady=20)
            return # Exit if model cannot be trained

        # Configure grid for responsiveness
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Header
        header = ctk.CTkLabel(self, text="🏋️ Lift Predictor", font=ctk.CTkFont(size=24, weight="bold"))
        header.grid(row=0, column=0, pady=(20, 10))

        # Frame for inputs
        input_frame = ctk.CTkFrame(self, corner_radius=15)
        input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        input_frame.grid_columnconfigure(1, weight=1)

        # Sex
        ctk.CTkLabel(input_frame, text="Sex", font=ctk.CTkFont(size=14)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.sex_combo = ctk.CTkOptionMenu(input_frame, values=["M", "F"])
        self.sex_combo.set("M")
        self.sex_combo.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Experience
        ctk.CTkLabel(input_frame, text="Experience (years)", font=ctk.CTkFont(size=14)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.exp_entry = ctk.CTkEntry(input_frame, placeholder_text="e.g., 3.5")
        self.exp_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Age
        ctk.CTkLabel(input_frame, text="Age (years)", font=ctk.CTkFont(size=14)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.age_entry = ctk.CTkEntry(input_frame, placeholder_text="e.g., 28")
        self.age_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Bodyweight
        ctk.CTkLabel(input_frame, text="Bodyweight (kg)", font=ctk.CTkFont(size=14)).grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.weight_entry = ctk.CTkEntry(input_frame, placeholder_text="e.g., 75")
        self.weight_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        # Predict button
        self.predict_btn = ctk.CTkButton(self, text="Predict Lifts", font=ctk.CTkFont(size=16, weight="bold"), command=self.predict)
        self.predict_btn.grid(row=2, column=0, pady=20)

        # Result display
        self.result_frame = ctk.CTkFrame(self, corner_radius=15)
        self.result_frame.grid(row=3, column=0, padx=20, pady=(0,20), sticky="nsew")
        self.result_label = ctk.CTkLabel(self.result_frame, text="Enter details and click Predict", font=ctk.CTkFont(size=14))
        self.result_label.pack(padx=10, pady=10, fill="both", expand=True)

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def predict(self):
        try:
            sex_val = 1 if self.sex_combo.get().upper() == 'M' else 0
            exp_val = float(self.exp_entry.get())
            age_val = float(self.age_entry.get())
            weight_val = float(self.weight_entry.get())

            features = [[sex_val, exp_val, age_val, weight_val]]
            squat, deadlift, bench = self.model.predict(features)[0]

            result_text = (
                f"🔹 Squat: {squat:.2f} kg   |   🔹 Deadlift: {deadlift:.2f} kg   |   🔹 Bench: {bench:.2f} kg"
            )
            self.result_label.configure(text=result_text)
        except Exception as e:
            self.result_label.configure(text=f"Error: {e}")

if __name__ == '__main__':
    app = LiftPredictorApp()
    app.mainloop()
