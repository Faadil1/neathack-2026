"""Local deterministic recovery kernel, NOT an AI agent or live integration."""
import json
import sqlite3
import urllib.error
import urllib.request
from pathlib import Path

class RecoveryKernel:
    def __init__(self, ledger_path: str, receiver_base: str):
        self.ledger_path = ledger_path
        self.receiver_base = receiver_base.rstrip('/')
        Path(ledger_path).parent.mkdir(parents=True, exist_ok=True)
        with self._db() as db:
            db.execute('CREATE TABLE IF NOT EXISTS runs (event_id TEXT PRIMARY KEY, status TEXT NOT NULL, attempts INTEGER NOT NULL DEFAULT 0, detail TEXT NOT NULL DEFAULT "")')

    def _db(self):
        return sqlite3.connect(self.ledger_path)

    def state(self, event_id):
        with self._db() as db:
            row = db.execute('SELECT status, attempts, detail FROM runs WHERE event_id=?', (event_id,)).fetchone()
        return {'status': row[0], 'attempts': row[1], 'detail': row[2]} if row else None

    def _set(self, event_id, status, attempts, detail=''):
        with self._db() as db:
            db.execute('INSERT INTO runs(event_id,status,attempts,detail) VALUES(?,?,?,?) ON CONFLICT(event_id) DO UPDATE SET status=excluded.status, attempts=excluded.attempts, detail=excluded.detail', (event_id,status,attempts,detail))

    def _request(self, method, path, payload=None):
        req = urllib.request.Request(self.receiver_base + path,
            data=json.dumps(payload).encode() if payload is not None else None,
            headers={'Content-Type':'application/json'}, method=method)
        try:
            with urllib.request.urlopen(req, timeout=2) as resp:
                return resp.status, json.loads(resp.read().decode())
        except urllib.error.HTTPError as exc:
            return exc.code, json.loads(exc.read().decode())

    def recover(self, event_id: str, mode='ok', max_attempts=2):
        """Only retry 503. Never treat POST success as verified without downstream receipt."""
        prior=self.state(event_id)
        if prior and prior['status']=='COMPLETED':
            return prior
        if prior and prior['status'] in ('REVIEW_REQUIRED', 'BLOCKED'):
            return prior
        attempts=prior['attempts'] if prior else 0
        while attempts < max_attempts:
            attempts += 1
            try:
                code, response = self._request('POST', '/deliver', {'event_id':event_id, 'mode':mode})
            except (urllib.error.URLError, TimeoutError, OSError) as exc:
                self._set(event_id, 'REVIEW_REQUIRED', attempts, 'Transport failure; result ambiguous. Do not blindly repeat.')
                return self.state(event_id)
            if code==401 or code==403:
                self._set(event_id,'REVIEW_REQUIRED',attempts,'Authorization failure; human review required')
                return self.state(event_id)
            if code==400:
                self._set(event_id,'BLOCKED',attempts,'Invalid schema; no automatic rewrite')
                return self.state(event_id)
            if code==503:
                self._set(event_id,'RETRYABLE',attempts,'Remote temporary failure')
                continue
            if code not in (200,201):
                self._set(event_id,'REVIEW_REQUIRED',attempts,f'Unexpected response {code}')
                return self.state(event_id)
            try:
                rc, receipt=self._request('GET',f'/receipts/{event_id}')
            except (urllib.error.URLError, TimeoutError, OSError):
                rc,receipt=0,{}
            if rc==200 and receipt.get('event_id')==event_id and receipt.get('committed') is True:
                self._set(event_id,'COMPLETED',attempts,'Verified persisted downstream receipt')
            else:
                self._set(event_id,'UNVERIFIED',attempts,'No verified downstream receipt; no success claim')
            return self.state(event_id)
        return self.state(event_id)
