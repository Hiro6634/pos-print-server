import threading
import firebase_admin
from  firebase_admin import credentials
from firebase_admin import firestore

class FirestoreDb:
    # def __init__(self):
    #     self.cred = credentials.Certificate("ajbpos-firebase-adminsdk-ao7l2-d308d8b1bc.json")
    #     firebase_admin.initialize_app(self.cred, {
    #         'projetctId': 'ajbpos'
    #     })

    #     self.db = firestore.client()
    
    def getDocTest(self):
        self.doc_ref = self.db.collection(u'printers').document(u'PRN1')

        self.doc = self.doc_ref.get()

        if self.doc.exists:
            print(f'Document data: {self.doc.to_dict()}')
        else:
            print('No such document')
    
    def getDocTestMonolitic(self):
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
    
#callback_done = threading.Event()

#cred = credentials.Certificate("ajbpos-firebase-adminsdk-ao7l2-d308d8b1bc.json")
#firebase_admin.initialize_app(cred, {
#    'projetctId': 'ajbpos'
#})

#db = firestore.client()

#def on_snapshot(doc_snapshot, changes, read_time):
#    for doc in doc_snapshot:
#        print(f'Received Document Snapshot: {doc.id}')
#    callback_done.set()

#doc_ref = db.collection(u'printers').document(u'PRN1')

#doc_watch = doc_ref.on_snapshot(on_snapshot)

#def main():
#    GetDocumentTest()
#    pass

#def GetDocumentTest():

def onSnapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        print('Received document snapshot: ' + doc.id)

cred = credentials.Certificate("ajbpos-firebase-adminsdk-ao7l2-d308d8b1bc.json")
firebase_admin.initialize_app(cred, {
    'projetctId': 'ajbpos'
})

db = firestore.client()
doc_ref = db.collection(u'printers').document(u'PRN1').collection('queue')

doc = doc_ref.on_snapshot(onSnapshot)

while True:
    pass
'''
if doc.exists:
    print(f'Document data: {doc.to_dict()}')
else:
    print('No such document')
'''
# def main2():
#     firestore = FirestoreDb()
#     firestore.getDocTestMonolitic()

# if __name__ == '__main__':
#     main()