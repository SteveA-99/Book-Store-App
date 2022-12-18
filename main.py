from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5 import uic
import pandas as pd
from PyQt5.QtGui import QPixmap


#######################################################################
# used code from assignment 4
# credit to Mustafa Tosun
class ShowUserGui(QMainWindow):
    def __init__(self, id):
        super(ShowUserGui, self).__init__()
        uic.loadUi('show_user.ui', self)
        self.df_users = pd.read_excel('361projectBooks.xlsx', sheet_name='books')
        self.user = self.df_users.loc[self.df_users.id == id].reset_index()
        self.lbl_photo.setPixmap(QPixmap(str(self.user.photo_path[0])))
        self.lbl_photo.setFixedWidth(300)
        self.lbl_photo.setFixedHeight(300)
        self.btn_browse.clicked.connect(self.displayBrowser)
        self.show()

    def displayBrowser(self):
        msg = QMessageBox()
        msg.setText(str(self.df_users))
        msg.exec()


class UsersGui(QMainWindow):
    def __init__(self):
        super(UsersGui, self).__init__()
        uic.loadUi('users_photo.ui', self)
        # self.user_labels = []
        self.row_length = 6
        self.show()
        self.load_users_data()

    def load_users_data(self):
        # for label in self.user_labels:
        #     label.setParent(None)
        while self.layout_users.count():
            self.layout_users.itemAt(0).widget().setParent(None)
        self.df_users = pd.read_excel('361projectBooks.xlsx', sheet_name='books')
        row_index = -1
        for i in range(len(self.df_users)):
            column_index = i % self.row_length
            if column_index == 0:
                row_index += 1
            user = QLabel()
            user.setPixmap(QPixmap(self.df_users.photo_path[i]))
            user.setScaledContents(True)
            user.setFixedWidth(300)
            user.setFixedHeight(300)
            user.mousePressEvent = lambda e, id=self.df_users.id[i]: self.show_user(id)
            # self.user_labels.append(user)
            self.layout_users.addWidget(user, row_index, column_index)

    def show_user(self, id):
        self.show_user_gui = ShowUserGui(id)
        self.load_users_data()


