"""
심평원 병원정보서비스 Open API → MySQL 저장
- 강남구 병원 목록을 페이지 단위로 전수 조회하여 ORM으로 저장합니다.
- .env에 SERVICE_KEY=<발급받은 인증키> 를 추가해야 합니다.
"""
import os
import time

import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine, String, Integer, Float, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

load_dotenv()

# ── DB 연결 ───────────────────────────────────────────────────
DATABASE_URL = (
    "mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset=utf8mb4".format(
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "3306"),
        db=os.getenv("DB_NAME", "crawler_db"),
    )
)

engine = create_engine(DATABASE_URL, echo=False)

# ── API 설정 ──────────────────────────────────────────────────
API_URL = "https://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList"
SERVICE_KEY = os.getenv("SERVICE_KEY", "")

# 강남구 지역 코드 (행정안전부 표준 코드)
SIDO_CD = "110000"   # 서울특별시
SGGU_CD = "110001"   # 강남구

PAGE_SIZE = 100      # 한 번에 가져올 건수 (최대 100)


# ── 모델 정의 ─────────────────────────────────────────────────

class Base(DeclarativeBase):
    pass


class Hospital(Base):
    __tablename__ = "hospitals_gangnam"

    ykiho:          Mapped[str]        = mapped_column(String(20),  primary_key=True, comment="암호화 요양기호")
    yadm_nm:        Mapped[str]        = mapped_column(String(100), nullable=False,   comment="병원명")
    cl_cd:          Mapped[str | None] = mapped_column(String(10),                   comment="종별코드")
    cl_cd_nm:       Mapped[str | None] = mapped_column(String(50),                   comment="종별코드명")
    sido_cd_nm:     Mapped[str | None] = mapped_column(String(50),                   comment="시도명")
    sggu_cd_nm:     Mapped[str | None] = mapped_column(String(50),                   comment="시군구명")
    emdong_nm:      Mapped[str | None] = mapped_column(String(50),                   comment="읍면동명")
    addr:           Mapped[str | None] = mapped_column(String(200),                  comment="주소")
    post_no:        Mapped[str | None] = mapped_column(String(10),                   comment="우편번호")
    telno:          Mapped[str | None] = mapped_column(String(30),                   comment="전화번호")
    hosp_url:       Mapped[str | None] = mapped_column(String(300),                  comment="홈페이지")
    estb_dd:        Mapped[str | None] = mapped_column(String(10),                   comment="개설일자")
    x_pos:          Mapped[float| None]= mapped_column(Float,                        comment="경도")
    y_pos:          Mapped[float| None]= mapped_column(Float,                        comment="위도")
    dr_tot_cnt:     Mapped[int | None] = mapped_column(Integer,                      comment="의사총수")
    # 의과
    mdept_gdr_cnt:  Mapped[int | None] = mapped_column(Integer, comment="의과 일반의")
    mdept_intn_cnt: Mapped[int | None] = mapped_column(Integer, comment="의과 인턴")
    mdept_resd_cnt: Mapped[int | None] = mapped_column(Integer, comment="의과 레지던트")
    mdept_sdr_cnt:  Mapped[int | None] = mapped_column(Integer, comment="의과 전문의")
    # 치과
    dety_gdr_cnt:   Mapped[int | None] = mapped_column(Integer, comment="치과 일반의")
    dety_intn_cnt:  Mapped[int | None] = mapped_column(Integer, comment="치과 인턴")
    dety_resd_cnt:  Mapped[int | None] = mapped_column(Integer, comment="치과 레지던트")
    dety_sdr_cnt:   Mapped[int | None] = mapped_column(Integer, comment="치과 전문의")
    # 한방
    hmdept_gdr_cnt:  Mapped[int | None]= mapped_column(Integer, comment="한방 일반의")
    hmdept_intn_cnt: Mapped[int | None]= mapped_column(Integer, comment="한방 인턴")
    hmdept_resd_cnt: Mapped[int | None]= mapped_column(Integer, comment="한방 레지던트")
    hmdept_sdr_cnt:  Mapped[int | None]= mapped_column(Integer, comment="한방 전문의")

    def __repr__(self) -> str:
        return f"Hospital(ykiho={self.ykiho!r}, name={self.yadm_nm!r}, type={self.cl_cd_nm!r})"


# ── 헬퍼 ──────────────────────────────────────────────────────

def _to_int(val) -> int | None:
    try:
        return int(val)
    except (TypeError, ValueError):
        return None


def _to_float(val) -> float | None:
    try:
        return float(val)
    except (TypeError, ValueError):
        return None


