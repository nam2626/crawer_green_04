"""
books.toscrape.com 1~5페이지 크롤러 + SQLAlchemy ORM 저장
- 모델: Book (title, price, rating, availability, category, url)
- 중복 url은 INSERT 시 스킵
"""
import os
import time

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from sqlalchemy import create_engine, String, Integer, Float, DateTime, func
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

# ── 모델 정의 ─────────────────────────────────────────────────

class Base(DeclarativeBase):
    pass


class Book(Base):
    __tablename__ = "books"

    id:           Mapped[int]        = mapped_column(Integer, primary_key=True, autoincrement=True)
    title:        Mapped[str]        = mapped_column(String(500), nullable=False)
    price:        Mapped[float]      = mapped_column(Float, nullable=False)
    rating:       Mapped[int]        = mapped_column(Integer, default=0)        # 1~5 (별점)
    availability: Mapped[str]        = mapped_column(String(50))
    category:     Mapped[str | None] = mapped_column(String(100))
    url:          Mapped[str]        = mapped_column(String(700), unique=True)
    created_at:   Mapped[DateTime]   = mapped_column(DateTime, server_default=func.now())

    def __repr__(self) -> str:
        return f"Book(id={self.id}, title={self.title!r}, price={self.price}, rating={self.rating})"


# ── 초기화 ────────────────────────────────────────────────────

def init_db():
    Base.metadata.create_all(engine)
    print("[DB] 테이블 초기화 완료")


# ── 크롤링 ────────────────────────────────────────────────────

BASE_URL = "https://books.toscrape.com/catalogue"

RATING_MAP = {
    "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5,
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}


def fetch_page(page: int) -> list[dict]:
    """한 페이지의 책 정보를 파싱해서 dict 리스트로 반환합니다."""
    url = f"{BASE_URL}/page-{page}.html"
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    books = []

    for article in soup.select("article.product_pod"):
        # 제목
        title = article.select_one("h3 > a")["title"]

        # 가격 (£ 기호 제거 후 float 변환)
        price_text = article.select_one("p.price_color").text.strip()
        price = float(price_text.replace("£", "").replace("Â", "").strip())

        # 별점 (class 속성에서 추출: "star-rating Three" → 3)
        rating_class = article.select_one("p.star-rating")["class"]  # ['star-rating', 'Three']
        rating = RATING_MAP.get(rating_class[1], 0)

        # 재고 상태
        availability = article.select_one("p.availability").text.strip()

        # 상세 페이지 URL
        href = article.select_one("h3 > a")["href"]
        book_url = f"{BASE_URL}/{href.replace('../', '')}"

        books.append({
            "title": title,
            "price": price,
            "rating": rating,
            "availability": availability,
            "url": book_url,
        })

    return books


def crawl(pages: int = 5) -> list[dict]:
    """1~pages 페이지를 순서대로 크롤링합니다."""
    all_books: list[dict] = []
    for page in range(1, pages + 1):
        print(f"[크롤링] {page}/{pages} 페이지 수집 중...")
        books = fetch_page(page)
        all_books.extend(books)
        print(f"  → {len(books)}권 수집")
        time.sleep(0.5)   # 서버 부하 방지
    print(f"[크롤링] 총 {len(all_books)}권 수집 완료")
    return all_books


# ── 저장 ─────────────────────────────────────────────────────

def save_books(books: list[dict]) -> int:
    """중복 URL을 스킵하고 새 책만 저장합니다. 저장 건수를 반환합니다."""
    saved = 0
    with Session(engine) as session:
        # 기존 URL을 모두 조회해서 집합으로 만듭니다.
        existing_urls = {row[0] for row in session.query(Book.url).all()}
        # 새로운 책 중에서 URL이 중복되지 않는 것만 필터링해서 저장합니다.
        new_books = [Book(**b) for b in books if b["url"] not in existing_urls]
        session.add_all(new_books)
        session.commit()
        saved = len(new_books)

    skipped = len(books) - saved
    print(f"[DB] {saved}건 저장 ({skipped}건 중복 스킵)")
    return saved


# ── 조회 ─────────────────────────────────────────────────────

def get_all_books(limit: int = 20) -> list[Book]:
    with Session(engine) as session:
        return session.query(Book).order_by(Book.price.asc()).limit(limit).all()


def get_stats() -> dict:
    with Session(engine) as session:
        total, avg_price, avg_rating = session.query(
            func.count(Book.id),
            func.avg(Book.price),
            func.avg(Book.rating),
        ).one()
        return {
            "total": total,
            "avg_price": round(float(avg_price or 0), 2),
            "avg_rating": round(float(avg_rating or 0), 2),
        }


# ── 실행 ─────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()

    # 1~5페이지 크롤링
    books = crawl(pages=5)

    # MySQL 저장
    save_books(books)

    # 결과 확인
    print("\n[가격 낮은 순 TOP 10]")
    for book in get_all_books(limit=10):
        stars = "★" * book.rating + "☆" * (5 - book.rating)
        print(f"  {stars}  GBP {book.price:<6}  {book.title}")

    stats = get_stats()
    print(
        f"\n[통계] 총 {stats['total']}권 / "
        f"평균 가격 GBP {stats['avg_price']} / "
        f"평균 별점 {stats['avg_rating']}"
    )
