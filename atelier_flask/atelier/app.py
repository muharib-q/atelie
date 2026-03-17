from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3, os

app = Flask(__name__)
app.secret_key = 'atelier_shik_secret_2024'

# /tmp не сбрасывается между запросами на Render
DB_PATH = '/tmp/atelier.db'

ICONS = {
    'sewing': '<svg viewBox="0 0 48 48" fill="none" width="44" height="44"><path d="M8 40L20 16L32 28L24 44" stroke="#C9A84C" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/><circle cx="36" cy="12" r="5" stroke="#C9A84C" stroke-width="2.5"/><path d="M31 12H8" stroke="#C9A84C" stroke-width="2.5" stroke-linecap="round"/><circle cx="36" cy="12" r="2" fill="#C9A84C"/></svg>',
    'scissors': '<svg viewBox="0 0 48 48" fill="none" width="44" height="44"><circle cx="14" cy="34" r="6" stroke="#C9A84C" stroke-width="2.5"/><circle cx="14" cy="14" r="6" stroke="#C9A84C" stroke-width="2.5"/><path d="M18.5 29.5L38 10" stroke="#C9A84C" stroke-width="2.5" stroke-linecap="round"/><path d="M18.5 18.5L38 38" stroke="#C9A84C" stroke-width="2.5" stroke-linecap="round"/></svg>',
    'ring': '<svg viewBox="0 0 48 48" fill="none" width="44" height="44"><circle cx="24" cy="30" r="12" stroke="#C9A84C" stroke-width="2.5"/><path d="M18 30 Q24 20 30 30" stroke="#C9A84C" stroke-width="2.5" stroke-linecap="round"/><rect x="20" y="6" width="8" height="4" rx="1" stroke="#C9A84C" stroke-width="2" fill="none"/><polygon points="24,8 27,16 21,16" fill="#C9A84C"/></svg>',
    'flower': '<svg viewBox="0 0 48 48" fill="none" width="44" height="44"><circle cx="24" cy="24" r="5" fill="#C9A84C"/><ellipse cx="24" cy="12" rx="4" ry="7" fill="none" stroke="#C9A84C" stroke-width="2.5"/><ellipse cx="24" cy="36" rx="4" ry="7" fill="none" stroke="#C9A84C" stroke-width="2.5"/><ellipse cx="12" cy="24" rx="7" ry="4" fill="none" stroke="#C9A84C" stroke-width="2.5"/><ellipse cx="36" cy="24" rx="7" ry="4" fill="none" stroke="#C9A84C" stroke-width="2.5"/></svg>',
    'camera': '<svg viewBox="0 0 48 48" fill="none" width="44" height="44"><rect x="6" y="16" width="36" height="26" rx="4" stroke="#C9A84C" stroke-width="2.5"/><circle cx="24" cy="29" r="7" stroke="#C9A84C" stroke-width="2.5"/><path d="M16 16l3-6h10l3 6" stroke="#C9A84C" stroke-width="2.5" stroke-linejoin="round"/><circle cx="38" cy="22" r="2" fill="#C9A84C"/></svg>',
    'shirt': '<svg viewBox="0 0 48 48" fill="none" width="44" height="44"><path d="M16 6L6 14l4 4 4-2v26h20V16l4 2 4-4-10-8" stroke="#C9A84C" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M16 6 Q24 12 32 6" stroke="#C9A84C" stroke-width="2.5" stroke-linecap="round"/></svg>',
}

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, description TEXT,
            price TEXT NOT NULL, unit TEXT, icon TEXT);
        CREATE TABLE IF NOT EXISTS masters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL, initials TEXT NOT NULL,
            specialization TEXT, experience INTEGER, bio TEXT);
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL, last_name TEXT,
            phone TEXT NOT NULL, service TEXT NOT NULL,
            booking_date TEXT, booking_time TEXT, comment TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT "новая");
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            initials TEXT NOT NULL, name TEXT NOT NULL,
            text TEXT NOT NULL, rating INTEGER DEFAULT 5);
    ''')
    if conn.execute('SELECT COUNT(*) FROM services').fetchone()[0] == 0:
        conn.executemany('INSERT INTO services(name,description,price,unit,icon) VALUES(?,?,?,?,?)', [
            ('Индивидуальный пошив','Создаём изделия по вашим меркам и эскизам. Платья, костюмы, блузки, юбки — любые фасоны.','от 1 500 ₽','/ изделие','sewing'),
            ('Ремонт и переделка','Ушить, выпустить, заменить молнию, укоротить — быстро и аккуратно на профессиональном оборудовании.','от 300 ₽','/ работа','scissors'),
            ('Свадебные наряды','Пошив и подгонка свадебных платьев с учётом всех ваших пожеланий. Реставрация и украшение.','от 5 000 ₽','/ наряд','ring'),
            ('Вышивка и декор','Именная вышивка, нашивки, декоративные элементы — украсим любое изделие.','от 500 ₽','/ работа','flower'),
            ('Пошив по фото','Привезите любимый образ из интернета или журнала — воплотим его в жизнь точь-в-точь.','от 2 000 ₽','/ изделие','camera'),
            ('Корпоративная одежда','Пошив форменной и рабочей одежды для компаний. Скидки на оптовые заказы.','от 1 200 ₽','/ единица','shirt'),
        ])
    if conn.execute('SELECT COUNT(*) FROM masters').fetchone()[0] == 0:
        conn.executemany('INSERT INTO masters(full_name,initials,specialization,experience,bio) VALUES(?,?,?,?,?)', [
            ('Зухра Ибрагимова','ЗИ','Главный мастер',15,'15 лет опыта. Специализация — вечерние и свадебные наряды. Участник выставок моды СКФО.'),
            ('Фатима Дзугаева','ФД','Мастер по ремонту',8,'8 лет опыта. Быстрый и аккуратный ремонт одежды любой сложности. Специализация — кожа и джинс.'),
            ('Мадина Хапаева','МХ','Мастер по пошиву',6,'6 лет опыта. Индивидуальный пошив и корпоративная одежда. Точные выкройки по меркам.'),
        ])
    if conn.execute('SELECT COUNT(*) FROM reviews').fetchone()[0] == 0:
        conn.executemany('INSERT INTO reviews(initials,name,text,rating) VALUES(?,?,?,?)', [
            ('АК','Амина Карданова','Заказывала свадебное платье — результат превзошёл все ожидания! Учли каждую мелочь, платье сидело идеально.',5),
            ('ЛМ','Лейла Мусаева','Отличная мастерская! Сдала джинсы на ушивку — сделали за 2 часа, цена разумная. Теперь только сюда хожу.',5),
            ('РБ','Руслан Байрамуков','Заказывал корпоративную форму для 15 сотрудников. Всё сделано качественно и в срок. Работаем уже 3-й год!',5),
        ])
    conn.commit()
    conn.close()

# Вызывается ВСЕГДА при старте — и через python app.py и через gunicorn
init_db()

@app.route('/')
def index():
    conn = get_db()
    services = conn.execute('SELECT * FROM services').fetchall()
    masters  = conn.execute('SELECT * FROM masters').fetchall()
    reviews  = conn.execute('SELECT * FROM reviews').fetchall()
    conn.close()
    return render_template('index.html', services=services, masters=masters, reviews=reviews, icons=ICONS)

@app.route('/booking', methods=['POST'])
def booking():
    fname = request.form.get('first_name','').strip()
    phone = request.form.get('phone','').strip()
    svc   = request.form.get('service','').strip()
    if not fname or not phone or not svc:
        flash('Заполните имя, телефон и выберите услугу', 'error')
        return redirect(url_for('index') + '#booking')
    conn = get_db()
    conn.execute(
        'INSERT INTO bookings(first_name,last_name,phone,service,booking_date,booking_time,comment) VALUES(?,?,?,?,?,?,?)',
        (fname, request.form.get('last_name',''), phone, svc,
         request.form.get('booking_date',''), request.form.get('booking_time',''),
         request.form.get('comment','')))
    conn.commit()
    conn.close()
    flash('success', 'success')
    return redirect(url_for('index') + '#booking')

@app.route('/admin')
def admin():
    conn = get_db()
    bookings = conn.execute('SELECT * FROM bookings ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('admin.html', bookings=bookings)

@app.route('/admin/delete/<int:bid>', methods=['POST'])
def delete_booking(bid):
    conn = get_db()
    conn.execute('DELETE FROM bookings WHERE id=?', (bid,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/admin/status/<int:bid>', methods=['POST'])
def update_status(bid):
    conn = get_db()
    conn.execute('UPDATE bookings SET status=? WHERE id=?',
                 (request.form.get('status','новая'), bid))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
