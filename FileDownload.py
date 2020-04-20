import requests
import time
import logging
from threading import *
import os


class FileDownLoad(object):
    """
    This class Downloads the file form the Google drive to the local Disk.
    """
    url = "https://docs.google.com/uc?export=download"

    def __init__(self, fileid, destination, filename, timeout=100, chunkSize = 3278):
        """
        :param id: File id of the file in drive
        :param destination: local folder on which the file will be save
        :param filename:
        :param timeout:
        :param chunkSize: The chunks of
        """
        self.id = fileid
        self.destination = destination
        self.session = requests.session()
        self.filename = filename
        self.timeout = timeout
        self.chunkSize = chunkSize
        log_format = "%(asctime)s::%(message)s"
        logging.basicConfig(level='WARN', format=log_format)
        self.startime = time.time()
        self.endtime = None
        self.rLock = Lock()
        self.deleteFile()
        self.filestartime = None
        self.tokentime = time.clock()


    def deleteFile(self):
        try:
            if os.path.exists(self.destination+self.filename):
                os.remove(self.destination + self.filename)
                #logging.info("existing file deleted .")
                
        except Exception:
            logging.error("File Cant be deleted .")
            raise Exception
        

    @property
    def downloadTime(self):
        """
        :return: File download time in seconds
        """
        return self.endtime - self.filestartime

    @property
    def downloadSpeed(self):
        """
        :return: return download speed in bytes/sec
        """
        return (os.path.getsize(self.destination + self.filename)/1000)/self.downloadTime

    
    @property
    def token(self):
        """
        :return: JWT
        """
        while time.clock() - self.tokentime < 10:
            try:
                response = self.session.get(self.url, params={'id':self.id}, stream=True)
                for key, value in response.cookies.items():
                    if key.startswith('download_warning'):
                        logging.info("Generated  the JWT token.")
                        self.tokentime = time.clock()
                        return value
                logging.warning("JWT token is not generated.")
                return None
            except Exception as e:
                logging.error("JWT token is not generated.")
                raise Exception("No token generated.")


    def download_file_from_google_drive(self):
        """This function stores the file form the drive to the local drive
        :return:
        """
        if self.session:
            try:
                params = {'id': self.id, 'confirm': self.token}
                response = self.session.get(self.url, params = params, stream = True)
                with self.rLock:
                    if self.chunkSize > 0:
                        if os.path.exists(self.destination):
                            with open(self.destination + self.filename, "wb") as f:
                                self.filestartime = time.time()
                                logging.warning("File Download in progress.")
                                for chunk in response.iter_content(self.chunkSize):
                                    if time.time() - self.filestartime <= self.timeout:
                                        f.write(chunk)
                                    else:
                                        f.close()
                                        self.deleteFile()
                                        logging.error("Can't complete Download the execution in {} seconds".format(self.timeout))
                                        return "Can't complete Download the execution in {} seconds".format(self.timeout)
                        else:
                            logging.error("Destination File Path doesn't exists")
                            return "Destination File Path doesn't exists ."
                    else:
                        logging.warning("chunk size should be greater zero .")
                        return "chunk size should be greater zero"
                    self.endtime = time.time()
                    f.close()
                    logging.info("File downloaded in {} seconds with kbps speed in  as {}".format(self.downloadTime, self.downloadSpeed))
            except Exception as e:
                logging.warning("download_file_from_google_drive caused exception".format(str(e)))
            finally:
                self.session.close()
        else:
            logging.error("The session has not been created .")
            return "The session has not been created."

