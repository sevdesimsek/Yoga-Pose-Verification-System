import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sqlite3
import os
import torch
from torchvision import transforms
from PIL import Image, ExifTags
from CNNmodel import YogaPoseCNN

basedir = os.path.dirname(__file__)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Yoga Pose Verification System"
        self.model = YogaPoseCNN(num_classes=5)
        model_path = os.path.join('userDatabase', 'yoga_pose_model.pth')
        self.model.load_state_dict(torch.load(model_path))
        self.model.eval()

        self.classes = [
            'Down dog Pose', 'Goddes Pose', 'Plank Pose', 'Tree Pose',
            'Warrior Pose'
        ]

        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.title)
        self.setStyleSheet("QMainWindow {border-image: url(guiPhotos/bg (3).jpg) 0 0 0 0 stretch stretch;}")

        buttonWindow1 = QPushButton('Sign Up', self)
        buttonWindowDoc = QPushButton('Login', self)
        buttonGuide = QPushButton('Guide', self)

        buttonWindow1.setCursor(QCursor(Qt.PointingHandCursor))
        buttonWindow1.setStyleSheet(self.button_style())
        buttonWindow1.setGeometry(550, 650, 250, 150)  # butonun ekrandaki yeri

        buttonWindowDoc.setCursor(QCursor(Qt.PointingHandCursor))
        buttonWindowDoc.setStyleSheet(self.button_style())
        buttonWindowDoc.setGeometry(950, 650, 250, 150)

        buttonGuide.setCursor(QCursor(Qt.PointingHandCursor))
        buttonGuide.setStyleSheet(self.button_style())
        buttonGuide.setGeometry(750, 850, 250, 150)  # butonun ekrandaki yeri

        l4 = QLabel(self)
        l4.setPixmap(QPixmap(os.path.join(basedir, "guiPhotos/logo1.png")))
        l4.setGeometry(300, 150, 500, 243)

        l5 = QLabel(self)
        l5.setPixmap(QPixmap(os.path.join(basedir, "guiPhotos/logo- (2).png")))
        l5.setGeometry(600, 170, 500, 243)

        l6 = QLabel(self)
        l6.setPixmap(QPixmap(os.path.join(basedir, "guiPhotos/logo- (1).png")))
        l6.setGeometry(900, 100, 500, 400)

        buttonWindow1.clicked.connect(self.signup_onClick)
        buttonWindowDoc.clicked.connect(self.login_onClick)
        buttonGuide.clicked.connect(self.buttonGuide_onClick)  # basılıp o sayfaya gidilmesini sağlıyor

        self.showMaximized()

    def button_style(self):
        return (
            "*{border: 4px solid '#9c532f';"
            "border-radius: 70px;"
            "font-size: 20px;"
            "color: 'black';"
            "padding: 10px 0;}"
            "*:hover{background: '#9c532f';}"
        )

    @pyqtSlot()
    def signup_onClick(self):
        self.statusBar().showMessage("Switched to Sign Up")
        self.cams = SignupPage(self.model, self.classes)
        self.cams.show()
        self.close()

    @pyqtSlot()
    def login_onClick(self):
        self.statusBar().showMessage("Switched to Log In")
        self.cams = LoginPage(self.model, self.classes)
        self.cams.show()
        self.close()

    @pyqtSlot()
    def buttonGuide_onClick(self):
        self.statusBar().showMessage("Switched to Guide")
        self.cams = GuidePage()
        self.cams.show()
        self.close()

class GuidePage(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: #ce966b")
        self.setWindowTitle('Guide Page')
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_FileDialogInfoView))

        self.header = QLabel("How to Use the App", self)
        self.header.setStyleSheet("font-size: 45px;")
        self.header.setGeometry(600, 50, 600, 100)

        self.guide_text = QLabel(self)
        self.guide_text.setText(
            "Welcome to the Yoga Pose Verification System!\n\n"
            "guide yazıcak"
        )
        self.guide_text.setStyleSheet("font-size: 20px; padding: 20px;")
        self.guide_text.setGeometry(100, 150, 1600, 800)
        self.guide_text.setWordWrap(True)

        self.backbutton = QPushButton(self)
        self.backbutton.setStyleSheet(self.back_button_style())
        self.backbutton.setFixedSize(100, 100)
        self.backbutton.clicked.connect(self.goMainWindow)

        self.showMaximized()

    def back_button_style(self):
        return (
            "*{border: 2px solid '#9c532f';"
            "border-radius: 50px;"
            "border-image: url(guiPhotos/back tuşu.png);}"
            "*:hover{background: '#ce966b';}"
        )

    def goMainWindow(self):
        self.cams = Window()
        self.cams.showMaximized()
        self.close()

