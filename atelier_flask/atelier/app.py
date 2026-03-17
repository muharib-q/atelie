from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'atelier_shik_secret_2024'

# Хранение данных прямо в памяти — работает на любом хостинге
BOOKINGS = []
BOOKING_ID = [1]

SERVICES = [
    {'id':1,'name':'Индивидуальный пошив','description':'Создаём изделия по вашим меркам и эскизам. Платья, костюмы, блузки, юбки — любые фасоны.','price':'от 1 500 ₽','unit':'/ изделие','icon':'sewing'},
    {'id':2,'name':'Ремонт и переделка','description':'Ушить, выпустить, заменить молнию, укоротить — быстро и аккуратно на профессиональном оборудовании.','price':'от 300 ₽','unit':'/ работа','icon':'scissors'},
    {'id':3,'name':'Свадебные наряды','description':'Пошив и подгонка свадебных платьев с учётом всех ваших пожеланий. Реставрация и украшение.','price':'от 5 000 ₽','unit':'/ наряд','icon':'ring'},
    {'id':4,'name':'Вышивка и декор','description':'Именная вышивка, нашивки, декоративные элементы — украсим любое изделие.','price':'от 500 ₽','unit':'/ работа','icon':'flower'},
    {'id':5,'name':'Пошив по фото','description':'Привезите любимый образ из интернета или журнала — воплотим его в жизнь точь-в-точь.','price':'от 2 000 ₽','unit':'/ изделие','icon':'camera'},
    {'id':6,'name':'Корпоративная одежда','description':'Пошив форменной и рабочей одежды для компаний. Скидки на оптовые заказы.','price':'от 1 200 ₽','unit':'/ единица','icon':'shirt'},
]

MASTERS = [
    {'id':1,'full_name':'Зухра Ибрагимова','initials':'ЗИ','specialization':'Главный мастер','experience':15,'bio':'15 лет опыта. Специализация — вечерние и свадебные наряды. Участник выставок моды СКФО.'},
    {'id':2,'full_name':'Фатима Дзугаева','initials':'ФД','specialization':'Мастер по ремонту','experience':8,'bio':'8 лет опыта. Быстрый и аккуратный ремонт одежды любой сложности. Специализация — кожа и джинс.'},
    {'id':3,'full_name':'Мадина Хапаева','initials':'МХ','specialization':'Мастер по пошиву','experience':6,'bio':'6 лет опыта. Индивидуальный пошив и корпоративная одежда. Точные выкройки по меркам.'},
]

REVIEWS = [
    {'id':1,'initials':'АК','name':'Амина Карданова','text':'Заказывала свадебное платье — результат превзошёл все ожидания! Учли каждую мелочь, платье сидело идеально.','rating':5},
    {'id':2,'initials':'ЛМ','name':'Лейла Мусаева','text':'Отличная мастерская! Сдала джинсы на ушивку — сделали за 2 часа, цена разумная. Теперь только сюда хожу.','rating':5},
    {'id':3,'initials':'РБ','name':'Руслан Байрамуков','text':'Заказывал корпоративную форму для 15 сотрудников. Всё сделано качественно и в срок. Работаем уже 3-й год!','rating':5},
]

