from PyQt6.QtWidgets import (QMainWindow, QFileDialog, QMessageBox, QHeaderView)
from PyQt6.QtCore import Qt
from PyQt6 import uic
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import glob
from FileUtil import FileUtil
from DataSetViewer import DataSetViewer


class UIPrediction(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lm = None
        self.df = None
        self.X = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

        # Load UI from file
        uic.loadUi('house_pricing.ui', self)

        # Setup connections
        self.setup_connections()

        # Configure table
        self.table_evaluation.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Update model list
        self.update_model_list()

    def setup_connections(self):
        """Setup signal-slot connections"""
        self.btn_pick_dataset.clicked.connect(self.do_pick_data)
        self.btn_view_dataset.clicked.connect(self.do_view_dataset)
        self.btn_train.clicked.connect(self.do_train)
        self.btn_evaluate.clicked.connect(self.do_evaluation)
        self.btn_save_model.clicked.connect(self.do_save_model)
        self.btn_load.clicked.connect(self.do_load_model)
        self.btn_refresh.clicked.connect(self.refresh_model_list)
        self.btn_predict.clicked.connect(self.do_prediction)

    def update_model_list(self):
        """Get list of saved model files"""
        self.model_files = glob.glob("*.zip") + glob.glob("*.pkl")
        self.model_files.sort()

        self.combo_models.clear()
        if self.model_files:
            self.combo_models.addItems(self.model_files)
        else:
            self.combo_models.addItem("No models available")

    def refresh_model_list(self):
        """Refresh model list"""
        self.update_model_list()
        if self.model_files:
            QMessageBox.information(self, "Info", f"Found {len(self.model_files)} model(s)")
        else:
            QMessageBox.warning(self, "Warning", "No model files found!")

    def do_pick_data(self):
        """Pick dataset file"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Choose dataset",
            "",
            "CSV Files (*.csv);;All Files (*.*)"
        )
        if filename:
            self.txt_dataset.setText(filename)

    def do_view_dataset(self):
        """View dataset in new window"""
        viewer = DataSetViewer(self.txt_dataset.text())
        viewer.exec()

    def do_train(self):
        """Train the model"""
        try:
            ratio = self.spin_training_rate.value() / 100
            self.df = pd.read_csv(self.txt_dataset.text())

            self.X = self.df[['Avg. Area Income', 'Avg. Area House Age', 'Avg. Area Number of Rooms',
                              'Avg. Area Number of Bedrooms', 'Area Population']]
            self.y = self.df['Price']

            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
                self.X, self.y, test_size=1 - ratio, random_state=101)

            self.lm = LinearRegression()
            self.lm.fit(self.X_train, self.y_train)

            self.lbl_status.setText("Training is finished")
            QMessageBox.information(self, "Info", "Training is finished")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Training failed: {str(e)}")

    def do_evaluation(self):
        """Evaluate the model"""
        try:
            # Clear previous results
            self.txt_coefficient.clear()
            self.table_evaluation.setRowCount(0)

            # Display intercept and coefficients
            self.txt_coefficient.append(f"Intercept: {self.lm.intercept_:.6f}\n")
            self.txt_coefficient.append("Feature                                      Coefficient")
            self.txt_coefficient.append("=" * 70)

            coeff_df = pd.DataFrame(self.lm.coef_, self.X.columns, columns=['Coefficient'])
            for index, row in coeff_df.iterrows():
                self.txt_coefficient.append(f"{index:<45s}{row['Coefficient']:>20.6f}")

            # Make predictions
            predictions = self.lm.predict(self.X_test)

            # Populate table
            from PyQt6.QtWidgets import QTableWidgetItem
            y_test_array = np.asarray(self.y_test)
            self.table_evaluation.setRowCount(len(self.X_test))

            for i in range(len(self.X_test)):
                self.table_evaluation.setItem(i, 0, QTableWidgetItem(f"{self.X_test.iloc[i][0]:.2f}"))
                self.table_evaluation.setItem(i, 1, QTableWidgetItem(f"{self.X_test.iloc[i][1]:.2f}"))
                self.table_evaluation.setItem(i, 2, QTableWidgetItem(f"{self.X_test.iloc[i][2]:.2f}"))
                self.table_evaluation.setItem(i, 3, QTableWidgetItem(f"{self.X_test.iloc[i][3]:.2f}"))
                self.table_evaluation.setItem(i, 4, QTableWidgetItem(f"{self.X_test.iloc[i][4]:.2f}"))
                self.table_evaluation.setItem(i, 5, QTableWidgetItem(f"{y_test_array[i]:.2f}"))
                self.table_evaluation.setItem(i, 6, QTableWidgetItem(f"{predictions[i]:.2f}"))

            # Calculate and display metrics
            mae = metrics.mean_absolute_error(self.y_test, predictions)
            mse = metrics.mean_squared_error(self.y_test, predictions)
            rmse = np.sqrt(mse)

            self.txt_mae.setText(f"{mae:.6f}")
            self.txt_mse.setText(f"{mse:.6f}")
            self.txt_rmse.setText(f"{rmse:.6f}")

            self.lbl_status.setText("Evaluation is finished")
            QMessageBox.information(self, "Info", "Evaluation is finished")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Evaluation failed: {str(e)}")

    def do_save_model(self):
        """Save model to file"""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Model",
            "housingmodel.zip",
            "Model Files (*.zip);;All Files (*.*)"
        )

        if filename:
            success = FileUtil.savemodel(self.lm, filename)
            if success:
                QMessageBox.information(self, "Info", f"Model saved successfully!")
                # Auto refresh the list after saving
                self.update_model_list()
            else:
                QMessageBox.critical(self, "Error", "Failed to save model!")

    def do_load_model(self):
        """Load model from file"""
        selected = self.combo_models.currentText()

        if selected == "No models available" or not selected:
            QMessageBox.warning(self, "Warning", "Please select a valid model file!")
            return

        self.lm = FileUtil.loadmodel(selected)

        if self.lm is not None:
            QMessageBox.information(self, "Info", f"Model '{selected}' loaded successfully!")
            self.lbl_status.setText(f"Loaded model: {selected}")
        else:
            QMessageBox.critical(self, "Error", f"Failed to load model '{selected}'!")

    def do_prediction(self):
        """Make prediction"""
        try:
            area_income = float(self.txt_area_income.text())
            house_age = float(self.txt_house_age.text())
            rooms = float(self.txt_rooms.text())
            bedrooms = float(self.txt_bedrooms.text())
            population = float(self.txt_population.text())

            result = self.lm.predict([[area_income, house_age, rooms, bedrooms, population]])

            self.txt_prediction_result.setText(f"{result[0]:.2f}")
        except ValueError:
            QMessageBox.warning(self, "Warning", "Please enter valid numbers for all fields!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Prediction failed: {str(e)}\nPlease train or load a model first!")