# 프로젝트 폴더 생성 및 이동
mkdir 20260424PYCL_Project && cd 20260424PYCL_Project

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 필수 라이브러리 설치
pip install google-generativeai python-dotenv pyyaml pandas