ICONS = {
    'sewing': '<svg viewBox="0 0 48 48" fill="none" width="44" height="44"><path d="M8 40L20 16L32 28L24 44" stroke="#C9A84C" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/><circle cx="36" cy="12" r="5" stroke="#C9A84C" stroke-width="2.5"/><path d="M31 12H8" stroke="#C9A84C" stroke-width="2.5" stroke-linecap="round"/><circle cx="36" cy="12" r="2" fill="#C9A84C"/></svg>',
    'scissors': '<svg viewBox="0 0 48 48" fill="none" width="44" height="44"><circle cx="14" cy="34" r="6" stroke="#C9A84C" stroke-width="2.5"/><circle cx="14" cy="14" r="6" stroke="#C9A84C" stroke-width="2.5"/><path d="M18.5 29.5L38 10" stroke="#C9A84C" stroke-width="2.5" stroke-linecap="round"/><path d="M18.5 18.5L38 38" stroke="#C9A84C" stroke-width="2.5" stroke-linecap="round"/></svg>',
    'ring': '<svg viewBox="0 0 48 48" fill="none" width="44" height="44"><circle cx="24" cy="30" r="12" stroke="#C9A84C" stroke-width="2.5"/><path d="M18 30 Q24 20 30 30" stroke="#C9A84C" stroke-width="2.5" stroke-linecap="round"/><rect x="20" y="6" width="8" height="4" rx="1" stroke="#C9A84C" stroke-width="2" fill="none"/><polygon points="24,8 27,16 21,16" fill="#C9A84C"/></svg>',
    'flower': '<svg viewBox="0 0 48 48" fill="none" width="44" height="44"><circle cx="24" cy="24" r="5" fill="#C9A84C"/><ellipse cx="24" cy="12" rx="4" ry="7" fill="none" stroke="#C9A84C" stroke-width="2.5"/><ellipse cx="24" cy="36" rx="4" ry="7" fill="none" stroke="#C9A84C" stroke-width="2.5"/><ellipse cx="12" cy="24" rx="7" ry="4" fill="none" stroke="#C9A84C" stroke-width="2.5"/><ellipse cx="36" cy="24" rx="7" ry="4" fill="none" stroke="#C9A84C" stroke-width="2.5"/></svg>',
    'camera': '<svg viewBox="0 0 48 48" fill="none" width="44" height="44"><rect x="6" y="16" width="36" height="26" rx="4" stroke="#C9A84C" stroke-width="2.5"/><circle cx="24" cy="29" r="7" stroke="#C9A84C" stroke-width="2.5"/><path d="M16 16l3-6h10l3 6" stroke="#C9A84C" stroke-width="2.5" stroke-linejoin="round"/><circle cx="38" cy="22" r="2" fill="#C9A84C"/></svg>',
    'shirt': '<svg viewBox="0 0 48 48" fill="none" width="44" height="44"><path d="M16 6L6 14l4 4 4-2v26h20V16l4 2 4-4-10-8" stroke="#C9A84C" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M16 6 Q24 12 32 6" stroke="#C9A84C" stroke-width="2.5" stroke-linecap="round"/></svg>',
}

@app.route('/')
def index():
    return render_template('index.html',
                           services=SERVICES,
                           masters=MASTERS,
                           reviews=REVIEWS,
                           icons=ICONS)

@app.route('/booking', methods=['POST'])
def booking():
    fname = request.form.get('first_name','').strip()
    phone = request.form.get('phone','').strip()
    svc   = request.form.get('service','').strip()
    if not fname or not phone or not svc:
        flash('Заполните имя, телефон и выберите услугу', 'error')
        return redirect(url_for('index') + '#booking')
    
    booking = {
        'id': BOOKING_ID[0],
        'first_name': fname,
        'last_name': request.form.get('last_name',''),
        'phone': phone,
        'service': svc,
        'booking_date': request.form.get('booking_date',''),
        'booking_time': request.form.get('booking_time',''),
        'comment': request.form.get('comment',''),
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'status': 'новая'
    }
    BOOKINGS.append(booking)
    BOOKING_ID[0] += 1
    
    flash('success', 'success')
    return redirect(url_for('index') + '#booking')

@app.route('/admin')
def admin():
    return render_template('admin.html', bookings=list(reversed(BOOKINGS)))

@app.route('/admin/delete/<int:bid>', methods=['POST'])
def delete_booking(bid):
    global BOOKINGS
    BOOKINGS = [b for b in BOOKINGS if b['id'] != bid]
    return redirect(url_for('admin'))

@app.route('/admin/status/<int:bid>', methods=['POST'])
def update_status(bid):
    status = request.form.get('status','новая')
    for b in BOOKINGS:
        if b['id'] == bid:
            b['status'] = status
            break
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
