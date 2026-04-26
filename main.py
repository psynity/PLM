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

        print(f"[{self.project_id}] 연구 엔진 초기화 완료.")

    def ask(self, prompt):
        # 향후 이 지점에서 백업 로직(Part 2)이 트리거됩니다.
        response = self.model.generate_content(prompt)
        response_text = self.model.generate_content(prompt).text

        # 백그라운드 무결성 기록 실행
        block = self.engine.create_block(prompt, response_text)
        self.engine.save_to_markdown(block)

        
        return response.text


## main.py의 ResearchCore 클래스 확장
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


if __name__ == "__main__":
    core = ResearchCore()
    # print(core.ask("연구노트 무결성 테스트를 위한 질문입니다."))
