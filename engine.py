import hashlib
import datetime
import json
import os

class IntegrityEngine:
    def __init__(self, config):
        self.config = config
        self.project_id = config['project']['id']
        self.author = config['project']['author']
        self.log_path = config['storage']['path']
        self.prev_hash = self._load_last_hash()

    def _load_last_hash(self):
        """이전 기록을 찾아 마지막 해시값을 로드하거나 초기화합니다."""
        # 실제 구현 시 파일의 마지막 라인이나 DB에서 해시를 읽어옵니다.
        # 여기서는 단순화를 위해 'Genesis Block' 형태를 유지합니다.
        return "0" * 64 

    def create_block(self, query, response):
        """데이터 블록을 생성하고 해시 체이닝을 수행합니다."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 1. 메타데이터 주입
        metadata = {
            "entry_id": f"{self.project_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            "author": self.author,
            "timestamp": timestamp,
            "prev_hash": self.prev_hash
        }
        
        # 2. 데이터 본문 구성
        content = {
            "query": query,
            "response": response
        }
        
        # 3. 해시 계산 (Metadata + Content + Prev_Hash)
        block_data = {"metadata": metadata, "content": content}
        serialized_block = json.dumps(block_data, sort_keys=True).encode()
        current_hash = hashlib.sha256(serialized_payload).hexdigest()
        
        # 4. 체인 갱신 및 반환
        metadata["current_hash"] = current_hash
        self.prev_hash = current_hash
        
        return block_data

    def save_to_markdown(self, block):
        """연구노트 규정에 맞게 마크다운 형식으로 저장합니다."""
        if not os.path.exists(self.log_path):
            os.makedirs(self.log_path)
            
        filename = f"{self.log_path}{self.project_id}_note.md"
        meta = block['metadata']
        content = block['content']
        
        with open(filename, "a", encoding="utf-8") as f:
            f.write(f"\n---\n")
            f.write(f"### [ENTRY: {meta['entry_id']}]\n")
            f.write(f"**Timestamp:** {meta['timestamp']} | **Author:** {meta['author']}\n")
            f.write(f"**Prev Hash:** `{meta['prev_hash']}`\n")
            f.write(f"**Curr Hash:** `{meta['current_hash']}`\n\n")
            f.write(f"#### Q: {content['query']}\n")
            f.write(f"#### A: {content['response']}\n")
