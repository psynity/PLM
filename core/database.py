import sqlite3

class AssetManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self._bootstrap()

    def _bootstrap(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS research_ledger 
                (entry_id TEXT PRIMARY KEY, timestamp TEXT, prev_hash TEXT, 
                 curr_hash TEXT, query TEXT, response TEXT)''')

    def record(self, block):
        m = block['metadata']
        c = block['content']
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT INTO research_ledger VALUES (?,?,?,?,?,?)",
                (m['project_id']+"_"+m['timestamp'], m['timestamp'], 
                 m['prev_hash'], m['current_hash'], c['query'], c['response']))
