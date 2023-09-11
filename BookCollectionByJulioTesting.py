from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidSessionIdException
import unittest
import time

capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='emulator-5554',
    appPackage='com.salugan.todolist',
    appActivity='com.salugan.todolist.ui.activity.splash.SplashActivity',
    appWaitForLaunch = "false"
)

appium_server_url = 'http://localhost:4723'

class TestAppium(unittest.TestCase):
    
    def setUp(self) -> None:
        self.driver = webdriver.Remote(appium_server_url, capabilities)
        self.bookData1 = ["https://kognisia.co/wp-content/uploads/2017/04/1795191_35b54ca3-b77f-46dc-aeba-5a64d6c5bf7c.jpg", 
                     "Harry Potter : The Chamber of Secrets", 
                     "J.K. Rowling", 
                     "2003", 
                     "Fiksi"]

        self.editedBookData1 = ["https://www.bookstation.ie/wp-content/uploads/2019/06/Harry-Potter-25-Year.jpg", 
                     "Harry Potter : Prisoner of Azkaban", 
                     "J.K. Rowling", 
                     "2010", 
                     "Fiksi"]
        self.bookData2 = ["https://kognisia.co/wp-content/uploads/2017/04/1795191_35b54ca3-b77f-46dc-aeba-5a64d6c5bf7c.jpg", 
                     "Pulang", 
                     "Tere Liye", 
                     "2015", 
                     "Fiksi"]
        self.bookData3 = ["https://kognisia.co/wp-content/uploads/2017/04/1795191_35b54ca3-b77f-46dc-aeba-5a64d6c5bf7c.jpg", 
                     "Testing Crash Book", 
                     "Usman", 
                     "2147483649", 
                     "Nonfiksi"]

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def test_Case1(self) -> None:
        self.driver.implicitly_wait(10)
        print("Test Case tambah satu buku")
        try :
            nodata = self.driver.find_element(MobileBy.ID, "com.salugan.todolist:id/textView")
            if (nodata.is_displayed()):
                print("Berhasil masuk ke menu")
        except:
            self.driver.implicitly_wait(10)
            print("Buku telah ada sebelumnya dan berhasil masuk ke menu")
        
        addBookButton = self.driver.find_element(MobileBy.ID, 'com.salugan.todolist:id/fab')
        addBookButton.click()
        time.sleep(1)
        okButton = self.driver.find_element(MobileBy.ID, "android:id/button1")

        bookElements = [(MobileBy.ID, "com.salugan.todolist:id/edtCover"),
                       (MobileBy.ID, "com.salugan.todolist:id/edtJudul"),
                       (MobileBy.ID, "com.salugan.todolist:id/edtNamaPenulis"),
                       (MobileBy.ID, "com.salugan.todolist:id/edtTahun"),
                       (MobileBy.ID, "com.salugan.todolist:id/edtKategori")]

#          memasukkan data ke dalam form
        for i, data in enumerate(self.bookData1):
            input_element = self.driver.find_element(*bookElements[i])
            input_element.send_keys(data)
            time.sleep(0.1)

#       mengeklik ok /save button
        okButton = self.driver.find_element(MobileBy.ID, "android:id/button1")
        okButton.click()
        time.sleep(2)