class SignupPage(QDialog):
    def __init__(self, model, classes, parent=None):
        super().__init__(parent)
        self.model = model
        self.classes = classes
        self.setStyleSheet("background: #e0aa8f")
        self.setWindowTitle('Sign Up Page')
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_FileDialogInfoView))

        self.header = QLabel("Sign Up", self)
        self.header.setStyleSheet("font-size: 45px;")
        self.header.setGeometry(600, 50, 400, 100)

        self.username = QLabel("Please enter your username", self)
        self.password = QLabel("Please enter your password", self)
        self.role = QLabel("Please enter your role (student/instructor)", self)
        self.username.setStyleSheet("font-size: 20px;")
        self.password.setStyleSheet("font-size: 20px;")
        self.role.setStyleSheet("font-size: 20px;")
        self.username.setGeometry(450, 430, 245, 100)
        self.password.setGeometry(800, 430, 245, 100)
        self.role.setGeometry(1150, 430, 245, 100)

        self.lineEdit_password = QLineEdit(self)
        self.lineEdit_username = QLineEdit(self)
        self.lineEdit_role = QLineEdit(self)
        self.lineEdit_username.setPlaceholderText('     username')
        self.lineEdit_password.setPlaceholderText('     password')
        self.lineEdit_role.setPlaceholderText('     student/instructor')
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        self.lineEdit_password.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.lineEdit_username.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.lineEdit_role.setAttribute(Qt.WA_MacShowFocusRect, 0)

        self.lineEdit_username.setGeometry(430, 500, 300, 100)
        self.lineEdit_username.setStyleSheet(self.input_style())
        self.lineEdit_password.setGeometry(780, 500, 300, 100)
        self.lineEdit_password.setStyleSheet(self.input_style())
        self.lineEdit_role.setGeometry(1130, 500, 300, 100)
        self.lineEdit_role.setStyleSheet(self.input_style())

        self.createAccount = QPushButton(self)
        self.createAccount.setText('Sign Up')
        self.createAccount.setStyleSheet(self.button_style())
        self.createAccount.setGeometry(800, 650, 250, 150)

        self.backbutton = QPushButton(self)
        self.backbutton.setStyleSheet(self.back_button_style())
        self.backbutton.setFixedSize(100, 100)
        self.backbutton.setGeometry(10, 10, 100, 100)
        self.error = QLabel("", self)
        self.error.setGeometry(800, 800, 300, 30)
        self.error.setStyleSheet("color: 'red';")

        self.backbutton.clicked.connect(self.goMainWindow)
        self.createAccount.clicked.connect(self.createAccountFunction)
        self.showMaximized()

    def button_style(self):
        return (
            "*{border: 4px solid '#9c532f';"
            "border-radius: 70px;"
            "font-size: 20px;"
            "color: 'black';"
            "padding: 10px 0;}"
            "*:hover{background: '#9c532f';}"
        )

    def back_button_style(self):
        return (
            "*{border: 2px solid '#9c532f';"
            "border-radius: 50px;"
            "border-image: url(guiPhotos/back tuşu.png);}"
            "*:hover{background: '#9c532f';}"
        )

    def input_style(self):
        return (
            "*{border: 4px solid '#9c532f';"
            "border-radius: 70px;"
            "font-size: 20px;"
            "color: 'black';"
            "padding: 10px 0;}"
            "*:hover{background: '#9c532f';}"
        )

    def createAccountFunction(self):
        user = self.lineEdit_username.text()
        password = self.lineEdit_password.text()
        role = self.lineEdit_role.text()

        if not user or not password or role not in ['student', 'instructor']:
            self.error.setText("Please fill in all inputs correctly.")
            return

        conn = sqlite3.connect('userDatabase/yoga_pose_verification.db')
        cur = conn.cursor()
        try:
            query1 = "SELECT * FROM users WHERE username=?"
            cur.execute(query1, (user,))
            result = cur.fetchone()
            if result:
                self.error.setText("Existing user. Please choose another username.")
            else:
                query2 = "INSERT INTO users (username, password, role) VALUES (?, ?, ?)"
                cur.execute(query2, (user, password, role))
                conn.commit()
                self.error.setText("User is created. You can log in.")
        finally:
            conn.close()

    def goMainWindow(self):
        self.cams = Window()
        self.cams.showMaximized()
        self.close()