####################################################################################
class userMenu(QMainWindow):
    def __init__(self):
        super(userMenu, self).__init__()
        self.id = 0
        uic.loadUi('usersScreen.ui', self)
        self.df = pd.read_excel('361projectUsers.xlsx', sheet_name='users')
        x = 0
        for xy in range(len(self.df)):
            self.tableWidget.setItem(x, 0, QtWidgets.QTableWidgetItem(str(self.df['username'][x])))
            self.tableWidget.setItem(x, 1, QtWidgets.QTableWidgetItem(str(self.df['password'][x])))
            x += 1
        self.addUsersButton.clicked.connect(self.add)
        self.listUsersButton.clicked.connect(self.list)
        self.updateUsersButton.clicked.connect(self.updating)
        self.deleteUsersButton.clicked.connect(self.delete)

    def display(self):
        self.show()
        self.username.setText('')
        self.password.setText('')
        self.updatedUsername.setText('')
        self.updatedPassword.setText('')

    ### add button ###
    def add(self):
        if self.username.text() == '':
            error = QMessageBox.question(self, "Error", 'You must type something!', QMessageBox.Ok)
            if error == QMessageBox.Ok:
                pass
            else:
                pass
        else:
            error = QMessageBox.question(self, "Warning", 'Are you sure you want to add?',
                                         QMessageBox.Yes | QMessageBox.No)
            if error == QMessageBox.Yes:
                self.id = self.id + 1
                i = 0
                while i != len(self.df.username):
                    if self.username.text() != self.df.username[i]:
                        i += 1
                    elif self.username.text() == self.df.username[i]:
                        error = QMessageBox()
                        error.setWindowTitle("Error")
                        error.setText("Can not add the same username!")
                        error.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                        error.exec_()
                        return

                self.df.loc[len(self.df.index)] = [self.id, self.username.text(), self.password.text()]
                self.df.to_excel('361projectUsers.xlsx', sheet_name='users', index=False)
            elif error == QMessageBox.No:
                pass

    ### list button ###
    def list(self):
        msg = QMessageBox()
        msg.setText(str(self.df))
        msg.exec()
        # listingData()

    ### update button ###
    def updating(self):
        if self.username.text() == '':
            error = QMessageBox.question(self, "Error", 'You must type something!', QMessageBox.Ok)
            if error == QMessageBox.Ok:
                pass
            else:
                pass
        else:
            error = QMessageBox.question(self, "Warning", 'Are you sure you want to update?',
                                         QMessageBox.Yes | QMessageBox.No)
            if error == QMessageBox.Yes:
                self.df.replace(to_replace=self.username.text(), value=self.updatedUsername.text(), inplace=True)
                self.df.replace(to_replace=self.password.text(), value=self.updatedPassword.text(), inplace=True)
                self.df.to_excel('361projectUsers.xlsx', sheet_name='users', index=False)
            elif error == QMessageBox.No:
                pass

    ### deleting users button ###
    def delete(self):
        if self.username.text() == '':
            error = QMessageBox.question(self, "Error", 'You must type something!', QMessageBox.Ok)
            if error == QMessageBox.Ok:
                pass
            else:
                pass
        else:
            error = QMessageBox.question(self, "Warning", 'Are you sure you want to delete?',
                                         QMessageBox.Yes | QMessageBox.No)
            if error == QMessageBox.Yes:
                self.df.drop(self.df[self.df['username'] == self.username.text()].index, inplace=True)
                self.df.to_excel('361projectUsers.xlsx', sheet_name='users', index=False)
            elif error == QMessageBox.No:
                pass


class bookMenu(QMainWindow):
    def __init__(self):
        super(bookMenu, self).__init__()
        self.photo_path = 'images/default.png'
        uic.loadUi('bookMenu.ui', self)
        self.df = pd.read_excel('361projectBooks.xlsx', sheet_name='books')
        self.id = 0
        self.addBookButton.clicked.connect(self.add)
        self.listBookButton.clicked.connect(self.list)
        self.updateBookButton.clicked.connect(self.update)
        self.deleteBookButton.clicked.connect(self.delete)

    def display(self):
        self.show()
        self.username.setText('')
        self.authorName.setText('')
        self.numberBook.setText('')
        self.priceBook.setText('')
        self.updatedUsername.setText('')
        self.updatedAuthorName.setText('')
        self.updatedNumberBook.setText('')
        self.updatedPriceBook.setText('')

    def add(self):
        if self.username.text() == '':
            error = QMessageBox.question(self, "Error", 'You must type something!', QMessageBox.Ok)
            if error == QMessageBox.Ok:
                pass
            else:
                pass
        else:
            error = QMessageBox.question(self, "Warning", 'Are you sure you want to add?',
                                         QMessageBox.Yes | QMessageBox.No)
            if error == QMessageBox.Yes:
                i = 0
                count = 0
                while i != len(self.df.name):
                    if self.username.text() != self.df.name[i]:  # if id == id -> id += 1
                        i += 1
                    else:
                        count += 1
                        if count > 2:
                            error = QMessageBox()
                            error.setWindowTitle("Error")
                            error.setText("Can not add the same book more than twice!")
                            error.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                            error.exec_()
                            return

                self.id += 1
                self.df.loc[len(self.df.index)] = [self.id, self.username.text(), self.authorName.text(),
                                                   self.numberBook.text(), self.priceBook.text(), self.photo_path]
                self.df.to_excel('361projectBooks.xlsx', sheet_name='books', index=False)
            elif error == QMessageBox.No:
                pass

    def list(self):
        """msg = QMessageBox()
        msg.setText(str(self.df))
        msg.exec()"""
        UsersGui()
        # displayBooks.show_user_gui

    def update(self):
        if self.updatedUsername.text() == '':
            error = QMessageBox.question(self, "Error", 'You must type something!', QMessageBox.Ok)
            if error == QMessageBox.Ok:
                pass
            else:
                pass
        else:
            error = QMessageBox.question(self, "Warning", 'Are you sure you want to update?',
                                         QMessageBox.Yes | QMessageBox.No)
            if error == QMessageBox.Yes:
                self.df.replace(to_replace=self.username.text(), value=self.updatedUsername.text(), inplace=True)
                self.df.replace(to_replace=self.authorName.text(), value=self.updatedAuthorName.text(), inplace=True)
                self.df.replace(to_replace=self.numberBook.text(), value=self.updatedNumberBook.text(), inplace=True)
                self.df.replace(to_replace=self.priceBook.text(), value=self.updatedPriceBook.text(), inplace=True)
                self.df.to_excel('361projectBooks.xlsx', sheet_name='books', index=False)
            elif error == QMessageBox.No:
                pass

    def delete(self):
        if self.username.text() == '':
            error = QMessageBox.question(self, "Error", 'You must type something!', QMessageBox.Ok)
            if error == QMessageBox.Ok:
                pass
            else:
                pass
        else:
            error = QMessageBox.question(self, "Warning", 'Are you sure you want to delete?',
                                         QMessageBox.Yes | QMessageBox.No)
            if error == QMessageBox.Yes:
                self.df.drop(self.df[self.df['name'] == self.username.text()].index, inplace=True)
                self.df.to_excel('361projectBooks.xlsx', sheet_name='books', index=False)
            elif error == QMessageBox.No:
                pass


