import aiosqlite
import pytz
from datetime import datetime

tz = pytz.timezone('Asia/Tashkent')

DB_NAME = "vakto.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                user_id INTEGER PRIMARY KEY,
                full_name TEXT,
                birth_date TEXT,
                salary REAL,
                phone TEXT
            );
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS shifts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                start_time TEXT,
                end_time TEXT
            );
        """)
        await db.commit()
        import aiosqlite
from datetime import datetime, timedelta

DB_NAME = "vakto.db"

# 🟢 Базани инициализация қилиш
async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                user_id INTEGER PRIMARY KEY,
                full_name TEXT,
                birth_date TEXT,
                salary REAL,
                phone TEXT
            );
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS shifts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                start_time TEXT,
                end_time TEXT
            );
        """)
        await db.commit()

# 👤 Ходимни рўйхатдан ўтказиш
async def add_employee(user_id, full_name, birth_date, salary, phone):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT OR REPLACE INTO employees (user_id, full_name, birth_date, salary, phone)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, full_name, birth_date, salary, phone))
        await db.commit()

# 🕒 Смена бошлаш
async def add_shift_start(user_id):
    now = datetime.now().isoformat()
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT INTO shifts (user_id, start_time)
            VALUES (?, ?)
        """, (user_id, now))
        await db.commit()

# 🕔 Смена тугатиш
async def add_shift_end(user_id):
    now = datetime.now().isoformat()
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            UPDATE shifts
            SET end_time = ?
            WHERE user_id = ? AND end_time IS NULL
        """, (now, user_id))
        await db.commit()

# 📋 Барча ходимларни олиш
async def get_all_employees():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM employees")
        return await cursor.fetchall()

# 📊 Ҳисобот тайёрлаш
async def get_shifts_report():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
            SELECT e.full_name, s.start_time, s.end_time
            FROM shifts s
            JOIN employees e ON s.user_id = e.user_id
            WHERE s.start_time >= ?
        """, ((datetime.now() - timedelta(days=7)).isoformat(),))
        shifts = await cursor.fetchall()

    report = "📝 Ҳисобот (сўнгги 7 кун):\n\n"
    for full_name, start, end in shifts:
        start_time = datetime.fromisoformat(start).strftime('%Y-%m-%d %H:%M')
        end_time = datetime.fromisoformat(end).strftime('%Y-%m-%d %H:%M') if end else "⏳ Очиқ"
        report += f"👤 {full_name}\n🕒 Бошланди: {start_time}\n🕔 Тугади: {end_time}\n\n"
    return report