class LoginPage(QDialog):
    def __init__(self, model, classes, parent=None):
        super().__init__(parent)
        self.model = model
        self.classes = classes
        self.setStyleSheet("background: #ce966b")
        self.setWindowTitle('Log In Page')
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_FileDialogInfoView))

        self.header = QLabel("Log In", self)
        self.header.setStyleSheet("font-size: 45px;")
        self.header.setGeometry(600, 50, 400, 100)

        self.username = QLabel("Please enter your username", self)
        self.password = QLabel("Please enter your password", self)
        self.username.setStyleSheet("font-size: 20px;")
        self.password.setStyleSheet("font-size: 20px;")
        self.username.setGeometry(450, 430, 245, 100)
        self.password.setGeometry(800, 430, 245, 100)

        self.lineEdit_password = QLineEdit(self)
        self.lineEdit_username = QLineEdit(self)
        self.lineEdit_username.setPlaceholderText('     username')
        self.lineEdit_password.setPlaceholderText('     password')
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        self.lineEdit_password.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.lineEdit_username.setAttribute(Qt.WA_MacShowFocusRect, 0)

        self.lineEdit_username.setGeometry(430, 500, 300, 100)
        self.lineEdit_username.setStyleSheet(self.input_style())
        self.lineEdit_password.setGeometry(780, 500, 300, 100)
        self.lineEdit_password.setStyleSheet(self.input_style())

        self.logInButton = QPushButton(self)
        self.logInButton.setStyleSheet('background-color: rgb(0,0,255); color: #fff')
        self.logInButton.setText('Log In')
        self.logInButton.setStyleSheet(self.button_style())
        self.logInButton.setGeometry(800, 650, 250, 150)

        self.backbutton = QPushButton(self)
        self.backbutton.setStyleSheet(self.back_button_style())
        self.backbutton.setFixedSize(100, 100)
        self.backbutton.setGeometry(10, 10, 100, 100)
        self.error = QLabel("", self)
        self.error.setGeometry(800, 800, 300, 30)
        self.error.setStyleSheet("color: 'red';")

        self.backbutton.clicked.connect(self.goMainWindow)
        self.logInButton.clicked.connect(self.logInFunction)
        self.showMaximized()

    def button_style(self):
        return (
            "*{border: 4px solid '#9c532f';"
            "border-radius: 70px;"
            "font-size: 20px;"
            "color: 'black';"
            "padding: 10px 0;}"
            "*:hover{background: '#9c532f';}"
        )

    def back_button_style(self):
        return (
            "*{border: 2px solid '#9c532f';"
            "border-radius: 50px;"
            "border-image: url(guiPhotos/back tuşu.png);}"
            "*:hover{background: '#9c532f';}"
        )

    def input_style(self):
        return (
            "*{border: 4px solid '#9c532f';"
            "border-radius: 70px;"
            "font-size: 20px;"
            "color: 'black';"
            "padding: 10px 0;}"
            "*:hover{background: '#9c532f';}"
        )

    def logInFunction(self):
        user = self.lineEdit_username.text()
        password = self.lineEdit_password.text()

        if not user or not password:
            self.error.setText("Please fill in all inputs.")
            return

        conn = sqlite3.connect('userDatabase/yoga_pose_verification.db')
        cur = conn.cursor()
        query = "SELECT role FROM users WHERE username=? AND password=?"
        cur.execute(query, (user, password))
        result = cur.fetchone()
        conn.close()

        if result:
            role = result[0]
            if role == 'student':
                self.cams = StudentWindow(self.model, self.classes)
            else:
                self.cams = InstructorWindow(self.model, self.classes)
            self.cams.show()
            self.close()
        else:
            self.error.setText("Invalid username or password.")

    def goMainWindow(self):
        self.cams = Window()
        self.cams.showMaximized()
        self.close()

