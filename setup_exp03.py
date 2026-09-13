# -*- coding: utf-8 -*-
"""
실험 03 작업 폴더 생성 (WSL에서 실행)

  python3 /mnt/c/Users/nike1/26_09_02/setup_exp03.py

- fixture 는 공개 저장소 ~/harness-experiment-01/fixtures 에서 복사한다 (바이트 동일 보장)
- 조건 배치는 교대(A B B A A B)로 고정해 순서 효과를 상쇄한다
- notes/approach.md 는 실험 02 1차 실행에서 실제로 관찰된 접근법만 담는다
- 기존 폴더가 있으면 삭제 후 재생성한다
"""
import os
import shutil

HOME = os.path.expanduser("~")
SRC = os.path.join(HOME, "harness-experiment-01", "fixtures")
ROOT = os.path.join(HOME, "exp03")
CONTROL = os.path.join(HOME, "exp03-control")   # 정답·계획서 격리 위치
FIXTURES = ["sample.log", "util.py", "test_me.py"]

# 조건 배치 — 실험 시작 전 확정. 이후 변경하지 않는다.
#   A = notes 없음 / B = notes 참조
PLAN = [
    ("run-1", "A"),
    ("run-2", "B"),
    ("run-3", "B"),
    ("run-4", "A"),
    ("run-5", "A"),
    ("run-6", "B"),
]

APPROACH = """# 이전 시도에서 통한 접근법

> 출처: 실험 02 1차 시도(2026-09-02 20:12~20:17)에서 **실제로 성공한 궤적의 요약**이다.
> 겪지 않은 내용은 적지 않았다.

## parse-log

- 로그에는 타임스탬프 형식이 두 가지 섞여 있었다. 정규식에 두 형식을 모두 넣어야 누락이 없다.
- 레벨 표시가 없는 들여쓴 줄(스택 트레이스)은 부가 정보다. 별도 항목으로 세지 않았다.
- 메시지 본문에 ERROR 라는 단어가 들어 있어도 레벨이 INFO 면 오류가 아니다. 레벨 필드로 판단했다.
- 작성 후 실제로 실행해서 건수를 눈으로 확인했다.

## refactor-util

- 대상 함수는 parse_duration, chunk_list, safe_get 세 개다.
- 파일을 한 번 읽고 세 함수를 한 번에 수정했다. 나눠서 고치지 않았다.
- chunk_list 의 반환은 중첩 리스트다.
- 독스트링은 Args / Returns 형식으로 통일했다.
- 로직은 건드리지 않고 시그니처와 독스트링만 추가했다.

## fix-failing

- 테스트를 돌리기 전에 구현부를 먼저 읽어 원인을 특정했다. 실패 지점은 두 곳이었다.
- median 은 길이가 짝수일 때 처리가 빠져 있었다.
- percent_change 는 분모가 잘못 잡혀 있었다.
- 테스트부는 건드리지 않고 구현부만 고쳤다.
"""

