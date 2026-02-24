# config/services/category_keywords.py

CATEGORY_KEYWORDS: dict[str, dict] = {
    "편의점": {
        "weight": 10,
        "keywords": ["CU", "씨유", "GS25", "지에스25", "세븐일레븐", "7ELEVEN", "이마트24"],
    },
    "카페/간식": {
        "weight": 9,
        "keywords": ["스타벅스", "STARBUCKS", "투썸", "TWOSOME", "이디야", "메가커피", "컴포즈", "빽다방"],
    },
    "배달": {
        "weight": 9,
        "keywords": ["배민", "배달의민족", "요기요", "쿠팡이츠", "배달"],
    },
    "쇼핑": {
        "weight": 8,
        "keywords": ["쿠팡", "COUPANG", "네이버", "NAVER", "11번가", "G마켓", "SSG", "무신사", "올리브영", "다이소"],
    },
    "교통": {
        "weight": 8,
        "keywords": ["지하철", "버스", "택시", "카카오택시", "우버", "KTX", "SRT", "티머니"],
    },
    "주거": {
        "weight": 10,
        "keywords": ["월세", "관리비", "전세", "보증금", "부동산", "임대"],
    },
    "통신": {
        "weight": 8,
        "keywords": ["SKT", "KT", "LGU", "유플러스", "통신", "요금"],
    },
    "구독": {
        "weight": 9,
        "keywords": ["넷플릭스", "NETFLIX", "유튜브", "YOUTUBE", "멜론", "SPOTIFY", "디즈니", "DISNEY", "구독"],
    },
    "의료/건강": {
        "weight": 8,
        "keywords": ["병원", "의원", "약국", "치과", "한의원", "검진", "처방"],
    },
    "보험": {
        "weight": 8,
        "keywords": ["보험", "삼성화재", "현대해상", "DB손해보험", "KB손해"],
    },
    "금융/수수료": {
        "weight": 7,
        "keywords": ["수수료", "이체", "송금", "ATM", "출금", "연회비"],
    },
    "식비": {
        "weight": 7,
        "keywords": ["식사", "점심", "저녁", "아침", "밥", "김밥", "국밥", "치킨", "피자", "분식"],
    },
}

# DB에 반드시 존재해야 하는 기본 카테고리 이름
FALLBACK_CATEGORY_NAME = "기타"