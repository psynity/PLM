import hashlib
import time

class ResearchSaaS:
    def __init__(self, user_id, project_id):
        self.user_id = user_id
        self.project_id = project_id
        self.base_reward = 0.1 # 기본 보상 단위

    def process_node(self, query, response, ktii_score):
        """연구 노드를 처리하고 자산 가치를 계산합니다."""
        timestamp = time.time()
        node_id = hashlib.sha256(f"{self.user_id}{timestamp}".encode()).hexdigest()[:12]
        
        # 1. 자산 가치 산정 (KTII 가중치 적용)
        # 암묵지(KTII -5)일수록 가중치 상승
        weight = 1.0 + (abs(ktii_score) * 0.2) 
        reward_amount = self.base_reward * weight
        
        # 2. 보상 패킷 생성
        asset_packet = {
            "node_id": node_id,
            "user": self.user_id,
            "project": self.project_id,
            "ktii": ktii_score,
            "reward": round(reward_amount, 4),
            "status": "Anchoring_Pending"
        }
        
        return asset_packet

# 실증 실행 예시
# user_a = ResearchSaaS("Alpha_Res", "20260424PYCL")
# print(user_a.process_node("2nm 공정 수율 최적화 방법", "...", -5))
