I. File list
------------
FileDownload.py
FileDownloadTest.py

Program functionality.
The file FileDownload.py  This python module  downloads the file from the google drive with fileID and save to the local drive.it also
lists the download time and the download speed it can be used in multi threading envoirment also.



Steps to RUN the tests are :
python FileDownLoadTest.py

This will run the following  tests
here are basic description of the test.

Basic tests

test_timeoutSpecified -------->This test case verifies that file download exits in the timeout specified with correct error message.

test_timeoutSpecifiedneagtive------->This test code verifies that exits in the negative timeout specified with correct message.

test_chunksize---------------->This test verifies that whether the error message is returned when we set the chunkSize as zero.

test_chunksizeNegative--------> This test verifies that whether the error message is returned when we set the chunkSize as negative.

test_invalidFileId------------> This test verifies that  whether FileDownLoad raises an exception if the fileId is invalid.

test_invalidDestination------->This test case verifies that the error message for invalid file destination.

test_sessionnotCreated--------->This test case verifies that the error message if the rest session is not created.


Functional scenarios:
test_checkFileSize ------------>  The test case verifies that complete file is downloded i.e the file size on drive should be same as downloded .

test_fileDowndThread ------------> This test case verifies that that FileDownLoad class should be thread safe ie the there should be no dead lock
if the same file is downloaded by two threads and  file size should be same as that on drive.

test_downloadspeed ---> This test verifies that downloadSpeed field is not None after complete download of file.

test_downloadtime------------->This test verifies that downloadTime field is not None after complete download of file.

test_downloadMultipleFiles----->This test verifies that we can download multiple types of files with FileDownload.py

test not performed due to lack of data
Downlaod a large size file

python packages required for download
requests











I

