class orderMenu(QMainWindow):
    def __init__(self):
        super(orderMenu, self).__init__()
        uic.loadUi('orderMenu.ui', self)
        self.id = 1
        self.df = pd.read_excel('361projectOrders.xlsx', sheet_name='orders')
        x = 0
        for xy in range(len(self.df)):
            self.tableWidget.setItem(x, 0, QtWidgets.QTableWidgetItem(str(self.df['user_id'][x])))
            self.tableWidget.setItem(x, 1, QtWidgets.QTableWidgetItem(str(self.df['customer_name'][x])))
            self.tableWidget.setItem(x, 2, QtWidgets.QTableWidgetItem(str(self.df['date'][x])))
            self.tableWidget.setItem(x, 3, QtWidgets.QTableWidgetItem(str(self.df['total_price'][x])))
            x += 1
        self.createOrderButton.clicked.connect(self.create)
        self.updateOrderButton.clicked.connect(self.update)
        self.listOrderButton.clicked.connect(self.list)
        self.cancelOrderButton.clicked.connect(self.cancel)

    def display(self):
        self.show()
        self.userID.setText('')
        self.customerName.setText('')
        self.date.setText('')
        self.totalPrice.setText('')
        self.updateUserID.setText('')
        self.updateName.setText('')
        self.updateDate.setText('')
        self.updatePrice.setText('')

    def create(self):
        if self.userID.text() == '':
            error = QMessageBox.question(self, "Error", 'You must type something!', QMessageBox.Ok)
            if error == QMessageBox.Ok:
                pass
            else:
                pass
        else:
            error = QMessageBox.question(self, "Warning", 'Are you sure you want to create?',
                                         QMessageBox.Yes | QMessageBox.No)
            if error == QMessageBox.Yes:
                self.df.loc[len(self.df.index)] = [self.df.id.max() + 1, self.userID.text(), self.customerName.text(),
                                                   self.date.text(), self.totalPrice.text()]
                self.df.to_excel('361projectOrders.xlsx', sheet_name='orders', index=False)
            elif error == QMessageBox.No:
                pass

        """i = 0
        instBook = bookMenu()
        while i != len(self.df.id):
            instBook.df.loc[instBook.df.number[i]] += 1
            i += 1
            #self.df.numberBook[i] += 1"""

    def list(self):
        msg = QMessageBox()
        msg.setText(str(self.df))
        msg.exec()

    def update(self):
        if self.updateUserID.text() == '':
            error = QMessageBox.question(self, "Error", 'You must type something!', QMessageBox.Ok)
            if error == QMessageBox.Ok:
                pass
            else:
                pass
        else:
            error = QMessageBox.question(self, "Warning", 'Are you sure you want to delete?',
                                         QMessageBox.Yes | QMessageBox.No)
            if error == QMessageBox.Yes:
                self.df.replace(to_replace=self.userID.text(), value=self.updateUserID.text(), inplace=True)
                self.df.replace(to_replace=self.customerName.text(), value=self.updateName.text(), inplace=True)
                self.df.replace(to_replace=self.date.text(), value=self.updateDate.text(), inplace=True)
                self.df.replace(to_replace=self.totalPrice.text(), value=self.updatePrice.text(), inplace=True)
                self.df.to_excel('361projectOrders.xlsx', sheet_name='orders', index=False)
            elif error == QMessageBox.No:
                pass

    def cancel(self):
        if self.customerName.text() == '':
            error = QMessageBox.question(self, "Error", 'You must type something!', QMessageBox.Ok)
            if error == QMessageBox.Ok:
                pass
            else:
                pass
        else:
            error = QMessageBox.question(self, "Warning", 'Are you sure you want to cancel?',
                                         QMessageBox.Yes | QMessageBox.No)
            if error == QMessageBox.Yes:
                self.df.drop(self.df[self.df['customer_name'] == self.customerName.text()].index, inplace=True)
                self.df.to_excel('361projectOrders.xlsx', sheet_name='orders', index=False)
            elif error == QMessageBox.No:
                pass