# mengecek apabila text no data masih ada, jika tidak maka buku berhasil ditambahkan
        try:
            if nodata.is_displayed():
                print("Buku gagal ditambahkan")
                print(30*"=")
        except:
            print("Buku berhasil ditambahkan")
            print(30*"=")

    def test_Case2(self) -> None:
        self.driver.implicitly_wait(10)
        print("\nTest Case Edit Buku")
        # validate if book in collections
        try:
            bookChecker = None
            bookChecker = self.driver.find_element(MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.salugan.todolist:id/rvTodoList")')
            if bookChecker is not None:
                print("Buku telah divalidasi dan telah ditambahkan sebelumnya")
                time.sleep(0.5)
        except NoSuchElementException:           
            print("Tidak ada buku yang ditambahkan sebelumnya")
        
        book1 = bookChecker.find_elements(MobileBy.CLASS_NAME, "android.widget.FrameLayout")[0]
        book1.click()
        time.sleep(1)

        # menampung current value dari text view detail book
        oldValue = []
        oldValue.append(self.driver.find_element(MobileBy.ID, "com.salugan.todolist:id/tvJudul").text)
        oldValue.append(self.driver.find_element(MobileBy.ID, "com.salugan.todolist:id/tvNamaPenulisDt").text)
        oldValue.append(self.driver.find_element(MobileBy.ID, "com.salugan.todolist:id/tvTahun").text)
        oldValue.append(self.driver.find_element(MobileBy.ID, "com.salugan.todolist:id/tvKategori").text)
        
        bookEditButton = self.driver.find_element(MobileBy.ID, "com.salugan.todolist:id/btnUpdate")
        bookEditButton.click()
        time.sleep(0.5)
        
        # validation variable declare
        bookCover = self.driver.find_element(MobileBy.ID, "com.salugan.todolist:id/edtCover")
        bookAuthor = self.driver.find_element(MobileBy.ID, "com.salugan.todolist:id/edtNamaPenulis")
        bookElements = [(MobileBy.ID, "com.salugan.todolist:id/edtCover"),
                       (MobileBy.ID, "com.salugan.todolist:id/edtJudul"),
                       (MobileBy.ID, "com.salugan.todolist:id/edtNamaPenulis"),
                       (MobileBy.ID, "com.salugan.todolist:id/edtTahun"),
                       (MobileBy.ID, "com.salugan.todolist:id/edtKategori")]
        try: 
            if(bookCover and bookAuthor is not None):   
                print("Value sebelumnya berhasil di deteksi")
                for i, data in enumerate(self.editedBookData1):
                    input_element = self.driver.find_element(*bookElements[i])
                    input_element.clear()
                    input_element.send_keys(data)
                    time.sleep(0.1)
                okButton = self.driver.find_element(MobileBy.ID, "android:id/button1")
                okButton.click()
                time.sleep(2)
        except :
            print("Credential book salah/tidak sesuai")

        try:
            currentEdited = []
            counter = 0
            currentEdited.append(self.driver.find_element(MobileBy.ID, "com.salugan.todolist:id/tvJudul").text)
            currentEdited.append(self.driver.find_element(MobileBy.ID, "com.salugan.todolist:id/tvNamaPenulisDt").text)
            currentEdited.append(self.driver.find_element(MobileBy.ID, "com.salugan.todolist:id/tvTahun").text)
            currentEdited.append(self.driver.find_element(MobileBy.ID, "com.salugan.todolist:id/tvKategori").text)
            for i,j,k in zip(currentEdited,oldValue,range(len(oldValue))) :
                if i != j:
                    print(f"value indeks list ke-{k} tidak sama")
                    counter += 1
                else:
                    print(f"value indeks ke-{k} sama")
        except:
            print("Buku gagal diedit")
        finally:
            if counter > 0 :
                print("Buku berhasil diedit\n")
                print(30*"=")
            else:
                print("Buku tidak diedit / tetap")
                print(30*"=")

    def test_Case3(self) -> None:
        self.driver.implicitly_wait(10)
        print("\nTest Case Delete Satu Buku")
        try:
            bookChecker = None
            bookChecker = self.driver.find_element(MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.salugan.todolist:id/rvTodoList")')
            if bookChecker is not None:
                print("Buku telah divalidasi dan telah ditambahkan sebelumnya")
                time.sleep(0.5)
        except NoSuchElementException:           
            print("Tidak ada buku yang ditambahkan sebelumnya")
            print(30*"=")
        
        book1 = bookChecker.find_elements(MobileBy.CLASS_NAME, "android.widget.FrameLayout")[0]
        book1.click()
        time.sleep(1)
        
        try:
            currentBookDetails = []
            currentBookDetails.append(self.driver.find_element(MobileBy.ID, "com.salugan.todolist:id/tvJudul").text)
            currentBookDetails.append(self.driver.find_element(MobileBy.ID, "com.salugan.todolist:id/tvNamaPenulisDt").text)
            currentBookDetails.append(self.driver.find_element(MobileBy.ID, "com.salugan.todolist:id/tvTahun").text)
            currentBookDetails.append(self.driver.find_element(MobileBy.ID, "com.salugan.todolist:id/tvKategori").text)
            if currentBookDetails != 0:
                deleteButton = self.driver.find_element(MobileBy.ID,"com.salugan.todolist:id/btnDelete")
                deleteButton.click()
                time.sleep(0.3)
                confirmDeleteButton = self.driver.find_element(MobileBy.ID, "android:id/button1")
                confirmDeleteButton.click()
                time.sleep(1)
        except:
            print("Buku tidak tersedia")
            print(30*"=")
        finally:
            nodata = self.driver.find_element(MobileBy.ID, "com.salugan.todolist:id/textView").is_displayed
            if nodata != True:
                print("Buku berhasil dihapus")
                print(30*"=")

    def test_case4(self)-> None:
        self.driver.implicitly_wait(10)
        print("Test Case tambah satu buku invalid tahun terbit")
        
        try :
            nodata = self.driver.find_element(MobileBy.ID, "com.salugan.todolist:id/textView")
            if (nodata.is_displayed()):
                print("Berhasil masuk ke menu")
        except:
            self.driver.implicitly_wait(10)
            print("Buku telah ada sebelumnya dan berhasil masuk ke menu")
        
        addBookButton = self.driver.find_element(MobileBy.ID, 'com.salugan.todolist:id/fab')
        addBookButton.click()
        time.sleep(1)
        okButton = self.driver.find_element(MobileBy.ID, "android:id/button1")

        bookElements = [(MobileBy.ID, "com.salugan.todolist:id/edtCover"),
                       (MobileBy.ID, "com.salugan.todolist:id/edtJudul"),
                       (MobileBy.ID, "com.salugan.todolist:id/edtNamaPenulis"),
                       (MobileBy.ID, "com.salugan.todolist:id/edtTahun"),
                       (MobileBy.ID, "com.salugan.todolist:id/edtKategori")]

#          memasukkan data ke dalam form
        for i, data in enumerate(self.bookData3):
            input_element = self.driver.find_element(*bookElements[i])
            input_element.send_keys(data)
            time.sleep(0.1)

#       mengeklik ok /save button
#       mengecek terjadinya crash
        try:
            okButton = self.driver.find_element(MobileBy.ID, "android:id/button1")
            okButton.click()
            time.sleep(0.5)
            if InvalidSessionIdException :
                print("Aplikasi telah berhenti/crash")
                pass
        except InvalidSessionIdException as e:
            print(f"Aplikasi telah berhenti/crash dikarekanakan\n{e}")

if __name__ == '__main__':
    unittest.main()