import os
from dotenv import load_dotenv
from openai import OpenAI
from envs.tabletop_env import PickPlaceEnv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

with open("prompt_script.txt") as f:
  base = f.read()

task = input("Enter function name: ").strip()
prompt = f"{base}\n# Task: {task}"

res = client.chat.completions.create(
  model="gpt-4o",
  messages=[{"role": "user", "content": prompt}],
  temperature=0
)

code = res.choices[0].message.content.strip().replace("```python", "").replace("```", "")

# 생성된 코드를 generated_func.py로 저장
with open("output/generated_func.py", "w") as f:
  f.write(code)

# 저장된 파일 실행
exec(open("output/generated_func.py").read())

env = PickPlaceEnv(record=True)
env.reset(["red block", "blue bowl"])

# 생성된 함수 호출
globals()[task]()

env.save_video(f"output/{task}.mp4")
