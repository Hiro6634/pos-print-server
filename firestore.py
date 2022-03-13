from gc import callbacks
import threading
from tracemalloc import Snapshot
import firebase_admin
from  firebase_admin import credentials
from firebase_admin import firestore
import time

class MyDb:
    def __init__(self):
        cred = credentials.Certificate("ajbpos-firebase-adminsdk-ao7l2-d308d8b1bc.json")
        firebase_admin.initialize_app(cred, {
            'projetctId': 'ajbpos'
        })

        self.db = firestore.client()
        self.callback_done = threading.Event()

    def getDoc(self):
        doc_ref = self.db.collection(u'printers').document(u'PRN1')

        doc = doc_ref.get()

        if doc.exists:
            print(f'Document data: {doc.to_dict()}')
        else:
            print('No such document')


    def on_snapshot(self, doc_snapshot, changes, read_time):
        
        for doc in doc_snapshot:
            print(f'Received document snapshot: {doc.id}')
            doc_ref = self.db.collection(u'printers').document(u'PRN1').collection(u'queue').document(doc.id)

            ticket = doc_ref.get()
            if ticket.exists:
                print('Ticket Data: ',ticket.to_dict())

                printedTicket_ref = self.db.collection(u'printers').document(u'PRN1').collection(u'printed').document(doc.id)
                printedTicket_ref.set(
                    ticket.to_dict()
                )
            else:
                print('No Such element')
            self.db.collection(u'printers').document(u'PRN1').collection(u'queue').document(doc.id).delete()
        self.callback_done.set()

    def watchDoc(self):
        doc_ref = self.db.collection(u'printers').document(u'PRN1').collection(u'queue')

        doc_watch = doc_ref.on_snapshot(self.on_snapshot)

def getDocument():

    cred = credentials.Certificate("ajbpos-firebase-adminsdk-ao7l2-d308d8b1bc.json")
    firebase_admin.initialize_app(cred, {
        'projetctId': 'ajbpos'
    })

    db = firestore.client()

    doc_ref = db.collection(u'printers').document(u'PRN1')

    doc = doc_ref.get()

    if doc.exists:
        print(f'Document data: {doc.to_dict()}')
    else:
        print('No such document')


def main():
    db = MyDb()

    #db.getDoc()
    db.watchDoc()

    while(True):
        pass

if __name__ == '__main__':
    main()