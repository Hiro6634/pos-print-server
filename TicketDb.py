from asyncio import subprocess
import os
import threading
import firebase_admin
from  firebase_admin import credentials
from firebase_admin import firestore
from ConfigHelper import ConfigHelper

config = ConfigHelper()

class TicketDb:
    def __init__(self):
        self.doc_watch = None
        cred = credentials.Certificate("ajbpos-firebase-adminsdk-ao7l2-d308d8b1bc.json")
        self.PRN = config.getTerminalId()
        firebase_admin.initialize_app(cred, {
            'projetctId': 'ajbpos'
        })

        self.db = firestore.client()
        self.callback_done = threading.Event()
        self.configcallback_done = threading.Event()

    def on_snapshot(self, doc_snapshot, changes, read_time):
        
        for doc in doc_snapshot:
            print(f'Received document snapshot: {doc.id}')
            doc_ref = self.db.collection(u'printers').document(self.PRN.upper()).collection(u'queue').document(doc.id)
            ticket = doc_ref.get()
            if ticket.exists:
                self.callbackFn( ticket.to_dict())

                printedTicket_ref = self.db.collection(u'printers').document(self.PRN.upper()).collection(u'printed').document(doc.id)
                printedTicket_ref.set(
                    ticket.to_dict()
                )
            else:
                print('No Such element')
            self.db.collection(u'printers').document(self.PRN.upper()).collection(u'queue').document(doc.id).delete()
        self.callback_done.set()

    def watchQueue(self, callbackFn):
        if self.doc_watch is not None and not config.getSimulatePrinter():
            print("trying to run Unsubscribe")
            self.doc_watch.unsubscribe()

        self.callbackFn = callbackFn
        self.PRN = config.getTerminalId()
        print("TerminalId: " + self.PRN.upper())
        doc_ref = self.db.collection(u'printers').document(self.PRN.upper()).collection(u'queue')

        self.doc_watch = doc_ref.on_snapshot(self.on_snapshot)


    def on_configSnapshot(self, doc_snapshot, changes, read_time):
        
        for doc in doc_snapshot:
            print(f'Received document snapshot: {doc.id}')
            doc_ref = self.db.collection(u'printers').document(doc.id)
            prnConfig = doc_ref.get()
            if prnConfig.exists:
                self.callbackConfigFn(prnConfig.to_dict())

        self.configcallback_done.set()

    def watchConfig(self, callbackFn):
        self.callbackConfigFn = callbackFn
        self.PRN = config.getTerminalId()
        print("TerminalId: " + self.PRN.upper())
        doc_ref = self.db.collection(u'printers').document(self.PRN.upper())

        doc_watch = doc_ref.on_snapshot(self.on_configSnapshot)
        

    def onReboot(self):
        config_ref = self.db.collection(u'printers').document(self.PRN.upper())
        config_ref.update({ 'reboot' : False})
        print("Try to reboot")
        os.system("sudo reboot")

