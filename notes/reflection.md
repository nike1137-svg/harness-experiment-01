# 1차 시도 반성 기록

## parse-log
- 로그 형식은 `YYYY-MM-DD HH:MM:SS LEVEL 메시지` 이며, ERROR는 3건이다.
- 다음 시도에서는 파일 형식 확인 없이 바로 이 정규식 형태로 작성한다.

## refactor-util
- util.py 함수는 slugify, chunk, merge_defaults 3개다.
- chunk는 List[List[Any]], merge_defaults는 Dict[Any, Any] 반환이다.
- 다음 시도에서는 파일을 읽은 뒤 3개를 한 번에 수정한다.

## fix-failing
- 실패 원인은 divide(1, 0)과 average([]) 두 곳의 예외다.
- divide는 b == 0일 때 None, average는 빈 리스트일 때 0을 반환해야 한다.
- test_me.py는 수정 대상이 아니다. calc.py만 고친다.
