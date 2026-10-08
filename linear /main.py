from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Linear Search Visualization API",
    description="선형 검색 알고리즘의 수행 과정과 단계별 상태를 반환하는 API"
)

# CORS 설정: 구글 앱스 스크립트 및 웹 클라이언트 요청 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 요청 데이터 모델 정의
class SearchRequest(BaseModel):
    array: List[int]      # 검색 대상 정수 배열
    target: int           # 찾고자 하는 목표 값

# 응답 데이터 모델 정의 (단계별 진행 상황 저장용)
class SearchStep(BaseModel):
    step: int             # 현재 단계 번호 (1부터 시작)
    index: int            # 현재 검사 중인 배열의 인덱스
    value: int            # 현재 인덱스의 값
    is_found: bool        # 찾았는지 여부
    status: str           # 단계별 설명 메세지

class SearchResponse(BaseModel):
    target: int                       # 목표 값
    array: List[int]                  # 원본 배열
    found: bool                       # 최종 검색 성공 여부
    found_index: Optional[int]        # 찾은 경우 인덱스 (없으면 None)
    total_steps: int                  # 총 비교 횟수
    time_complexity: dict             # 시간 및 공간 복잡도 정보
    steps: List[SearchStep]           # 시각화를 위한 단계별 트레이스 데이터

@app.post("/search", response_model=SearchResponse)
def linear_search(request: SearchRequest):
    """
    선형 검색을 수행하고 각 단계별 탐색 과정(Trace)을 기록하여 반환합니다.
    """
    if not request.array:
        raise HTTPException(status_code=400, detail="배열이 비어있습니다.")

    steps = []
    found = False
    found_index = None

    # 선형 검색 수행: 배열의 처음부터 끝까지 순차 탐색 (O(N))
    for idx, val in enumerate(request.array):
        is_match = (val == request.target)
        
        step_info = SearchStep(
            step=len(steps) + 1,
            index=idx,
            value=val,
            is_found=is_match,
            status=f"인덱스 {idx}의 값({val})과 목표 값({request.target}) 비교 -> {'일치!' if is_match else '불일치'}"
        )
        steps.append(step_info)

        if is_match:
            found = True
            found_index = idx
            break  # 목표 값을 찾으면 검색 종료

    return SearchResponse(
        target=request.target,
        array=request.array,
        found=found,
        found_index=found_index,
        total_steps=len(steps),
        time_complexity={
            "best": "O(1) - 첫 번째 요소에서 찾은 경우",
            "average": "O(N) - 중간에서 찾거나 평균적인 경우",
            "worst": "O(N) - 마지막 요소에서 찾거나 존재하지 않는 경우",
            "space": "O(1) - 추가 메모리 사용 최소화"
        },
        steps=steps
    )

@app.get("/")
def health_check():
    """서버 상태 확인용 엔드포인트"""
    return {"status": "ok", "message": "Linear Search Service is running"}
