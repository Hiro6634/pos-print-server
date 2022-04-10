from time import sleep
import firebase_admin
from  firebase_admin import credentials
from firebase_admin import firestore
import threading

class emergencia:
    def __init__(self):
        cred = credentials.Certificate("ajbpos-firebase-adminsdk-ao7l2-d308d8b1bc.json")
        firebase_admin.initialize_app(cred, {
            'projetctId': 'ajbpos'
        })
        self.db = firestore.client()
        self.callback_done = threading.Event()

    def on_snapshot(self, doc_snapshot, changes, read_time):
        print("BINGO Hay algo")

    def watchQueue(self, callbackFn):
        self.callbackFn = callbackFn
        self.PRN = "PRN2"

        doc_ref = self.db.collection(u'printers').document(self.PRN).collection(u'queue')
        doc_watch = doc_ref.on_snapshot(self.on_snapshot)


def processJobs():
    pass

if __name__ == '__main__':
    processor = emergencia()

    processor.watchQueue(processJobs)

    while True:
        sleep(1)