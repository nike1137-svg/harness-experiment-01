# -*- coding: utf-8 -*-
"""
실험 02 작업 폴더 생성 (WSL에서 실행)

  python3 /mnt/c/Users/nike1/26_09_02/setup_exp02.py

생성 위치는 리눅스 네이티브 경로 ~/exp02 이다. (/mnt/c 에서 작업하지 않는다)
기존 폴더가 있으면 삭제 후 재생성한다.
"""
import os
import shutil

HOME = os.path.expanduser("~")
ROOT = os.path.join(HOME, "exp02")

SAMPLE_LOG = """2026-08-28 09:12:03 INFO  [api] service started on port 8080
2026-08-28 09:12:04 INFO  [db] connection pool size=10
2026-08-28 09:13:41 WARN  [api] slow response 1420ms path=/users
2026-08-28 09:14:02 ERROR [db] connection refused host=10.0.0.7 port=5432
2026-08-28 09:14:02 ERROR [db] retry 1/3 failed
2026-08-28 09:14:09 INFO  [api] request ok path=/health
2026-08-28 09:15:33 WARN  [cache] eviction rate high ratio=0.82
2026-08-28 09:16:10 ERROR [worker] task 4417 crashed
    Traceback (most recent call last):
      File "worker.py", line 88, in run
        payload = json.loads(raw)
    ValueError: Expecting value: line 1 column 1 (char 0)
2026-08-28 09:16:11 INFO  [worker] task 4417 requeued
2026-08-28 09:17:00 INFO  [api] user reported an ERROR in the UI form
28/Aug/2026:09:18:22 ERROR [auth] token signature mismatch user=ktm
2026-08-28 09:19:44 WARN  [api] deprecated endpoint /v1/list
2026-08-28 09:20:01 ERROR [db] connection refused host=10.0.0.7 port=5432
2026-08-28 09:21:15 INFO  [api] shutdown signal received
"""

UTIL_PY = '''def parse_duration(text):
    unit = text[-1]
    value = float(text[:-1])
    if unit == "s":
        return value
    if unit == "m":
        return value * 60
    if unit == "h":
        return value * 3600
    raise ValueError("unknown unit: " + unit)


def chunk_list(items, size):
    result = []
    for i in range(0, len(items), size):
        result.append(items[i:i + size])
    return result


def safe_get(mapping, key, default=None):
    parts = key.split(".")
    current = mapping
    for part in parts:
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current
'''

TEST_ME_PY = '''# ---- 구현부 (이 부분을 수정하시오) ----------------------------------


def median(numbers):
    ordered = sorted(numbers)
    middle = len(ordered) // 2
    return ordered[middle]


def percent_change(old, new):
    return (new - old) / new * 100


def flatten(nested):
    out = []
    for item in nested:
        if isinstance(item, list):
            out.extend(item)
        else:
            out.append(item)
    return out


# ---- 테스트부 (수정하지 마시오) --------------------------------------


def test_median_odd():
    assert median([3, 1, 2]) == 2


def test_median_even():
    assert median([4, 1, 3, 2]) == 2.5


def test_percent_change():
    assert percent_change(200, 250) == 25.0


def test_flatten():
    assert flatten([1, [2, 3], 4]) == [1, 2, 3, 4]
'''

FILES = {
    "sample.log": SAMPLE_LOG,
    "util.py": UTIL_PY,
    "test_me.py": TEST_ME_PY,
}

# 기존 블록 삭제 후 재작성
if os.path.isdir(ROOT):
    shutil.rmtree(ROOT)

fixtures = os.path.join(ROOT, "fixtures")
trial1 = os.path.join(ROOT, "trial-1")
os.makedirs(fixtures)
os.makedirs(trial1)

for name, content in FILES.items():
    for target in (fixtures, trial1):
        with open(os.path.join(target, name), "w", encoding="utf-8", newline="\n") as f:
            f.write(content)

print("생성 완료")
print("  " + fixtures + "   (원본 - 수정 금지)")
print("  " + trial1 + "   (1차 작업장)")
print("")
print("다음: 새 Claude Code 세션을 다음 폴더에서 연다")
print("  cd " + trial1)
