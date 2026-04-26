import sqlite3
import json

class StorageManager:
    def __init__(self, config):
        self.db_path = config['storage'].get('db_path', './notes/research_vault.db')
        self._init_db()

    def _init_db(self):
        """연구 기록 저장을 위한 SQLite 테이블을 초기화합니다."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS research_blocks (
                    entry_id TEXT PRIMARY KEY,
                    timestamp TEXT,
                    prev_hash TEXT,
                    current_hash TEXT,
                    query TEXT,
                    response TEXT,
                    ktii_score REAL,
                    raw_json TEXT
                )
            ''')
            conn.commit()

    def insert_block(self, block_data):
        """무결성이 검증된 블록을 DB에 증분 저장합니다."""
        meta = block_data['metadata']
        content = block_data['content']
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO research_blocks 
                (entry_id, timestamp, prev_hash, current_hash, query, response, raw_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                meta['entry_id'],
                meta['timestamp'],
                meta['prev_hash'],
                meta['current_hash'],
                content['query'],
                content['response'],
                json.dumps(block_data)
            ))
            conn.commit()

    def get_sync_payload(self, last_sync_id=None):
        """Dew-Layer 전송을 위한 미동기화 블록 추출 인터페이스"""
        # 실제 구현 시 last_sync_id 이후의 데이터만 쿼리하여 전송 객체 생성
        pass
