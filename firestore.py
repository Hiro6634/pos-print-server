import firebase_admin
from  firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("ajbpos-firebase-adminsdk-ao7l2-d308d8b1bc.json")
firebase_admin.initialize_app(cred, {
    'projetctId': 'ajbpos'
})

db = firestore.client()

doc_ref = db.collection(u'printers').document(u'PRN1')

doc = doc_ref.get()

if doc.exists:
    print(f'Document data: {doc.to.dict()}')
else:
    print('No such document')