from FileDownload import FileDownLoad
import unittest
import os




class MyTest(unittest.TestCase):
    #testdata = {", "destination": ".", "filename": "file.txt"}
    testdata = {"fileId": "0B1fGSuBXAh1IeEpzajRISkNHckU", "filesize": 45688229, "destination": "../", "filename": "file.txt","fileId2": "0BzGLzkYTf9Oya19INmpNVXk5SmM2QnBXRnNmbWNfcGNQNndN","filesize2":50045}
    testdataegative = {"fileId": "----", "destination":" "}

    def test_timeoutSpecified(self):
        """
        The test code  exits in the timeout specified with correct error message
        :return:
        """
        self.assertEqual(FileDownLoad(self.testdata["fileId2"], self.testdata['destination'], self.testdata["filename"], 0.0001).download_file_from_google_drive(), "Can't complete Download the execution in {} seconds".format(0.0001))

    def test_timeoutSpecifiedneagtive(self):
        """
        The test code  exits in the negative timeout specified with correct message
        :return:
        """
        self.assertEqual(FileDownLoad(self.testdata["fileId"], self.testdata['destination'], self.testdata["filename"], -1).download_file_from_google_drive(), "Can't complete Download the execution in {} seconds".format(-1))

    def test_chunksize(self):
        """
        This test specifies the whether the error message is returned when we set the chunkSize as zero.
        :return:
        """
        self.assertEqual(FileDownLoad(self.testdata["fileId"], self.testdata['destination'], self.testdata["filename"], 100, 0).download_file_from_google_drive(), "chunk size should be greater zero")

    def test_chunksizeNegative(self):
        """
        This test specifies the whether the error message is returned when we set the chunkSize as negative.
        :return:
        """
        self.assertEqual(FileDownLoad(self.testdata["fileId"], self.testdata['destination'], self.testdata["filename"], 100, -2).download_file_from_google_drive(), "chunk size should be greater zero")

    def test_invalidFileId(self):
        """
        This test verifies whether FileDownLoad raises an exception if the fileId is invalid
        :return:
        """
        try:
            self.assertEqual(FileDownLoad(self.testdataegative["fileId"], self.testdata['destination'], self.testdata["filename"], 100, -2).download_file_from_google_drive())
        except:
            self.assertRaises(Exception)

    def test_invalidDestination(self):
        """
        This test case verifies the error messege for invalid file destination.
        :return:
        """
        self.assertEqual(FileDownLoad(self.testdata["fileId"], self.testdataegative['destination'], self.testdata["filename"], 100, 100).download_file_from_google_drive(), "Destination File Path doesn't exists .")

    def test_sessionnotCreated(self):
        """
        This test case verifies the error messege if the rest session is not created.
        :return:
        """
        a = FileDownLoad(self.testdata["fileId"], self.testdataegative['destination'], self.testdata["filename"], 100, 100)
        a.session = None
        self.assertEqual(a.download_file_from_google_drive(), "The session has not been created.")

    def test_checkFileSize(self):
        """
        The test case verifies that complete file is downloded i.e the file size on drive should be same as downloded .
        :return:
        """
        import os
        filesize = self.testdata['filesize2']
        a = FileDownLoad(self.testdata["fileId2"], self.testdata['destination'], self.testdata["filename"])
        a.download_file_from_google_drive()
        self.assertEqual(os.path.getsize(a.destination+a.filename), filesize)

    def test_fileDowndThread(self):
        """
         Test for The FileDownLoad class should be thread safe ie the same file should be downloaded by two thread there should  be no dead lock
         and there should be no data corruption.
        :return:
        """
        import threading
        filesize = self.testdata['filesize2']
        a = FileDownLoad(self.testdata["fileId2"], self.testdata['destination'], self.testdata["filename"])
        threading.Thread(a.download_file_from_google_drive()).start()
        threading.Thread(a.download_file_from_google_drive()).start()
        self.assertEqual(os.path.getsize(a.destination+a.filename), filesize)

    def test_downloadspeed(self):
        """
        This[ test verifies that downloadSpeed field is not None after complete download of file
        :return:
        """
        a = FileDownLoad(self.testdata["fileId2"], self.testdata['destination'], self.testdata["filename"])
        a.download_file_from_google_drive()
        self.assertIsNotNone(a.downloadSpeed)

    def test_downloadtime(self):
        """[
        This test verifies that downloadTime field is not None after complete download of file,
        :return:
        """
        a = FileDownLoad(self.testdata["fileId2"], self.testdata['destination'], self.testdata["filename"])
        a.download_file_from_google_drive()
        self.assertIsNotNone(a.downloadTime)

    def test_downloadMultipleFiles(self):
        """
        This test verifies that we can download multi types of files with FileDownload.py
        :return:
        """
        filesize = self.testdata['filesize2']
        a = FileDownLoad(self.testdata["fileId2"], self.testdata['destination'], self.testdata["filename"])
        a.download_file_from_google_drive()
        self.assertEqual(os.path.getsize(a.destination + a.filename), filesize)
        a.id = self.testdata["fileId"]
        a.download_file_from_google_drive()
        filesize = self.testdata['filesize']
        self.assertEqual(os.path.getsize(a.destination + a.filename), filesize)


if __name__ == "__main__":
    unittest.main()