def _item_to_hospital(item: dict) -> Hospital:
    return Hospital(
        ykiho=item.get("ykiho", ""),
        yadm_nm=item.get("yadmNm", ""),
        cl_cd=item.get("clCd"),
        cl_cd_nm=item.get("clCdNm"),
        sido_cd_nm=item.get("sidoCdNm"),
        sggu_cd_nm=item.get("sgguCdNm"),
        emdong_nm=item.get("emdongNm"),
        addr=item.get("addr"),
        post_no=item.get("postNo"),
        telno=item.get("telno"),
        hosp_url=item.get("hospUrl"),
        estb_dd=item.get("estbDd"),
        x_pos=_to_float(item.get("XPos")),
        y_pos=_to_float(item.get("YPos")),
        dr_tot_cnt=_to_int(item.get("drTotCnt")),
        mdept_gdr_cnt=_to_int(item.get("mdeptGdrCnt")),
        mdept_intn_cnt=_to_int(item.get("mdeptIntnCnt")),
        mdept_resd_cnt=_to_int(item.get("mdeptResdCnt")),
        mdept_sdr_cnt=_to_int(item.get("mdeptSdrCnt")),
        dety_gdr_cnt=_to_int(item.get("detyGdrCnt")),
        dety_intn_cnt=_to_int(item.get("detyIntnCnt")),
        dety_resd_cnt=_to_int(item.get("detyResdCnt")),
        dety_sdr_cnt=_to_int(item.get("detySdrCnt")),
        hmdept_gdr_cnt=_to_int(item.get("hmdeptGdrCnt")),
        hmdept_intn_cnt=_to_int(item.get("hmdeptIntnCnt")),
        hmdept_resd_cnt=_to_int(item.get("hmdeptResdCnt")),
        hmdept_sdr_cnt=_to_int(item.get("hmdeptSdrCnt")),
    )


# ── API 호출 ──────────────────────────────────────────────────

def fetch_page(page_no: int) -> tuple[int, list[dict]]:
    """단일 페이지를 호출하고 (totalCount, items) 를 반환합니다."""
    params = {
        "ServiceKey": SERVICE_KEY,
        "pageNo": page_no,
        "numOfRows": PAGE_SIZE,
        "sidoCd": SIDO_CD,
        "sgguCd": SGGU_CD,
        "_type": "json",
    }
    resp = requests.get(API_URL, params=params, timeout=100)
    resp.raise_for_status()

    body = resp.json().get("response", {}).get("body", {})
    total = int(body.get("totalCount", 0))
    items = body.get("items", {})

    # 결과가 없으면 빈 리스트
    if not items:
        return total, []

    raw = items.get("item", [])
    # 단건 조회 시 dict로 내려오는 경우 처리
    if isinstance(raw, dict):
        raw = [raw]
    return total, raw


def fetch_all_hospitals() -> list[dict]:
    """전체 페이지를 순회하며 모든 병원 항목을 수집합니다."""
    if not SERVICE_KEY:
        raise EnvironmentError(".env에 SERVICE_KEY가 없습니다. 공공데이터포털에서 발급받아 추가해주세요.")

    total, first_items = fetch_page(1)
    print(f"[API] 강남구 병원 총 {total}건")

    all_items = list(first_items)
    page = 2
    while len(all_items) < total:
        time.sleep(0.2)  # API 과부하 방지
        _, items = fetch_page(page)
        if not items:
            break
        all_items.extend(items)
        print(f"  페이지 {page} 수집 중... ({len(all_items)}/{total})")
        page += 1

    return all_items


# ── DB 저장 ───────────────────────────────────────────────────

def init_db():
    Base.metadata.create_all(engine)
    print("[DB] 테이블 초기화 완료")


def save_hospitals(items: list[dict]) -> tuple[int, int]:
    """병원 목록을 저장하고 (저장 건수, 스킵 건수)를 반환합니다."""
    saved = skipped = 0
    with Session(engine) as session:
        existing_ids = {
            row[0] for row in session.execute(text("SELECT ykiho FROM hospitals_gangnam"))
        }
        for item in items:
            ykiho = item.get("ykiho", "")
            if not ykiho or ykiho in existing_ids:
                skipped += 1
                continue
            session.add(_item_to_hospital(item))
            existing_ids.add(ykiho)
            saved += 1
        session.commit()
    return saved, skipped


# ── 실행 ─────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()

    items = fetch_all_hospitals()
    saved, skipped = save_hospitals(items)
    print(f"[완료] 저장 {saved}건 / 스킵 {skipped}건 (중복)")
