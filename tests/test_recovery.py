import json
import sqlite3
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from recovery import RecoveryKernel

class Receiver(BaseHTTPRequestHandler):
    def log_message(self, *args): pass
    def _reply(self, status, payload):
        data=json.dumps(payload).encode()
        self.send_response(status)
        self.send_header('Content-Type','application/json')
        self.send_header('Content-Length',str(len(data)))
        self.end_headers()
        self.wfile.write(data)
    def do_POST(self):
        if self.path!='/deliver': return self._reply(404,{})
        item=json.loads(self.rfile.read(int(self.headers['Content-Length'])).decode())
        eid,mode=item.get('event_id'),item.get('mode')
        if not eid: return self._reply(400,{'error':'event_id required'})
        with self.server.lock:
            if mode=='unauthorized': return self._reply(401,{'error':'forbidden'})
            if mode=='no_receipt': return self._reply(200,{'accepted':True})
            if mode=='invalid_schema': return self._reply(400,{'error':'schema mismatch'})
            if mode=='unavailable_once' and eid not in self.server.fail_seen:
                self.server.fail_seen.add(eid)
                return self._reply(503,{'error':'temporarily unavailable'})
            with sqlite3.connect(self.server.receipts_db) as db:
                db.execute('INSERT OR IGNORE INTO receipts(event_id) VALUES(?)',(eid,))
        return self._reply(200,{'accepted':True})
    def do_GET(self):
        if not self.path.startswith('/receipts/'): return self._reply(404,{})
        eid=self.path[len('/receipts/'):]
        with sqlite3.connect(self.server.receipts_db) as db:
            count=db.execute('SELECT COUNT(*) FROM receipts WHERE event_id=?',(eid,)).fetchone()[0]
        return self._reply(200,{'event_id':eid,'committed':bool(count)}) if count else self._reply(404,{'error':'not found'})

class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        root=Path(self.tmp.name)
        self.receiver_db=str(root/'downstream.sqlite')
        self.ledger=str(root/'ledger.sqlite')
        with sqlite3.connect(self.receiver_db) as db:
            db.execute('CREATE TABLE receipts (event_id TEXT PRIMARY KEY)')
        self.server=ThreadingHTTPServer(('127.0.0.1',0), Receiver)
        self.server.receipts_db=self.receiver_db
        self.server.fail_seen=set()
        self.server.lock=threading.RLock()
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True)
        self.thread.start()
        self.base=f'http://127.0.0.1:{self.server.server_address[1]}'
    def tearDown(self):
        self.server.shutdown();self.server.server_close();self.thread.join(timeout=2);self.tmp.cleanup()
    def count(self):
        with sqlite3.connect(self.receiver_db) as db:
            return db.execute('SELECT COUNT(*) FROM receipts').fetchone()[0]
    def test_transient_failure_recovers_and_verifies(self):
        k=RecoveryKernel(self.ledger,self.base)
        s=k.recover('order-1',mode='unavailable_once')
        self.assertEqual(s['status'],'COMPLETED')
        self.assertEqual(s['attempts'],2)
        self.assertEqual(self.count(),1)
    def test_unauthorized_refuses_action(self):
        k=RecoveryKernel(self.ledger,self.base)
        self.assertEqual(k.recover('order-2','unauthorized')['status'],'REVIEW_REQUIRED')
        self.assertEqual(self.count(),0)
    def test_schema_mismatch_blocks(self):
        k=RecoveryKernel(self.ledger,self.base)
        self.assertEqual(k.recover('order-3','invalid_schema')['status'],'BLOCKED')
        self.assertEqual(self.count(),0)
    def test_accepted_without_receipt_is_not_completion(self):
        k=RecoveryKernel(self.ledger,self.base)
        self.assertEqual(k.recover('order-5','no_receipt')['status'],'UNVERIFIED')
        self.assertEqual(self.count(),0)

    def test_exhausted_retries_remain_recoverable_not_falsely_complete(self):
        k=RecoveryKernel(self.ledger,self.base)
        self.assertEqual(k.recover('order-6','unavailable_once',max_attempts=1)['status'],'RETRYABLE')
        self.assertEqual(k.recover('order-6','unavailable_once',max_attempts=2)['status'],'COMPLETED')
        self.assertEqual(self.count(),1)

    def test_restart_does_not_duplicate_committed_delivery(self):
        first=RecoveryKernel(self.ledger,self.base)
        self.assertEqual(first.recover('order-4')['status'],'COMPLETED')
        fresh=RecoveryKernel(self.ledger,self.base)
        self.assertEqual(fresh.recover('order-4')['status'],'COMPLETED')
        self.assertEqual(fresh.state('order-4')['attempts'],1)
        self.assertEqual(self.count(),1)

if __name__=='__main__': unittest.main(verbosity=2)