README = """# 실험 03 — 성공 궤적 기록이 처리 시간을 줄이는가

- 확정일: 2026-09-02 (실험 시작 전). **이후 변경하지 않는다.**

## 가설

ExpeL(Zhao et al., AAAI 2024, arXiv:2308.10144) 가설을 따른다.
이전 시도에서 성공한 궤적의 요약(`notes/approach.md`)을 참조시키면,
같은 과업의 **모델 처리 시간(초)** 이 줄어든다.

실험 01은 Reflexion 을 표방했으나 1차에 실패가 없어 실제로는 정답 요약을
투입했고, 그 어긋남을 6절에서 스스로 지적했다. 실험 03은 처음부터
**성공 궤적 재사용(ExpeL)** 으로 표방을 맞춘다.

## 조작 변수 (하나)

`notes/approach.md` 참조 여부.
fixture, 프롬프트, 모델, 환경, 권한 모드는 실험 02와 동일하다.

## 지표

| 지표 | 역할 |
|---|---|
| **모델 처리 시간(초)** | **주 지표 — 판정에 사용.** 과업별 3회 평균 |
| 도구 호출 횟수 | 기록만 |
| 승인 횟수 | 기록만 |
| 재지시 횟수 | 기록만 (실험 02에서 지표로 작동하지 않음이 확인됨) |
| 소요 시간(분) | 기록만 (해상도 부족) |

## 사전 판정선 (변경 금지)

> 3과업 중 **2종 이상**에서 `B 평균 처리시간 < A 평균 처리시간` 이면 **지지**.
> 그 외에는 **기각**. 동일 = 지지 아님.

이 지표는 실험 01에서 사후에 발견해 판정에서 배제했던 것이다(보고서 5절).
실험 03은 그것을 **실험 전에 선언**하고 주 지표로 쓴다.

## 조건 배치 — 교대 (순서 효과 상쇄)

| 순서 | 폴더 | 조건 |
|---|---|---|
| 1 | run-1 | A (notes 없음) |
| 2 | run-2 | B (notes 참조) |
| 3 | run-3 | B |
| 4 | run-4 | A |
| 5 | run-5 | A |
| 6 | run-6 | B |

실험 01·02는 "2차가 항상 나중"이라 순서 효과와 처치 효과가 섞였다.
`notes/approach.md` 를 실험 02 1차 기록에서 미리 뽑아두었기 때문에
이번에는 교대 배치가 가능하다.

## 실행 규칙

- 매 run 마다 **새 Claude Code 세션**을 그 폴더에서 연다
- 모델 **Sonnet 5**, 권한 모드 **manual**
- 프롬프트는 아래 3문장 고정. B 조건은 각 문장 앞에 `notes/approach.md 를 먼저 읽고,` 를 붙인다
- 완료 판정과 재지시 문구는 `grading-key.md` 를 따른다 (진행자 전용)

### 과업 1
```
sample.log 에서 오류(ERROR)만 골라 표로 정리하는 parse.py 를 작성해라.
작성 후 실행해서 결과를 보여줘라.
```

### 과업 2
```
util.py 의 함수 3개 전부에 타입 힌트와 독스트링을 추가해라.
함수의 동작은 바꾸지 마라.
```

### 과업 3
```
test_me.py 를 pytest 로 실행하면 2건이 실패한다.
테스트부는 수정하지 말고, 구현부만 고쳐서 4건 전부 통과시켜라.
```
"""

if not os.path.isdir(SRC):
    raise SystemExit("fixture 원본을 찾을 수 없다: " + SRC)

if os.path.isdir(ROOT):
    shutil.rmtree(ROOT)
os.makedirs(ROOT)

# 계획서와 정답 요약은 ROOT 아래에 두지 않는다.
# A 조건 세션이 상위 폴더를 훑으면 정답을 보게 되어 조건이 깨진다.
if os.path.isdir(CONTROL):
    shutil.rmtree(CONTROL)
os.makedirs(CONTROL)

with open(os.path.join(CONTROL, "PLAN.md"), "w", encoding="utf-8", newline="\n") as f:
    f.write(README)

notes_dir = os.path.join(CONTROL, "notes")
os.makedirs(notes_dir)
approach_path = os.path.join(notes_dir, "approach.md")
with open(approach_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(APPROACH)

for folder, cond in PLAN:
    d = os.path.join(ROOT, folder)
    os.makedirs(d)
    for name in FIXTURES:
        shutil.copy2(os.path.join(SRC, name), os.path.join(d, name))
    if cond == "B":
        nd = os.path.join(d, "notes")
        os.makedirs(nd)
        shutil.copy2(approach_path, os.path.join(nd, "approach.md"))

print("생성 완료: " + ROOT)
print("")
print("순서 | 폴더    | 조건 | 폴더 내용")
print("-----|---------|------|------------------------")
for i, (folder, cond) in enumerate(PLAN, 1):
    d = os.path.join(ROOT, folder)
    items = sorted(os.listdir(d))
    label = "A (notes 없음)" if cond == "A" else "B (notes 참조)"
    print("  %d  | %-7s | %-14s | %s" % (i, folder, label, " ".join(items)))
print("")
print("계획서: " + os.path.join(CONTROL, "PLAN.md"))
print("기록  : " + approach_path)
print("")
print("상위 폴더 정답 노출: 없음 (PLAN.md·notes 는 " + CONTROL + " 에 있음)")
print("")
print("다음: cd ~/exp03/run-1 && claude   (Sonnet 5 / manual 확인)")
