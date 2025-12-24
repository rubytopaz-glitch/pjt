import json
import re
from typing import Any, Dict, List, Optional, Tuple

from django.conf import settings
from openai import OpenAI

GMS_BASE_URL = "https://gms.ssafy.io/gmsapi/api.openai.com/v1"

client = OpenAI(
    api_key=settings.GMS_KEY,
    base_url=GMS_BASE_URL,
)

RECOMMEND_LIMIT = 3

GENRE_LIST = [
    "드라마", "SF", "판타지", "로맨스", "뮤지컬", "애니메이션", "전쟁", "가족", "다큐멘터리",
    "스릴러", "공포", "액션", "코미디", "범죄", "모험", "미스터리", "역사", "음악", "서부"
]
GENRES = ", ".join(GENRE_LIST)

# ----------------------------
# utils
# ----------------------------
def _safe_json(text: str) -> Optional[Dict[str, Any]]:
    try:
        if not text:
            return None
        text = re.sub(r"```(?:json)?", "", text, flags=re.IGNORECASE).replace("```", "").strip()
        m = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if not m:
            return None
        return json.loads(m.group(0))
    except Exception:
        return None


def _dedupe_str_list(items: Any) -> List[str]:
    if not isinstance(items, list):
        return []
    seen = set()
    out: List[str] = []
    for x in items:
        if not isinstance(x, str):
            continue
        s = x.strip()
        if not s or s in seen:
            continue
        seen.add(s)
        out.append(s)
    return out


def _clamp(n: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, n))


def _infer_min_vote_from_message(message: str) -> float:
    nums = re.findall(r"(\d+(?:\.\d+)?)", message)
    if nums:
        try:
            return _clamp(float(nums[0]), 0.0, 10.0)
        except Exception:
            pass

    if any(k in message for k in ["명작", "평점", "후회", "인생영화", "극찬", "완성도", "탄탄"]):
        return 7.5
    if any(k in message for k in ["무난", "가볍게", "편하게", "대중적", "부담없이"]):
        return 6.5
    return 6.0


def _pick_strict_from_message(message: str) -> bool:
    """
    사용자가 '딱/오직/만/정확히/제대로/엄격히' 같은 표현 쓰면 strict=True로.
    """
    keys = ["딱", "오직", "만", "정확", "엄격", "무조건", "반드시"]
    return any(k in message for k in keys)


# ----------------------------
# PROMPTS
# ----------------------------

SYSTEM_PROMPT_FILTER = f"""
너는 영화 추천 서비스의 '필터 추출기'다.
사용자 메시지를 읽고 DB 검색을 위한 필터를 JSON으로만 반환한다.

[절대 규칙]
- 출력은 반드시 순수 JSON만. 마크다운/코드펜스/설명 문장 금지.
- 장르는 반드시 이 목록에서만 선택: [{GENRES}]
- 키는 정확히 아래 스키마만 사용한다.

[JSON 스키마]
{{
  "answer": "사용자에게 보여줄 짧은 안내(1~2문장)",
  "filters": {{
    "primary_genre_name": null 또는 "장르1",
    "genre_names": ["장르1", "장르2"],
    "exclude_genre_names": ["제외장르1"],
    "exclude_titles": ["제외할 영화제목1"],
    "keywords": ["키워드1", "키워드2"],
    "titles": ["사용자가 언급한 영화제목"],
    "min_vote": 0~10 숫자,
    "strict": true/false
  }}
}}

[해석 규칙 - 매우 중요]
1) 장르/분위기 매핑
- "따뜻한/힐링/연말/겨울/눈/가족/로맨틱" -> 기본 후보: 드라마, 로맨스, 가족, 코미디
- "긴장감/반전/추리" -> 미스터리, 스릴러
- "액션/시원한" -> 액션, 모험
- 사용자가 '장르를 명시'하면 그 장르를 primary_genre_name으로 우선 설정한다.

2) 제외 조건 처리
- 사용자가 "A 빼고/제외/말고"라고 하면:
  - A가 장르 목록에 있으면 exclude_genre_names에 넣는다.
  - A가 특정 영화 제목(예: 체인소맨)이면 exclude_titles에 넣는다.
- 따뜻한/힐링 계열 요청이면 사용자가 별도 언급이 없어도 기본적으로
  공포/스릴러/범죄/전쟁은 exclude_genre_names에 넣는다. (단, 사용자가 원하면 제외하지 말 것)

3) strict 설정
- 사용자가 "딱/오직/만/정확히/엄격" 뉘앙스 -> strict=true
- 그렇지 않으면 strict=false

4) min_vote
- "명작/평점 높은/후회 없는/극찬" -> 7.5
- "무난/가볍게" -> 6.5
- 별 말 없으면 6.0
- 사용자가 숫자를 말하면 그 값 사용

5) 키워드
- keywords에는 분위기/상황을 검색에 도움 되는 단어로 넣는다.
  예: 겨울, 연말, 눈, 따뜻한, 힐링, 가족, 사랑, 우정, 감성
- "영화/추천" 같은 포괄어 금지

[answer 작성]
- 1~2문장으로, “요청 조건 반영해서 추천하겠다” 정도만 말한다.
- 영화 제목 나열 금지.

이제 사용자 메시지에 대해 JSON만 출력해라.
""".strip()