class InstructorWindow(QDialog):
    def __init__(self, model, classes, parent=None):
        super().__init__(parent)
        self.imagePath = ""
        self.setStyleSheet("background: #ce966b")
        self.setWindowTitle('Instructor Page')
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_FileDialogInfoView))
        self.model = model
        self.classes = classes

        self.database_path = os.path.join(basedir, 'userDatabase/yoga_pose_verification.db')
        self.InitUI()
        self.readBlobData()

    def InitUI(self):
        self.button = QPushButton(self)
        self.button.setStyleSheet(self.back_button_style())
        self.button.setFixedSize(100, 100)

        self.button.clicked.connect(self.goMainWindow)

        self.imageTable = QTableWidget(self)
        self.imageTable.setColumnCount(3)
        self.imageTable.setRowCount(100)
        self.imageTable.setGeometry(200, 100, 1000, 600)
        self.imageTable.setHorizontalHeaderLabels(['Username', 'Pose', 'Prediction'])
        self.imageTable.setColumnWidth(0, 200)
        self.imageTable.setColumnWidth(1, 300)
        self.imageTable.setColumnWidth(2, 300)

        self.imprevlabel = QLabel("Image preview", self)
        self.imprevlabel.setGeometry(1230, 100, 300, 200)
        self.imprevlabel.setStyleSheet("font-size: 30px;")
        self.imLabel = QLabel("", self)
        self.imLabel.setGeometry(1200, 300, 224, 224)

        self.showMaximized()

    def button_style(self):
        return (
            "*{border: 4px solid '#9c532f';"
            "border-radius: 45px;"
            "font-size: 28px;"
            "color: 'white';"
            "padding: 25px 0;}"
            "*:hover{background: '#9c532f';}"
        )

    def back_button_style(self):
        return (
            "*{border: 2px solid '#9c532f';"
            "border-radius: 50px;"
            "border-image: url(guiPhotos/back tuşu.png);}"
            "*:hover{background: '#9c532f';}"
        )

    def readBlobData(self):
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            query = """SELECT users.username, images.image, images.predictionResult 
                       FROM images JOIN users ON images.userID = users.id"""
            cursor.execute(query)
            record = cursor.fetchall()
            rowCount = 0
            icon_size = QSize(224, 224)
            for row in record:
                username = row[0]
                im = row[1]
                predRes = row[2]
                saveLike = 'data' + str(rowCount) + '.jpg'
                imagPat = 'uploadeddata/' + saveLike
                with open(imagPat, 'wb') as f:
                    f.write(im)

                pixmap = QPixmap()
                pixmap.loadFromData(im)
                imgButton = QPushButton()
                imgButton.setObjectName(imagPat)
                imgButton.setVisible(False)
                icon = QIcon(pixmap.scaled(icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                imgButton.setIcon(icon)
                self.imageTable.setItem(rowCount, 0, QTableWidgetItem(username))
                self.imageTable.item(rowCount, 0).setFlags(Qt.ItemIsEnabled)
                self.imageTable.setCellWidget(rowCount, 1, imgButton)
                self.imageTable.setItem(rowCount, 2, QTableWidgetItem(str(predRes)))
                self.imageTable.item(rowCount, 2).setFlags(Qt.ItemIsEnabled)
                imgButton.clicked.connect(self.imagee)
                rowCount += 1

            cursor.close()
        except sqlite3.Error as error:
            print("Failed.")
        finally:
            if conn:
                conn.close()

    def imagee(self):
        button = self.sender()
        imagPat = button.objectName()
        pixmap = QPixmap(imagPat)
        pixmap = pixmap.scaled(224, 224, Qt.KeepAspectRatio)
        self.imLabel.setPixmap(QPixmap(pixmap))

    def goMainWindow(self):
        self.cams = Window()
        self.cams.showMaximized()
        self.close()

class StudentWindow(QDialog):
    def __init__(self, model, classes, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: #ce966b")
        self.setWindowTitle('Student Page')
        self.model = model
        self.classes = classes
        self.imagePath = ''
        self.error = QLabel(" ", self)
        self.error.setGeometry(500, 600, 300, 30)
        self.error.setStyleSheet("color: 'red'; font-size: 20px;")

        self.InitUI()

    def InitUI(self):
        self.backbutton = QPushButton(self)
        self.backbutton.setStyleSheet(self.back_button_style())
        self.backbutton.setFixedSize(100, 100)
        self.statusBar = QStatusBar(self)
        self.statusBar.setGeometry(0, 750, 200, 100)

        warningl = QLabel(self)
        warningl.setPixmap(QPixmap(os.path.join(basedir, "guiPhotos/warningl.png")))
        warningl.setGeometry(20, 250, 400, 400)

        self.predButton = QPushButton(self)
        self.predButton.setText('Your Feedback')
        self.predButton.setStyleSheet(self.button_style())
        self.predButton.setGeometry(750, 650, 250, 150)

        self.resultL = QLabel("Result", self)
        self.resultL.setGeometry(1050, 250, 300, 100)
        self.resultL.setStyleSheet("font-size: 50px;")

        self.resultLabel = QLabel("", self)
        self.resultLabel.setStyleSheet("font-size: 35px;")
        self.resultLabel.setGeometry(1050, 370, 200, 100)

        self.imButton = QPushButton(self)
        self.imButton.setText('Upload Your Pose')
        self.imButton.setStyleSheet(self.button_style())
        self.imButton.setGeometry(450, 650, 250, 150)
        self.imButton.clicked.connect(self.getImagePath)
        self.predButton.clicked.connect(self.getPrediction)

        self.backbutton.clicked.connect(self.goMainWindow)
        self.imLabel = QLabel("", self)
        self.imLabel.setGeometry(400, 100, 500, 500)
        self.imagel = QLabel("Pose Preview Page", self)
        self.imagel.setGeometry(500, 0, 350, 100)
        self.imagel.setStyleSheet("font-size: 50px;")

        self.showMaximized()

    def button_style(self):
        return (
            "*{border: 4px solid '#9c532f';"
            "border-radius: 70px;"
            "font-size: 20px;"
            "color: 'black';"
            "padding: 10px 0;}"
            "*:hover{background: '#9c532f';}"
        )

    def back_button_style(self):
        return (
            "*{border: 2px solid '#9c532f';"
            "border-radius: 50px;"
            "border-image: url(guiPhotos/back tuşu.png);}"
            "*:hover{background: '#9c532f';}"
        )

    def getImagePath(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Image files (*.jpg)")
        imagePathh = fname[0]

        if imagePathh:
            image = Image.open(imagePathh)
            try:
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                exif = dict(image._getexif().items())

                if exif[orientation] == 3:
                    image = image.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    image = image.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    image = image.rotate(90, expand=True)
            except (AttributeError, KeyError, IndexError):
                # cases: image don't have getexif
                pass

            image.save("temp.jpg")
            pixmap = QPixmap("temp.jpg")
            pixmap = pixmap.scaled(500, 500, Qt.KeepAspectRatio)
            self.imLabel.setPixmap(QPixmap(pixmap))
            self.imagePath = "temp.jpg"
        else:
            self.error.setText("Image not selected.")

    def getPrediction(self):
        transformer = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
        ])

        if self.imagePath:
            try:
                image = Image.open(self.imagePath)
                image_tensor = transformer(image).float()
                image_tensor = image_tensor.unsqueeze_(0)
                input = torch.autograd.Variable(image_tensor)
                output = self.model(input)
                index = output.data.numpy().argmax()
                pred = self.classes[index]
                self.resultLabel.setText(pred)
                self.saveResult(pred)
            except Exception as e:
                self.error.setText(f"Error during prediction: {str(e)}")
        else:
            self.error.setText("Please select image.")

    def saveResult(self, prediction):
        conn = sqlite3.connect('userDatabase/yoga_pose_verification.db')
        cur = conn.cursor()
        try:
            query = "INSERT INTO images (userID, predictionResult, image) VALUES ((SELECT id FROM users WHERE username=?), ?, ?)"
            with open(self.imagePath, "rb") as image:
                cur.execute(query, (username, prediction, sqlite3.Binary(image.read())))
            conn.commit()
        finally:
            conn.close()

    def goMainWindow(self):
        self.cams = Window()
        self.cams.showMaximized()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
