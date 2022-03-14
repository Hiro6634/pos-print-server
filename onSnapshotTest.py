import threading
import firebase_admin
from  firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("ajbpos-firebase-adminsdk-ao7l2-d308d8b1bc.json")
firebase_admin.initialize_app(cred, {
    'projetctId': 'ajbpos'
})

db = firestore.client()


# Create an Event for notifying main thread.
callback_done = threading.Event()

# Create a callback on_snapshot function to capture changes
def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        print(f'Received document snapshot: {doc.id}')
    callback_done.set()

doc_ref = db.collection(u'printers').document(u'PRN1')

# Watch the document
doc_watch = doc_ref.on_snapshot(on_snapshot)