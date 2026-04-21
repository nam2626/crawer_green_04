"""
MySQL CRUD 패턴 — 실무에서 바로 쓰는 함수 구조
- Create (INSERT)
- Read (SELECT)
- Update (UPDATE)
- Delete (DELETE)
"""
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

# DB 연결 설정을 한 곳에서 관리합니다.
DB_CONFIG = {
    "host":        os.getenv("DB_HOST", "localhost"),
    "port":        int(os.getenv("DB_PORT", 3306)),
    "db":          os.getenv("DB_NAME", "crawler_db"),
    "user":        os.getenv("DB_USER", "root"),
    "password":    os.getenv("DB_PASSWORD", ""),
    "charset":     "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
}


def get_conn():
    print(DB_CONFIG)
    """DB 연결을 반환하는 팩토리 함수"""
    return pymysql.connect(**DB_CONFIG)


# ── 초기화 ────────────────────────────────────────────────────

def init_db():
    """테이블 생성"""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS posts (
                    id         INT           AUTO_INCREMENT PRIMARY KEY,
                    title      VARCHAR(500)  NOT NULL,
                    url        VARCHAR(700) UNIQUE,
                    views      INT           DEFAULT 0,
                    category   VARCHAR(100),
                    created_at TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
                ) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci
            """)
        conn.commit()
        
    print("테이블 초기화 완료")


# ── 저장 (CREATE) ─────────────────────────────────────────────

def save_posts(posts):
    """
    게시글 여러 개를 한 번에 저장합니다.
    INSERT IGNORE: 중복되는 URL은 무시 (스킵)하고, 새로운 항목만 저장합니다.
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.executemany(
                "INSERT IGNORE INTO posts (title, url, views, category) VALUES (%s, %s, %s, %s)",
                [(p["title"], p["url"], p.get("views", 0), p.get("category")) for p in posts]
            )
            saved = cur.rowcount  # 실제 삽입된 행 수
        conn.commit()
        # conn.rollback()  # 트랜잭션 롤백 (테스트용)
    print(f"{saved}건 저장 ({len(posts) - saved}건 중복 스킵)")
    return saved


# ── 조회 (READ) ───────────────────────────────────────────────

def get_all_posts(limit=20):
    """
    조회수 기준 상위 게시글을 조회합니다.
    LIMIT: 반환할 최대 행의 개수를 제한합니다.
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM posts ORDER BY views DESC LIMIT %s", (limit,))
            return cur.fetchall()


def get_posts_by_category(category):
    """카테고리별로 게시글을 필터링해서 조회합니다."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM posts WHERE category = %s ORDER BY views DESC",
                (category,)
            )
            return cur.fetchall()


def get_stats():
    """전체 게시글 통계 (개수, 평균 조회수, 최대 조회수)를 조회합니다."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            # COUNT(): 행의 개수, AVG(): 평균, MAX(): 최댓값
            cur.execute("SELECT COUNT(*) AS total, AVG(views) AS avg_views, MAX(views) AS max_views FROM posts")
            return cur.fetchone()


# ── 수정 / 삭제 (UPDATE / DELETE) ─────────────────────────────

def update_views(url, new_views):
    """특정 URL의 게시글 조회수를 업데이트합니다."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE posts SET views = %s WHERE url = %s", (new_views, url))
        conn.commit()


def delete_post(url):
    """특정 URL의 게시글을 삭제합니다."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM posts WHERE url = %s", (url,))
        conn.commit()


# ── 실행 ─────────────────────────────────────────────────────

init_db()

# 1차 저장: 3개 게시글
save_posts([
    {"title": "Python 크롤링 입문", "url": "https://example.com/1", "views": 1500, "category": "기술"},
    {"title": "DB 연동하기",        "url": "https://example.com/2", "views": 2300, "category": "기술"},
    {"title": "CSS 기초",            "url": "https://example.com/3", "views": 450,  "category": "디자인"},
])

# 2차 저장: 첫 번째 게시글은 URL 중복으로 스킵, 새 게시글만 저장
save_posts([
    {"title": "Python 크롤링 입문", "url": "https://example.com/1", "views": 1500},
    {"title": "React 훅 완벽정리",  "url": "https://example.com/4", "views": 3100, "category": "프론트엔드"},
])

print("\n[전체 조회]")
for post in get_all_posts():
    print(f"  [{post['category']}] {post['title']} — {post['views']}회")

print("\n[기술 카테고리]")
for post in get_posts_by_category("기술"):
    print(f"  {post['title']}")

stats = get_stats()
print(f"\n[통계] 총 {stats['total']}건 / 평균 {int(stats['avg_views'])}회 / 최고 {stats['max_views']}회")

# 첫 번째 게시글 조회수를 9999로 업데이트
update_views("https://example.com/1", 9999)
print("\n[UPDATE] 조회수 9999로 변경 완료")

# CSS 기초 게시글 삭제
delete_post("https://example.com/3")
print("[DELETE] CSS 기초 삭제 완료")

# 정리
# with get_conn() as conn:
#     with conn.cursor() as cur:
#         cur.execute("DROP TABLE IF EXISTS posts")
#     conn.commit()
