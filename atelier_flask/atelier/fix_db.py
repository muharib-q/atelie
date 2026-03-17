# Запусти этот файл ОДИН РАЗ чтобы починить базу данных
# python fix_db.py

import sqlite3, os

# Найди database.db в папке atelier
db_path = 'database.db'

conn = sqlite3.connect(db_path)

# Проверяем какие столбцы есть
cols = [row[1] for row in conn.execute("PRAGMA table_info(bookings)").fetchall()]
print("Текущие столбцы:", cols)

# Добавляем недостающие столбцы
missing = {
    'booking_date': 'TEXT',
    'booking_time': 'TEXT', 
    'last_name':    'TEXT',
    'comment':      'TEXT',
    'status':       "TEXT DEFAULT 'новая'",
}

for col, typ in missing.items():
    if col not in cols:
        conn.execute(f'ALTER TABLE bookings ADD COLUMN {col} {typ}')
        print(f'✅ Добавлен столбец: {col}')
    else:
        print(f'☑️  Уже есть: {col}')

conn.commit()
conn.close()
print('\n✅ База данных исправлена! Теперь запусти app.py снова.')
