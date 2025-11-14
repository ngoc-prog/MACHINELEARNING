import random
from random import random
import plotly.graph_objects as go

from PyQt6 import QtGui, QtCore
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon, QPixmap
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QMainWindow, QDialog, QComboBox, QPushButton, QCheckBox, \
    QListWidgetItem, QFileDialog
from matplotlib import pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import traceback

import matplotlib

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import random

from MLBAProject.Models.PurchaseLinearRegression import PurchaseLinearRegression
from MLBAProject.UI.ChartHandle import ChartHandle
from MLBAProject.UI.DatabaseConnectEx import DatabaseConnectEx
from MLBAProject.UI.MainWindow import Ui_MainWindow


class MainWindowEx(Ui_MainWindow):
    def __init__(self):
        self.purchaseLinearRegression = PurchaseLinearRegression()
        self.databaseConnectEx=DatabaseConnectEx()
        self.databaseConnectEx.parent=self
        self.chartHandle= ChartHandle()
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
        self.verticalLayoutFunctions.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setupPlot()

        self.actionConnection.triggered.connect(self.openDatabaseConnectUI)

        self.pushButtonPurchaseRatesByGender.clicked.connect(self.showPurchaseRatesByGender)
        self.pushButtonSalesFlucuationsByYearAndMonth.clicked.connect(self.showSalesFlucuationsByYearAndMonth)
        self.pushButtonPurchaseCountingByCategory.clicked.connect(self.showPurchaseCountingByCategory)
        self.pushButtonPurchaseRatesByAgeGroup.clicked.connect(self.showPurchaseRatesByAgeGroup)
        self.pushButtonPurchaseCountingByCategory.clicked.connect(self.showPurchaseCountingByCategory)
        self.pushButtonPurchaseValueByCategory.clicked.connect(self.showPurchaseValueByCategory)
        self.pushButtonPurchaseByCategoryAndGender.clicked.connect(self.showPurchaseByCategoryAndGender)
        self.pushButtonPaymentMethod.clicked.connect(self.showPaymentMethod)
        self.pushButtonPurchaseRatesByShoppingMall.clicked.connect(self.showPurchaseRatesByShoppingMall)
        self.pushButtonProductSpendingByGender.clicked.connect(self.showProductSpendingByGender)
        self.pushButtonPurchaseFrequenceByAge.clicked.connect(self.showShowPurchaseFrequenceByAge)
        self.pushButtonSalesFluctuationsByMonth.clicked.connect(self.showpushButtonSalesFluctuationsByMonth)
        self.checkEnableWidget(False)

        self.pushButtonTrainModel.clicked.connect(self.processTrainModel)
        self.pushButtonEvaluate.clicked.connect(self.processEvaluateTrainedModel)
        self.pushButtonSavePath.clicked.connect(self.processPickSavePath)
        self.pushButtonSaveModel.clicked.connect(self.processSaveTrainedModel)
        self.pushButtonLoadModel.clicked.connect(self.processLoadTrainedModel)
        self.pushButtonPredict.clicked.connect(self.processPrediction)

        # Disable Evaluate button initially
        self.pushButtonEvaluate.setEnabled(False)

    def setupPlot(self):
        self.figure = plt.figure(figsize=(15, 5))
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self.MainWindow)
        self.verticalLayoutChart.addWidget(self.toolbar)
        self.verticalLayoutChart.addWidget(self.canvas)

    def openDatabaseConnectUI(self):
        self.databaseConnectEx.setupUi(QMainWindow())
        self.databaseConnectEx.show()

    def checkEnableWidget(self,isEnable):
        self.pushButtonPurchaseRatesByGender.setEnabled(isEnable)
        self.pushButtonPurchaseRatesByAgeGroup.setEnabled(isEnable)
        self.pushButtonPurchaseCountingByCategory.setEnabled(isEnable)
        self.pushButtonPurchaseValueByCategory.setEnabled(isEnable)
        self.pushButtonPurchaseByCategoryAndGender.setEnabled(isEnable)
        self.pushButtonPaymentMethod.setEnabled(isEnable)
        self.pushButtonPurchaseRatesByShoppingMall.setEnabled(isEnable)
        self.pushButtonProductSpendingByGender.setEnabled(isEnable)
        self.pushButtonPurchaseFrequenceByAge.setEnabled(isEnable)
        self.pushButtonSalesFluctuationsByMonth.setEnabled(isEnable)
        self.pushButtonSalesFlucuationsByYearAndMonth.setEnabled(isEnable)

        self.pushButtonTrainModel.setEnabled(isEnable)
        self.pushButtonEvaluate.setEnabled(isEnable)
        self.pushButtonSavePath.setEnabled(isEnable)
        self.pushButtonSaveModel.setEnabled(isEnable)
        self.pushButtonLoadModel.setEnabled(isEnable)
        self.pushButtonPredict.setEnabled(isEnable)

    def showPurchaseRatesByGender(self):
        self.purchaseLinearRegression.connector = self.databaseConnectEx.connector
        dfGender = self.purchaseLinearRegression.processGenderDistribution()
        self.chartHandle.visualizePieChart(self.figure, self.canvas, dfGender, "gender", "count", "Gender Distribution")

        self.tableWidgetStatistic.setRowCount(0)
        self.tableWidgetStatistic.setRowCount(len(dfGender))
        for row in range(len(dfGender)):
            self.tableWidgetStatistic.setItem(row, 0, QTableWidgetItem(str(dfGender.iloc[row]["gender"])))
            self.tableWidgetStatistic.setItem(row, 1, QTableWidgetItem(str(dfGender.iloc[row]["count"])))

    def showSalesFlucuationsByYearAndMonth(self):
        self.purchaseLinearRegression.connector = self.databaseConnectEx.connector
        dfMonthlyAndYearSalesAmount = self.purchaseLinearRegression.processMonthlyAndYearSalesAmount()
        self.chartHandle.visualizeLinePlotChart(self.figure, self.canvas, dfMonthlyAndYearSalesAmount, "month", "sales_amount", "Monthly Variation in Sales Amount Over Years", hue="year", xticks=True)

        self.tableWidgetStatistic.setRowCount(0)
        self.tableWidgetStatistic.setRowCount(len(dfMonthlyAndYearSalesAmount))
        for row in range(len(dfMonthlyAndYearSalesAmount)):
            self.tableWidgetStatistic.setItem(row, 0, QTableWidgetItem(str(dfMonthlyAndYearSalesAmount.iloc[row]["year"])))
            self.tableWidgetStatistic.setItem(row, 1, QTableWidgetItem(str(dfMonthlyAndYearSalesAmount.iloc[row]["month"])))
            self.tableWidgetStatistic.setItem(row, 2, QTableWidgetItem(str(dfMonthlyAndYearSalesAmount.iloc[row]["sales_amount"])))

    def showPurchaseCountingByCategory(self):
        self.purchaseLinearRegression.connector = self.databaseConnectEx.connector
        dfCategory = self.purchaseLinearRegression.processCategoryDistribution()
        self.chartHandle.visualizePieChart(self.figure, self.canvas, dfCategory, "category", "count", "Categories Distribution", legend=False)

        self.tableWidgetStatistic.setRowCount(0)
        self.tableWidgetStatistic.setRowCount(len(dfCategory))
        for row in range(len(dfCategory)):
            self.tableWidgetStatistic.setItem(row, 0, QTableWidgetItem(str(dfCategory.iloc[row]["category"])))
            self.tableWidgetStatistic.setItem(row, 1, QTableWidgetItem(str(dfCategory.iloc[row]["count"])))

    def showPurchaseRatesByAgeGroup(self):
        self.purchaseLinearRegression.connector = self.databaseConnectEx.connector
        fromAge = int(self.lineEditFromAge.text())
        toAge = int(self.lineEditToAge.text())
        dfAges = self.purchaseLinearRegression.processAgeDistribution(fromAge, toAge)
        self.chartHandle.visualizeBarChart(self.figure, self.canvas, dfAges, "age", "count", "Age Distribution %s~%s" % (fromAge, toAge))

        self.tableWidgetStatistic.setRowCount(0)
        self.tableWidgetStatistic.setRowCount(len(dfAges))
        for row in range(len(dfAges)):
            self.tableWidgetStatistic.setItem(row, 0, QTableWidgetItem(str(dfAges.iloc[row]["age"])))
            self.tableWidgetStatistic.setItem(row, 1, QTableWidgetItem(str(dfAges.iloc[row]["count"])))

    def showPurchaseValueByCategory(self):
        self.purchaseLinearRegression.connector = self.databaseConnectEx.connector
        dfCateSpending = self.purchaseLinearRegression.processCategorySpending()
        self.chartHandle.visualizeBarChart(self.figure, self.canvas, dfCateSpending, "category", "price", "Distribution category and Spending")

        self.tableWidgetStatistic.setRowCount(0)
        self.tableWidgetStatistic.setRowCount(len(dfCateSpending))
        for row in range(len(dfCateSpending)):
            self.tableWidgetStatistic.setItem(row, 0, QTableWidgetItem(str(dfCateSpending.iloc[row]["category"])))
            self.tableWidgetStatistic.setItem(row, 1, QTableWidgetItem(str(dfCateSpending.iloc[row]["price"])))

    def showPurchaseByCategoryAndGender(self):
        self.purchaseLinearRegression.connector = self.databaseConnectEx.connector
        dfGenderCategory = self.purchaseLinearRegression.processGenderAndCategoryCounter()
        self.chartHandle.visualizeMultiBarChart(self.figure, self.canvas, self.purchaseLinearRegression.df, "category", "count", "gender", "Distribution gender and category")

        self.tableWidgetStatistic.setRowCount(0)
        self.tableWidgetStatistic.setRowCount(len(dfGenderCategory))
        for row in range(len(dfGenderCategory)):
            self.tableWidgetStatistic.setItem(row, 0, QTableWidgetItem(str(dfGenderCategory.iloc[row]["gender"])))
            self.tableWidgetStatistic.setItem(row, 1, QTableWidgetItem(str(dfGenderCategory.iloc[row]["category"])))
            self.tableWidgetStatistic.setItem(row, 2, QTableWidgetItem(str(dfGenderCategory.iloc[row]["count"])))

    def showPaymentMethod(self):
        self.purchaseLinearRegression.connector = self.databaseConnectEx.connector
        dfPayment = self.purchaseLinearRegression.processPaymentMethod()
        self.chartHandle.visualizePieChart(self.figure, self.canvas, dfPayment, "payment_method", "count", "Payment Distribution", legend=False)

        self.tableWidgetStatistic.setRowCount(0)
        self.tableWidgetStatistic.setRowCount(len(dfPayment))
        for row in range(len(dfPayment)):
            self.tableWidgetStatistic.setItem(row, 0, QTableWidgetItem(str(dfPayment.iloc[row]["payment_method"])))
            self.tableWidgetStatistic.setItem(row, 1, QTableWidgetItem(str(dfPayment.iloc[row]["count"])))

    def showPurchaseRatesByShoppingMall(self):
        self.purchaseLinearRegression.connector = self.databaseConnectEx.connector
        dfShoppingMall = self.purchaseLinearRegression.processShoppingMall()
        self.chartHandle.visualizePieChart(self.figure, self.canvas, dfShoppingMall, "shopping_mall", "count", "Shopping Mall Distribution", legend=False)

        self.tableWidgetStatistic.setRowCount(0)
        self.tableWidgetStatistic.setRowCount(len(dfShoppingMall))
        for row in range(len(dfShoppingMall)):
            self.tableWidgetStatistic.setItem(row, 0, QTableWidgetItem(str(dfShoppingMall.iloc[row]["shopping_mall"])))
            self.tableWidgetStatistic.setItem(row, 1, QTableWidgetItem(str(dfShoppingMall.iloc[row]["count"])))

    def showProductSpendingByGender(self):
        self.purchaseLinearRegression.connector = self.databaseConnectEx.connector
        dfGenderCateSpending = self.purchaseLinearRegression.processGenderCategorySpending()
        self.chartHandle.visualizeBarPlot(self.figure, self.canvas, dfGenderCateSpending, "category", "price", "gender", "Male and Female category Total Price Spend")

        self.tableWidgetStatistic.setRowCount(0)
        self.tableWidgetStatistic.setRowCount(len(dfGenderCateSpending))
        for row in range(len(dfGenderCateSpending)):
            self.tableWidgetStatistic.setItem(row, 0, QTableWidgetItem(str(dfGenderCateSpending.iloc[row]["gender"])))
            self.tableWidgetStatistic.setItem(row, 1, QTableWidgetItem(str(dfGenderCateSpending.iloc[row]["category"])))
            self.tableWidgetStatistic.setItem(row, 2, QTableWidgetItem(str(dfGenderCateSpending.iloc[row]["price"])))

    def showShowPurchaseFrequenceByAge(self):
        self.purchaseLinearRegression.connector = self.databaseConnectEx.connector
        dfAgeGender = self.purchaseLinearRegression.processAgeOrderFrequence()
        self.chartHandle.visualizeScatterPlot(self.figure, self.canvas, dfAgeGender, "age", "count", "Age VS Order Frequence")

        self.tableWidgetStatistic.setRowCount(0)
        self.tableWidgetStatistic.setRowCount(len(dfAgeGender))
        for row in range(len(dfAgeGender)):
            self.tableWidgetStatistic.setItem(row, 0, QTableWidgetItem(str(dfAgeGender.iloc[row]["age"])))
            self.tableWidgetStatistic.setItem(row, 1, QTableWidgetItem(str(dfAgeGender.iloc[row]["count"])))

    def showpushButtonSalesFluctuationsByMonth(self):
        self.purchaseLinearRegression.connector = self.databaseConnectEx.connector
        dfMonthlySalesAmount = self.purchaseLinearRegression.processMonthlySalesAmount()
        self.chartHandle.visualizeLinePlotChart(self.figure, self.canvas, dfMonthlySalesAmount, "month", "sales_amount", "Monthly Variation in Sales Amount", xticks=True)

        self.tableWidgetStatistic.setRowCount(0)
        self.tableWidgetStatistic.setRowCount(len(dfMonthlySalesAmount))
        for row in range(len(dfMonthlySalesAmount)):
            self.tableWidgetStatistic.setItem(row, 0, QTableWidgetItem(str(dfMonthlySalesAmount.iloc[row]["month"])))
            self.tableWidgetStatistic.setItem(row, 1, QTableWidgetItem(str(dfMonthlySalesAmount.iloc[row]["sales_amount"])))

    def processTrainModel(self):
        try:
            columns_input = ["gender", "age"]
            if self.checkBoxPaymentMethod.isChecked():
                columns_input.append("payment_method")
            column_target = "price"
            test_size = int(self.lineEditTestSize.text()) / 100
            random_state = int(self.lineEditRandomState.text())
            self.purchaseLinearRegression.connector = self.databaseConnectEx.connector
            self.purchaseLinearRegression.processTrain(
                columns_input,
                column_target,
                test_size,
                random_state)
            dlg = QMessageBox(self.MainWindow)
            dlg.setWindowTitle("Info")
            dlg.setIcon(QMessageBox.Icon.Information)
            dlg.setText("Train machine learning model successful!")
            buttons = QMessageBox.StandardButton.Yes
            dlg.setStandardButtons(buttons)
            button = dlg.exec()

            # Enable Evaluate button after successful train
            self.pushButtonEvaluate.setEnabled(True)
        except Exception as e:
            traceback.print_exc()
            dlg = QMessageBox(self.MainWindow)
            dlg.setWindowTitle("Lỗi")
            dlg.setIcon(QMessageBox.Icon.Warning)
            dlg.setText(f"Train thất bại: {str(e)}")
            dlg.exec()

    def processEvaluateTrainedModel(self):
        try:
            # Kiểm tra nếu model đã train chưa
            if not hasattr(self.purchaseLinearRegression, 'model') or self.purchaseLinearRegression.model is None:
                raise ValueError("Model chưa được train. Hãy bấm 'Train Model' trước!")

            result = self.purchaseLinearRegression.evaluate()
            self.lineEditMAE.setText(str(result.MAE))
            self.lineEditMSE.setText(str(result.MSE))
            self.lineEditRMSE.setText(str(result.RMSE))
            self.lineEditR2SCore.setText(str(result.R2_SCORE))
        except Exception as e:
            traceback.print_exc()  # In lỗi ra console để debug
            dlg = QMessageBox(self.MainWindow)
            dlg.setWindowTitle("Lỗi")
            dlg.setIcon(QMessageBox.Icon.Warning)
            dlg.setText(f"Không thể evaluate model: {str(e)}\nHãy kiểm tra lại dữ liệu hoặc train model trước.")
            dlg.exec()

    def processPickSavePath(self):
        filters = "trained model file (*.zip);;All files(*)"
        filename, selected_filter = QFileDialog.getSaveFileName(
            self.MainWindow,
            filter=filters,
        )
        self.lineEditPath.setText(filename)

    def processSaveTrainedModel(self):
        trainedModelPath=self.lineEditPath.text()
        if trainedModelPath=="":
            return
        ret = self.purchaseLinearRegression.saveModel(trainedModelPath)
        dlg = QMessageBox(self.MainWindow)
        dlg.setWindowTitle("Info")
        dlg.setIcon(QMessageBox.Icon.Information)
        dlg.setText(f"Saved Trained machine learning model successful at [{trainedModelPath}]!")
        buttons = QMessageBox.StandardButton.Yes
        dlg.setStandardButtons(buttons)
        button = dlg.exec()

    def processLoadTrainedModel(self):
        # setup for QFileDialog
        filters = "trained model file (*.zip);;All files(*)"
        filename, selected_filter = QFileDialog.getOpenFileName(
            self.MainWindow,
            filter=filters,
        )
        if filename=="":
            return
        self.lineEditLocationLoadTrainedModel.setText(filename)
        self.purchaseLinearRegression.loadModel(filename)
        dlg = QMessageBox(self.MainWindow)
        dlg.setWindowTitle("Info")
        dlg.setIcon(QMessageBox.Icon.Information)
        dlg.setText(f"Load Trained machine learning model successful from [{filename}]!")
        buttons = QMessageBox.StandardButton.Yes
        dlg.setStandardButtons(buttons)
        button = dlg.exec()

        # Enable Evaluate after load (if needed)
        self.pushButtonEvaluate.setEnabled(True)

    def processPrediction(self):
        gender = self.lineEditGender.text()
        age = int(self.lineEditAge.text())
        payment = self.lineEditPaymentMethod.text()
        if len(self.purchaseLinearRegression.trainedmodel.columns_input)==3:
            predicted_price = self.purchaseLinearRegression.predictPriceFromGenderAndAgeAndPayment(gender, age, payment)
        else:
            predicted_price = self.purchaseLinearRegression.predictPriceFromGenderAndAge(gender, age)
        self.lineEditPredictedPrice.setText(str(predicted_price[0]))