SYSTEM_PROMPT_REASONS = """
너는 영화 추천 이유를 '영화 리스트 기반'으로 작성하는 에디터다.

[입력]
- user_request: 사용자가 원하는 분위기/조건
- movies: 영화 리스트(각 항목에 tmdb_id, title, genres(optional), vote_average(optional), overview(optional))

[출력 규칙]
- 반드시 순수 JSON만 출력한다.
- key는 tmdb_id(문자열)로 하고, value는 추천 이유 한 문장.
- 추천 이유는 20~35자 내외, 스포일러 금지, 사용자 조건과 영화 특징을 연결.
- 영화 리스트에 없는 tmdb_id를 만들지 말 것.
- 값이 비어 있으면 안 됨.

[출력 형식]
{
  "reasons": {
    "123": "겨울 감성에 어울리는 포근한 로맨스입니다.",
    "456": "힐링 분위기와 잔잔한 여운이 좋은 영화입니다."
  }
}
""".strip()


# ----------------------------
# normalize
# ----------------------------
def _normalize_filters_output(data: Dict[str, Any], message: str) -> Dict[str, Any]:
    answer = data.get("answer")
    filters = data.get("filters") or {}

    if not isinstance(answer, str) or not answer.strip():
        answer = "원하시는 분위기와 조건에 맞춰 추천을 준비해볼게요."

    primary = filters.get("primary_genre_name")
    primary = primary.strip() if isinstance(primary, str) else None

    genre_names = _dedupe_str_list(filters.get("genre_names", []))
    exclude_genres = _dedupe_str_list(filters.get("exclude_genre_names", []))
    exclude_titles = _dedupe_str_list(filters.get("exclude_titles", []))
    keywords = _dedupe_str_list(filters.get("keywords", []))
    titles = _dedupe_str_list(filters.get("titles", []))

    if primary not in GENRE_LIST:
        primary = None
    genre_names = [g for g in genre_names if g in GENRE_LIST]
    exclude_genres = [g for g in exclude_genres if g in GENRE_LIST]

    # include/exclude 충돌 제거 (exclude 우선)
    genre_names = [g for g in genre_names if g not in exclude_genres]
    if primary in exclude_genres:
        primary = None

    # strict 기본값: 모델이 비워도 사용자 표현으로 보정
    strict_raw = filters.get("strict")
    if isinstance(strict_raw, (bool, int)):
        strict = bool(strict_raw)
    else:
        strict = _pick_strict_from_message(message)

    min_vote = filters.get("min_vote")
    if not isinstance(min_vote, (int, float)):
        min_vote = _infer_min_vote_from_message(message)
    min_vote = _clamp(float(min_vote), 0.0, 10.0)

    return {
        "answer": answer.strip(),
        "filters": {
            "primary_genre_name": primary,
            "genre_names": genre_names[:4],
            "exclude_genre_names": exclude_genres[:4],
            "exclude_titles": exclude_titles[:6],
            "keywords": keywords[:8],
            "titles": titles[:5],
            "min_vote": min_vote,
            "strict": strict,
        }
    }


