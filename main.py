import os
import google.generativeai as genai
from dotenv import load_dotenv
import yaml

# 1. 환경 변수 및 설정 로드
load_dotenv()
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# 2. 기초 인터페이스 클래스 정의
class ResearchCore:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.project_id = config['project']['id']
        self.engine = IntegrityEngine(config)
        self.storage = StorageManager(config)
        
        print(f"[{self.project_id}] 연구 엔진 초기화 완료.")

    def ask(self, prompt):
        # 향후 이 지점에서 백업 로직(Part 2)이 트리거됩니다.
        response = self.model.generate_content(prompt)
        response_text = self.model.generate_content(prompt).text

        
        ## 백그라운드 무결성 기록 실행
        # block = self.engine.create_block(prompt, response_text)
        # self.engine.save_to_markdown(block)

        # 1. 무결성 블록 생성 (Part 2)
        block = self.engine.create_block(prompt, response_text)
        
        # 2. 마크다운 저장 (가독성용)
        self.engine.save_to_markdown(block)
        
        # 3. SQLite 증분 저장 (데이터 자산화용)
        self.storage.insert_block(block)
        
        # 4. [선택적] Dew-Layer 동기화 트리거 : 향후 활용
        # self.sync_to_dew(block)
        
        return response.text


## main.py의 ResearchCore 클래스 확장 v2
# class ResearchCore:
#    def __init__(self):
#        # ... (기존 초기화 코드)
#        self.engine = IntegrityEngine(config)
#
#    def ask(self, prompt):
#        response_text = self.model.generate_content(prompt).text
#        
#        # 백그라운드 무결성 기록 실행
#        block = self.engine.create_block(prompt, response_text)
#        self.engine.save_to_markdown(block)
#        
#        return response_text

## main.py 또는 통합 모듈에서의 호출 구조 v3
#class ResearchCore:
#    def __init__(self):
#        # ... (기존 초기화 코드)
#        self.storage = StorageManager(config)

#    def ask(self, prompt):
#        response_text = self.model.generate_content(prompt).text
        
#        # 1. 무결성 블록 생성 (Part 2)
#        block = self.engine.create_block(prompt, response_text)
#        
#        # 2. 마크다운 저장 (가독성용)
#        self.engine.save_to_markdown(block)
#        
#        # 3. SQLite 증분 저장 (데이터 자산화용)
#        self.storage.insert_block(block)
#        
#        # 4. [선택적] Dew-Layer 동기화 트리거
#        # self.sync_to_dew(block)
#        
#        return response_text



if __name__ == "__main__":
    core = ResearchCore()
    # print(core.ask("연구노트 무결성 테스트를 위한 질문입니다."))
