"""
SQLAlchemy ORM CRUD 패턴
- ORM: 테이블 → Python 클래스, 행 → 객체로 다룹니다.
- Create / Read / Update / Delete
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, String, Integer, DateTime, func
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


class Post(Base):
    __tablename__ = "posts_orm"

    id:         Mapped[int]          = mapped_column(Integer, primary_key=True, autoincrement=True)
    title:      Mapped[str]          = mapped_column(String(500), nullable=False)
    url:        Mapped[str | None]   = mapped_column(String(700), unique=True)
    views:      Mapped[int]          = mapped_column(Integer, default=0)
    category:   Mapped[str | None]   = mapped_column(String(100))
    created_at: Mapped[DateTime]     = mapped_column(DateTime, server_default=func.now())

    def __repr__(self) -> str:
        return f"Post(id={self.id}, title={self.title!r}, views={self.views})"


# ── 초기화 ────────────────────────────────────────────────────

def init_db():
    """테이블이 없으면 생성합니다."""
    Base.metadata.create_all(engine)
    print("테이블 초기화 완료")


# ── CREATE ────────────────────────────────────────────────────

def create_post(title: str, url: str, views: int = 0, category: str = None) -> Post:
    """게시글 1건을 저장하고 반환합니다."""
    with Session(engine) as session:
        post = Post(title=title, url=url, views=views, category=category)
        session.add(post)
        session.commit()
        session.refresh(post)   # DB에서 auto-increment ID 등을 다시 읽어옵니다.
        print(f"[CREATE] {post}")
        return post


def create_posts(posts: list[dict]) -> int:
    """게시글 여러 개를 한 번에 저장합니다. 중복 URL은 스킵합니다."""
    saved = 0
    with Session(engine) as session:
        for p in posts:
            # URL 중복 여부를 먼저 확인합니다.
            exists = session.query(Post).filter_by(url=p["url"]).first()
            if exists:
                continue
            session.add(Post(**p))
            saved += 1
        session.commit()
    skipped = len(posts) - saved
    print(f"[CREATE] {saved}건 저장 ({skipped}건 중복 스킵)")
    return saved


# ── READ ─────────────────────────────────────────────────────

def get_all_posts(limit: int = 20) -> list[Post]:
    """조회수 내림차순으로 게시글 목록을 반환합니다."""
    with Session(engine) as session:
        return session.query(Post).order_by(Post.views.desc()).limit(limit).all()


def get_posts_by_category(category: str) -> list[Post]:
    """카테고리로 필터링한 게시글 목록을 반환합니다."""
    with Session(engine) as session:
        return session.query(Post).filter(Post.category == category).order_by(Post.views.desc()).all()


def get_post_by_url(url: str) -> Post | None:
    """URL로 게시글 1건을 조회합니다. 없으면 None을 반환합니다."""
    with Session(engine) as session:
        return session.query(Post).filter_by(url=url).first()


def get_stats() -> dict:
    """전체 통계 (총 건수, 평균 조회수, 최대 조회수)를 반환합니다."""
    with Session(engine) as session:
        total, avg_views, max_views = session.query(
            func.count(Post.id),
            func.avg(Post.views),
            func.max(Post.views),
        ).one()
        return {"total": total, "avg_views": avg_views, "max_views": max_views}


# ── UPDATE ────────────────────────────────────────────────────

def update_views(url: str, new_views: int) -> bool:
    """특정 URL 게시글의 조회수를 변경합니다. 성공 시 True를 반환합니다."""
    with Session(engine) as session:
        post = session.query(Post).filter_by(url=url).first()
        if not post:
            print(f"[UPDATE] URL을 찾을 수 없습니다: {url}")
            return False
        post.views = new_views
        session.commit()
        print(f"[UPDATE] {post.title!r} → 조회수 {new_views}")
        return True


# ── DELETE ────────────────────────────────────────────────────

def delete_post(url: str) -> bool:
    """특정 URL 게시글을 삭제합니다. 성공 시 True를 반환합니다."""
    with Session(engine) as session:
        post = session.query(Post).filter_by(url=url).first()
        if not post:
            print(f"[DELETE] URL을 찾을 수 없습니다: {url}")
            return False
        title = post.title
        session.delete(post)
        session.commit()
        print(f"[DELETE] {title!r} 삭제 완료")
        return True


# ── 실행 ─────────────────────────────────────────────────────

init_db()

# CREATE: 단건
create_post("Python 크롤링 입문", "https://example.com/orm/1", views=1500, category="기술")
create_post("DB 연동하기",        "https://example.com/orm/2", views=2300, category="기술")
create_post("CSS 기초",            "https://example.com/orm/3", views=450,  category="디자인")

# CREATE: 다건 (URL 중복 스킵 포함)
create_posts([
    {"title": "Python 크롤링 입문", "url": "https://example.com/orm/1", "views": 1500},  # 중복 → 스킵
    {"title": "React 훅 완벽정리",  "url": "https://example.com/orm/4", "views": 3100, "category": "프론트엔드"},
])

# READ: 전체 조회
print("\n[전체 조회]")
for post in get_all_posts():
    print(f"  [{post.category}] {post.title} — {post.views}회")

# READ: 카테고리 필터
print("\n[기술 카테고리]")
for post in get_posts_by_category("기술"):
    print(f"  {post.title}")

# READ: 통계
stats = get_stats()
avg = int(stats["avg_views"]) if stats["avg_views"] else 0
print(f"\n[통계] 총 {stats['total']}건 / 평균 {avg}회 / 최고 {stats['max_views']}회")

# UPDATE
update_views("https://example.com/orm/1", 9999)

# DELETE
delete_post("https://example.com/orm/3")

# 최종 확인
print("\n[최종 목록]")
for post in get_all_posts():
    print(f"  {post}")

# 테이블 초기화 (필요 시 주석 해제)
# Base.metadata.drop_all(engine)