def _normalize_reasons_output(data: Dict[str, Any], movies: List[Dict[str, Any]]) -> Dict[str, str]:
    """
    reasons는 tmdb_id(str) -> reason(str) 형태로만.
    영화 리스트에 없는 id는 버림.
    """
    reasons = data.get("reasons")
    if not isinstance(reasons, dict):
        return {}

    valid_ids = {str(m.get("tmdb_id")) for m in movies if m.get("tmdb_id") is not None}
    out: Dict[str, str] = {}

    for k, v in reasons.items():
        sid = str(k).strip()
        if sid not in valid_ids:
            continue
        if not isinstance(v, str):
            continue
        reason = v.strip()
        if not reason:
            continue
        # 너무 길면 잘라서 UI 깨짐 방지
        if len(reason) > 60:
            reason = reason[:60].rstrip()
        out[sid] = reason

    return out


# ----------------------------
# public functions
# ----------------------------
def run_taste_ai_filters(message: str, history: Optional[List[Dict[str, str]]] = None) -> Tuple[Dict[str, Any], str]:
    msgs: List[Dict[str, str]] = [{"role": "system", "content": SYSTEM_PROMPT_FILTER}]

    if isinstance(history, list) and history:
        trimmed: List[Dict[str, str]] = []
        for m in history[-10:]:
            if isinstance(m, dict) and m.get("role") in ("user", "assistant") and isinstance(m.get("content"), str):
                trimmed.append({"role": m["role"], "content": m["content"]})
        msgs += trimmed

    msgs.append({"role": "user", "content": message})

    model = getattr(settings, "GMS_MODEL", "gpt-4o-mini")

    res = client.chat.completions.create(
        model=model,
        messages=msgs,
        temperature=0.2,
        # 가능하면 JSON 강제 (GMS에서 지원하면 안정성 확 올라감)
        # response_format={"type": "json_object"},
    )

    raw = (res.choices[0].message.content or "").strip()
    parsed = _safe_json(raw)

    if not parsed:
        fallback = {
            "answer": "죄송합니다. 추천을 생성하는 중에 문제가 발생했습니다.",
            "filters": {
                "primary_genre_name": None,
                "genre_names": [],
                "exclude_genre_names": [],
                "exclude_titles": [],
                "keywords": [],
                "titles": [],
                "min_vote": _infer_min_vote_from_message(message),
                "strict": _pick_strict_from_message(message),
            }
        }
        return fallback, raw

    data = _normalize_filters_output(parsed, message)
    return data, raw


def run_taste_ai_reasons(user_request: str, movies: List[Dict[str, Any]]) -> Tuple[Dict[str, str], str]:
    """
    DB에서 뽑힌 movies를 기반으로 tmdb_id별 추천 이유를 생성한다.
    movies 항목에는 최소 tmdb_id, title은 있어야 함.
    """
    payload = {
        "user_request": user_request,
        "movies": [
            {
                "tmdb_id": m.get("tmdb_id"),
                "title": m.get("title"),
                "genres": m.get("genres"),
                "vote_average": m.get("vote_average"),
                "overview": m.get("overview"),
            }
            for m in movies
        ]
    }

    msgs = [
        {"role": "system", "content": SYSTEM_PROMPT_REASONS},
        {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
    ]

    # 이유 생성은 필터보다 모델 품질이 체감됨 → 필요하면 여기만 상위 모델 사용
    model = getattr(settings, "GMS_MODEL_REASON", getattr(settings, "GMS_MODEL", "gpt-4o-mini"))

    res = client.chat.completions.create(
        model=model,
        messages=msgs,
        temperature=0.3,
        # response_format={"type": "json_object"},
    )

    raw = (res.choices[0].message.content or "").strip()
    parsed = _safe_json(raw)
    if not parsed:
        return {}, raw

    reasons = _normalize_reasons_output(parsed, movies)
    return reasons, raw


# 기존 호환용(필터만)
def run_taste_ai(message: str, history: Optional[List[Dict[str, str]]] = None) -> Tuple[Dict[str, Any], str]:
    return run_taste_ai_filters(message, history)
