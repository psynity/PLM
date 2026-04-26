import os
import yaml
from dotenv import load_dotenv
import google.generativeai as genai
from core.engine import IntegrityEngine
from core.database import AssetManager

def run_demo():
    # 환경 로드
    load_dotenv()
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # 엔진 초기화
    engine = IntegrityEngine(config)
    db = AssetManager(config['storage']['db_path'])
    
    print(f"--- {config['project']['id']} 지식 주권 엔진 가동 ---")
    
    while True:
        user_input = input("\n연구 질문 입력 (종료: exit): ")
        if user_input.lower() == 'exit': break
        
        # 1. AI 응답 생성
        response = model.generate_content(user_input)
        
        # 2. 무결성 블록 생성 및 체이닝
        block = engine.generate_block(user_input, response.text)
        
        # 3. DB 기록 (자산화)
        db.record(block)
        
        print(f"\n[AI]: {response.text}")
        print(f"\n[SYSTEM]: 해시 생성 완료 -> {block['metadata']['current_hash'][:15]}...")

if __name__ == "__main__":
    run_demo()
