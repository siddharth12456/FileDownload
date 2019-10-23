import requests
import os
import time
import logging


class FileDownLoad(object):
    """
    This class Downlaods the file form the Google to the local Disk.
    """
    url = "https://docs.google.com/uc?export=download"

    def __init__(self, id, destination, filename, timeout=10, chunkSize=3278):
        """
        :param id: File id of the file in drive
        :param destination: local folder on which the file will be save
        :param filename:
        :param timeout:
        :param chunkSize: The chunks of
        """
        self.id = id
        self.destination = destination
        self.session = requests.session()
        self.filename = filename
        self.timeout = timeout
        self.chunkSize = chunkSize
        log_format = "%(asctime)s::%(message)s"
        logging.basicConfig(level='INFO', format=log_format)
        self.startime = None
        self.endtime = None

    @property
    def downloadTime(self):
        """
        :return: File download time in secs
        """
        return self.endtime - self.startime

    @property
    def downloadSpeed(self):
        """
        :return: return download speed in bytes/sec
        """
        return os.path.getsize(self.destination + self.filename)/self.downloadTime

    @property
    def token(self):
        """
        :return: JWT  token for authentication
        """
        try:
            response = self.session.get(self.url, params={'id':self.id}, stream=True)
            for key, value in response.cookies.items():
                if key.startswith('download_warning'):
                    logging.info("Generated  the JWT token.")
                    return value
            logging.warning("JWT token is not generated.")
            return None
        except Exception as e:
            logging.error("JWT token is not generated.")
            raise Exception("No token genrated.")

    def download_file_from_google_drive(self):
        """This function stores the file form the drive to the local drive
        :return:
        """
        if self.session:
            try:
                params = {'id': self.id, 'confirm': self.token}
                response = self.session.get(self.url, params = params, stream = True)
                self.chunkSize = 10000000
                if self.chunkSize > 0:
                    if os.path.exists(self.destination):
                        with open(self.destination+self.filename, "wb") as f:
                            self.startime = int(time.time())
                            logging.warning("File Download in progress.")
                            for chunk in response.iter_content(self.chunkSize):
                                if int(time.time()) - self.startime <= self.timeout:
                                    f.write(chunk)
                                else:
                                    logging.error("Can't complete Download the execution in {} seconds".format(self.timeout))
                                    return "Can't complete Download the execution in {} seconds".format(self.timeout)
                    else:
                        logging.error("Destination File Path doesn't exists")
                        return "Destination File Path doesn't exists"
                else:
                    logging.warning("chunk size should be greater zero")
                    return "chunk size should be greater zero"
                self.endtime = int(time.time())
                logging.info("File downloaded in {} seconds with bps speed as {}".format(self.downloadTime, self.downloadSpeed))
            except Exception as e:
                logging.warning("download_file_from_google_drive caused exception".format(str(e)))
        else:
            logging.error("The session has not been created")
            return "The session has not been created"


a = FileDownLoad("0B1fGSuBXAh1IeEpzajRISkNHckU", "D:/Master/", "file.txt")
a.download_file_from_google_drive()

