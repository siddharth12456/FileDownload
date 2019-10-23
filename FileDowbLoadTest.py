from FileDownload import FileDownLoad
from unittest import *


class MyTest(TestCase):

    testdata = {"fileId": "0B1fGSuBXAh1IeEpzajRISkNHckU", "destination": "D:/Master/", "filename": "file.txt"}
    testdataegative = {"fieId": "----"}

    def test_attribute(self):
        """
        This test checks that that the various attributes are intilised
        :return:
        """
        self.filedownload = FileDownLoad(self.testdata["fileId"], self.testdata['destination'], self.testdata["filename"])
        self.assertIsNotNone(self.filedownload)

    def test_timeoutSpecified(self):
        """
        This test specifies the whether the test fileDownload exits in the timeout specified.
        :return:
        """
        self.assertEqual(FileDownLoad(self.testdata["fileId"], self.testdata['destination'], self.testdata["filename"], 0.1).download_file_from_google_drive(), "Can't complete Download the execution in {} seconds".format(0.1))

    def test_timeoutSpecifiedneagtive(self):
        """
        This test specifies the whether the test fileDownload exits if the timeout specified is negative.
        :return:
        """
        self.assertEqual(FileDownLoad(self.testdata["fileId"], self.testdata['destination'], self.testdata["filename"], -1).download_file_from_google_drive(), "Can't complete Download the execution in {} seconds".format(-1))

    def test_chunksize(self):
        """
        This test specifies the whether the error message is returned when we set the chunkSize as zero.
        :return:
        """
        self.assertEqual(FileDownLoad(self.testdata["fileId"], self.testdata['destination'], self.testdata["filename"], 100, 0).download_file_from_google_drive(), "chunk size should be greater zero.")

    def test_chunksizeNegative(self):
        """
        This test specifies the whether the error message is returned when we set the chunkSize as negative.
        :return:
        """
        self.assertEqual(FileDownLoad(self.testdata["fileId"], self.testdata['destination'], self.testdata["filename"], 100, -2).download_file_from_google_drive(), "chunk size should be greater zero.")

    def test_invalidFileId(self):
        """
        This test specifies the whether file download code
        :return:
        """
        self.assertEqual(FileDownLoad(self.testdataegative["fileId"], self.testdata['destination'], self.testdata["filename"], 100, -2).download_file_from_google_drive(), "chunk size should be greater zero.")


if __name__ == "__main__":
    main()










