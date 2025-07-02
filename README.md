# Lift-Performance-Predictor

A desktop application suite designed for managing and predicting powerlifting performance data. The project consists of two main components: a data management GUI to handle records and a predictive modeling GUI that estimates strength metrics based on user attributes.

## Features
This project is split into two powerful, user-friendly applications:

1. Performance Database (data.py)

- A graphical user interface for managing a database of athlete performance records stored in a local CSV file.
- View Data: Displays all records in a clean, sortable table.
- Add Records: Easily insert new athlete data, including ID, sex, age, experience, bodyweight, and lift numbers.
- Delete Records: Remove entries from the database using their unique ID.
- Data Persistence: All data is saved in data.csv, making it easy to view, edit, or use elsewhere.
- Input Validation: Checks for duplicate IDs to maintain data integrity.

3. Lift Predictor (Main.py)

- A predictive tool that uses a machine learning model to estimate an individual's performance in the three main powerlifts.
- Predictive Model: Utilizes a Linear Regression model trained on the data from data.csv.
- User Input: Takes sex, age, years of experience, and bodyweight as inputs.
- Instant Predictions: Provides estimated 1-rep maxes for the Squat, Deadlift, and Bench Press.
- Dynamic Training: The model automatically retrains on the latest data every time the application is launched, ensuring predictions improve as more data is added.

## Tech Stack

- GUI: customtkinter for a modern and responsive user interface.
- Data Manipulation: pandas for efficient data handling and processing.
- Machine Learning: scikit-learn for building and training the linear regression model.
- Core Language: Python 3

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Zefad/Lift-Performance-Predictor.git
cd Lift-Performance-Predictor
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Simply Run main.py for Prediction.
```bash
python main.py
```

2. Run data.py for data manipulation:
```
python data.py
```