class mainMenu(QMainWindow):
    def __init__(self):
        super(mainMenu, self).__init__()
        uic.loadUi('361menuProject.ui', self)
        self.show()
        self.user = userMenu()
        self.book = bookMenu()
        self.order = orderMenu()
        self.userButton.clicked.connect(lambda: self.user.display())
        self.booksButton.clicked.connect(lambda: self.book.display())
        self.orderButton.clicked.connect(lambda: self.order.display())
        self.show()


class userLoginScreen(QMainWindow):
    def __init__(self):
        super(userLoginScreen, self).__init__()
        uic.loadUi('361projectLoginScreen.ui', self)
        self.show()
        self.df = pd.read_excel('361projectUsers.xlsx', sheet_name='users')
        self.enterButton.clicked.connect(self.display)
        self.cancelButton.clicked.connect(self.close)

    def display(self):
        i = 0
        self.order = orderMenu()
        self.books = bookMenu()
        while i != len(self.df.username):
            if self.userLogin.text() == 'mustafa' and self.passLogin.text() == 'isNumberOne':
                self.main = mainMenu()
                self.main.show()
                self.close()
                break
            elif self.userLogin.text() == self.df.username[i] and self.passLogin.text() == self.df.password[i]:
                choice = QMessageBox.question(self, 'Choose', 'Would you like to access order menu?',
                                              QMessageBox.Yes | QMessageBox.No)
                if choice == QMessageBox.Yes:
                    self.order.display()
                elif choice == QMessageBox.No:
                    choice = QMessageBox.question(self, 'Choose', 'Would you like to access book menu?',
                                                  QMessageBox.Yes | QMessageBox.No)
                    if choice == QMessageBox.Yes:
                        self.books.display()
                    elif choice == QMessageBox.No:
                        return
                break
            i += 1
        if i == len(self.df.username):
            error = QMessageBox()
            error.setWindowTitle("Invalid")
            error.setText("User does not exist!")
            error.exec()


app = QApplication([])
window = userLoginScreen()
app.exec()
