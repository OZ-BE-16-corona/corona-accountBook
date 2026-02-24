# config/services/category_classifier.py
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

from django.core.cache import cache

from category.models import Category
from config.services.category_keywords import CATEGORY_KEYWORDS, FALLBACK_CATEGORY_NAME


@dataclass(frozen=True)
class ClassificationResult:
    category_id: int
    category_name: str
    confidence: float
    matched_keyword: Optional[str]


def normalize_text(text: str) -> str:
    if not text:
        return ""
    t = text.strip()
    # 결제메모에 자주 등장하는 괄호/특수문자 처리
    t = re.sub(r"[()\[\]{}]", " ", t)
    t = re.sub(r"\s+", " ", t)
    return t


def build_category_name_to_id_map() -> dict[str, int]:
    """
    Category 테이블을 {category_name: id}로 매핑.
    캐시로 조회 최소화.
    """
    cache_key = "category_name_to_id_map_v1"
    m = cache.get(cache_key)
    if m:
        return m

    m = {c.category_name: c.id for c in Category.objects.all()}

    # '기타' 카테고리 없으면 생성(ERD 변경 X, 데이터 시드 보정)
    if FALLBACK_CATEGORY_NAME not in m:
        fallback = Category.objects.create(category_name=FALLBACK_CATEGORY_NAME)
        m[fallback.category_name] = fallback.id

    cache.set(cache_key, m, timeout=600)
    return m


def contains_keyword(haystack: str, keyword: str) -> bool:
    if not keyword:
        return False
    # 영문/숫자 포함 키워드는 대소문자 무시
    if re.search(r"[A-Za-z0-9]", keyword):
        return keyword.lower() in haystack.lower()
    return keyword in haystack


def classify_category(text: str) -> ClassificationResult:
    """
    memo/title 기반 카테고리 자동 분류
    - 키워드 매칭 → 최고 점수 카테고리
    - 매칭 없으면 '기타'
    """
    name_to_id = build_category_name_to_id_map()
    norm = normalize_text(text)

    best_name = FALLBACK_CATEGORY_NAME
    best_score = 0
    best_kw: Optional[str] = None

    for category_name, rule in CATEGORY_KEYWORDS.items():
        weight = int(rule.get("weight", 5))
        for kw in rule.get("keywords", []):
            if contains_keyword(norm, kw):
                score = weight
                if score > best_score:
                    best_score = score
                    best_name = category_name
                    best_kw = kw

    # 설명 가능한 confidence
    if best_name == FALLBACK_CATEGORY_NAME:
        confidence = 0.40
    else:
        confidence = min(0.95, 0.55 + best_score * 0.04)

    category_id = name_to_id.get(best_name) or name_to_id[FALLBACK_CATEGORY_NAME]
    return ClassificationResult(category_id, best_name, confidence, best_kw)