import time
import requests
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

acceptedFileTypes = ['.mi2', '.mi3', '.mid']

# To do:
# - better response handling for jobs
# - threading for jobs
# - better handle error if server isn't available

class PointcloudPipeline():

    def ingest(self, filePath):

        print "============"
        print "INGEST POINTCLOUD: START"

        verifyFile = VerifyFile()
        job_1_result = verifyFile.pointcloud(filePath)
        if (job_1_result == 'error'):
            print "INGEST POINTCLOUD: FAILED"
            print "============"
        else:
            backendApiAdapter = BackendApiAdapter()
            job_2_result = backendApiAdapter.postFile(job_1_result)

            if (job_2_result != 'success'):
                print "INGEST POINTCLOUD: FAILED"
                print "============"

            else:
                print "INGEST POINTCLOUD: SUCCESS"
                print "============"

class BackendApiAdapter():

    def postFile(self, filePath):

        print "opening file..."
        with open(filePath, 'rb') as f:
            print "file opened"
            print "posting file..."
            r = requests.post('http://localhost:3000/pointcloud', files={filePath: f})
            if (r.status_code == 200):
                print "success"
                return "success"

            else:
                print "failed: error code %s " % r.status_code
                return r.status_code

class VerifyFile():

    def pointcloud(self, filePath):
        print "------------"
        print "pointcloud verification start" 
        print "file path: %s " % filePath

        filename, file_extension = os.path.splitext(filePath)
        print "file name: %s" % filename
        print "file extension: %s" % file_extension

        isfileValidated = False

        for acceptedFileType in acceptedFileTypes:
            if file_extension == acceptedFileType:
                isfileValidated = True

        if isfileValidated == True:
            print "pointcloud validation: success"
            return filePath

        else:
            print "------------"
            print "pointcloud validation error 'wrong file type'"
            print "received file type" 
            print file_extension
            print "accepted file types"
            print(', '.join(acceptedFileTypes))
            return 'error'

class Watcher:
    DIRECTORY_TO_WATCH = "watched"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print "Error"

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print "Received created event - %s." % event.src_path

            pointcloudPipeline = PointcloudPipeline()
            pointcloudPipeline.ingest(event.src_path)

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            print "Received modified event - %s." % event.src_path

if __name__ == '__main__':
    w = Watcher()
    w.run()