import hashlib
import json
import datetime

class IntegrityEngine:
    def __init__(self, config):
        self.config = config
        self.prev_hash = "0" * 64 

    def generate_block(self, query, response):
        timestamp = datetime.datetime.now().isoformat()
        metadata = {
            "project_id": self.config['project']['id'],
            "author": self.config['project']['author'],
            "timestamp": timestamp,
            "prev_hash": self.prev_hash
        }
        content = {"query": query, "response": response}
        
        # 해시 생성 (순서 고정)
        block_raw = json.dumps({"metadata": metadata, "content": content}, sort_keys=True).encode()
        current_hash = hashlib.sha256(block_raw).hexdigest()
        
        metadata["current_hash"] = current_hash
        self.prev_hash = current_hash
        
        return {"metadata": metadata, "content": content}
