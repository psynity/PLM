import hashlib
import datetime
import json

class ResearchNoteEngine:
    def __init__(self, author_id, project_code):
        self.author_id = author_id
        self.project_code = project_code
        self.prev_hash = "0" * 64  # 초기 블록(Genesis Block)

    def generate_hash(self, data_content):
        # 1. 타임스탬프 생성
        timestamp = datetime.datetime.now().isoformat()
        
        # 2. 메타데이터 및 이전 해시 결합
        payload = {
            "project": self.project_code,
            "author": self.author_id,
            "timestamp": timestamp,
            "data": data_content,
            "prev_hash": self.prev_hash
        }
        
        # 3. SHA-256 해시 생성
        serialized_payload = json.dumps(payload, sort_keys=True).encode()
        current_hash = hashlib.sha256(serialized_payload).hexdigest()
        
        # 4. 다음 체인을 위해 현재 해시 저장 및 페이로드 반환
        self.prev_hash = current_hash
        return payload, current_hash

# 실행 예시
engine = ResearchNoteEngine("Alpha_Leader", "20260424PYCL")
note_entry, current_hash = engine.generate_hash("AI 연구노트 무결성 엔진 설계 완료")
print(f"Current Hash: {current_hash}")
