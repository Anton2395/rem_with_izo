from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from sqlalchemy_utils.types.choice import ChoiceType
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import check_password_hash
from settings import DB
from sqlalchemy.schema import MetaData, Table
from passlib.hash import django_pbkdf2_sha256


# БД
#######################################################
# engine = create_engine('sqlite:///test.db', connect_args={'check_same_thread': False}, echo=False)
engine = create_engine('postgresql+psycopg2://' + DB['user'] + ':' + DB['pass'] + '@' + DB['host'] + '/' + DB['dbName'], pool_size=20, max_overflow=0)
base = declarative_base()


class Connections(base):
    __tablename__ = 'connections'
    id = Column(Integer(), primary_key=True)
    switch = Column(Boolean, default=True, nullable=False)
    driver = Column(String(128), nullable=False)
    name = Column(String(128), nullable=False)
    ip = Column(String(128), nullable=False)
    port = Column(Integer, nullable=False)
    rack = Column(Integer, nullable=False)
    slot = Column(Integer, nullable=False)
    arrays = Column(String(128), nullable=False)
    DB = Column(Integer, nullable=False)
    start = Column(Integer, nullable=False)
    offset = Column(Integer, nullable=False)
    listvalue = relationship("ListValue", cascade="all, delete")
    status = Column(Boolean, default=None, nullable=True)


class ListValue(base):
    TYPES = [
        ('int', 'int'),
        ('real', 'real'),
        ('bool', 'bool'),
        ('double', 'double')
    ]

    __tablename__ = 'listvalue'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    start = Column(Integer, nullable=False)
    type_value = Column(ChoiceType(TYPES))
    type_table = Column(ChoiceType(TYPES))
    connections_id = Column(Integer, ForeignKey('connections.id'))
    divide = Column(Boolean, default=False)
    divide_number = Column(Integer, nullable=True)
    if_change = Column(Boolean, default=False)
    byte_bind = Column(Integer, nullable=False)
    bit_bind = Column(Integer, nullable=False)
    alarms = relationship("Alarms", cascade="all, delete")
    polling_time = Column(Integer, nullable=True, default=1)
    rewrite_time = Column(Integer, nullable=True, default=10)


    def get_name_alarm(self):
        session = Session()
        a = session.query(Alarms).get(self.alarms_id)
        if a == None:
            a = "Нет связи"
        else:
            a = session.query(Alarms).get(self.alarms_id).text_alarm_id
            a = session.query(Text_Alarm).get(a).name
        return a


class Alarms(base):
    __tablename__ = 'alarms'

    id = Column(Integer, primary_key=True)
    value_list_id = Column(Integer, ForeignKey('listvalue.id'))
    bit = Column(Integer, nullable=False)
    text_alarm_id = Column(Integer, ForeignKey('text_alarm.id'))
    Value = relationship('ListValue', cascade='save-update')


class Text_Alarm(base):
    __tablename__ = 'text_alarm'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    alarm = relationship("Alarms", cascade="all, delete")


# class User(base, UserMixin):
#     __tablename__ = 'user'
#     id = Column(Integer, primary_key=True)
#     login = Column(String, nullable=False, unique=True)
#     password = Column(String, nullable=False)

metadata = MetaData(bind=engine)

class User(base, UserMixin):
    __table__ = Table('users_userp', metadata, autoload=True)





base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
##########################################################################


app = Flask('opc', static_url_path='', static_folder='web/static', template_folder='web/template')
app.secret_key = 'kldjalksdjio23poekl2op3k-d3-0980qdwkslajsd89234'
manager = LoginManager(app)
connections = []



@manager.user_loader
def load_user(user_id):
    ses = Session()
    return ses.query(User).get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')
    ses = Session()
    if login and password:
        user = ses.query(User).filter_by(username=login).first()

        if user and django_pbkdf2_sha256.verify(password, user.password):#check_password_hash(user.password, password):
            login_user(user)

            next_page = request.args.get('next')
            try:
                return redirect(next_page)
            except:
                return redirect(url_for('main'))
        else:
            flash('neverno')
    else:
        flash('zapolnite polya')
    ses.close()
    return render_template('login.html')



@app.route('/status/<int:id_status>', methods=['GET'])
def status(id_status):
    session = Session()
    con_data = session.query(Connections).get(id_status)
    if con_data.status == None:
        data = '#696969'
    if con_data.status == True:
        data = '#32CD32'
    if con_data.status == False:
        data = '#FF0000'
    session.close()
    return data


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect('login' + '?next=' + request.url)
    return response

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/alarm_text')
@login_required
def alarm_text():
    session = Session()
    data = session.query(Text_Alarm).all()
    session.close()
    return render_template('alarem_text_list.html', data=data)


@app.route('/alarm_text/add_alarm_text', methods=['GET'])
@login_required
def add_alarm_text_form():
    return render_template('add_alarm_text.html')


@app.route('/alarm_text/add_alarm_text', methods=['POST'])
@login_required
def add_alarm_text():
    name = request.form['name']
    type = request.form['type']
    a = Text_Alarm(name=name, type=type)
    session = Session()
    session.add(a)
    session.commit()
    session.close()
    return redirect(url_for('alarm_text'))


@app.route('/alarm_text/del', methods=['POST'])
@login_required
def alarm_text_del():
    # from data import pr
    id = request.form['del']
    session = Session()
    a = session.query(Text_Alarm).get(id)
    # pr[a.name].kill()
    session.delete(a)
    session.commit()
    session.close()
    return redirect(url_for('alarm_text'))


@app.route('/alarm_text/up/<int:id_alarm_text>', methods=['GET'])
@login_required
def up_alarm_text_form(id_alarm_text):
    session = Session()
    data = session.query(Text_Alarm).get(id_alarm_text)
    session.close()
    return render_template('up_alarm_text.html', alarm_text_get=data)


@app.route('/alarm_text/up/<int:id_alarm_text>', methods=['POST'])
@login_required
def up_alarm_text(id_alarm_text):
    name = request.form['name']
    type = request.form['type']
    session = Session()
    a = session.query(Text_Alarm).get(id_alarm_text)
    a.name = name
    a.type = type
    session.commit()
    session.close()
    return redirect(url_for('alarm_text'))


@app.route('/connections', methods=['GET'])
@login_required
def index():
    session = Session()
    a = session.query(Connections).order_by(Connections.id)
    data = []
    for i in a:
        k = {
            "name": i.name,
            "ip": i.ip,
            "switch": i.switch,
            "rack": i.rack,
            "slot": i.slot,
            "DB": i.DB,
            "start": i.start,
            "offset": i.offset,
            "id": i.id
        }
        data.append(k)
    session.close()
    return render_template('connections_list.html', data=data)

@app.route('/connections', methods=['POST'])
@login_required
def index_switcher():
    status = request.form['status']
    id = request.form['id']
    session = Session()
    art = session.query(Connections).get(int(id))
    if status == "1":
        art.switch = True
    elif status == "0":
        art.switch = False
    session.commit()
    session.close()
    return f"{type(request.form['status'])}, {type(request.form['id'])}"




@app.route('/add_con', methods=['GET'])
@login_required
def con():
    return render_template('conn.html')


@app.route('/add_con', methods=['POST'])
@login_required
def add_connections():
    name = request.form['name']
    ip = request.form['ip']
    rack = request.form['rack']
    slot = request.form['slot']
    DB = request.form['DB']
    start = request.form['start']
    offset = request.form['offset']
    switch = True
    arrays = request.form['arrays']
    driver = request.form['driver']
    try:
        port = request.form['port']
    except:
        port = 102
    a = Connections(name=name, ip=ip, rack=rack, slot=slot, DB=DB, start=start, offset=offset, switch=switch,
                    driver=driver, port=port, arrays=arrays)
    session = Session()
    session.add(a)
    session.commit()
    session.close()
    return redirect(url_for('index'))


@app.route('/updata_con/<int:id>', methods=['GET'])
@login_required
def up_con(id):
    session = Session()
    data = session.query(Connections).get(id)
    session.close()
    return render_template('up_con.html', data=data)


@app.route('/updata_con', methods=['POST'])
@login_required
def updata_connections():
    id = request.form['id']
    name = request.form['name']
    ip = request.form['ip']
    rack = request.form['rack']
    slot = request.form['slot']
    DB = request.form['DB']
    start = request.form['start']
    offset = request.form['offset']
    arrays = request.form['arrays']
    try:
        port = request.form['port']
    except:
        port = 102
    session = Session()
    a = session.query(Connections).get(id)
    a.name = name
    a.ip = ip
    a.rack = rack
    a.slot = slot
    a.DB = DB
    a.start = start
    a.offset = offset
    a.arrays = arrays
    a.port = port
    session.commit()
    session.close()
    return redirect(url_for('index'))


@app.route('/del_con', methods=['POST'])
@login_required
def del_connections():
    id = request.form['id']
    session = Session()
    a = session.query(Connections).get(id)
    session.delete(a)
    session.commit()
    session.close()
    return redirect(url_for('index'))


@app.route('/value_list/<int:id>', methods=['GET'])
@login_required
def value_list(id):
    session = Session()
    a = session.query(ListValue).filter_by(connections_id=id).order_by(ListValue.id)
    b = session.query(Connections).get(id).name
    array = []
    for i in a:
        c = {
            "id": i.id,
            "name": i.name,
            "start": i.start,
            "type_value": i.type_value,
            "type_table": i.type_table,
            "connections_id": i.connections_id,
            "divide": i.divide,
            "if_change": i.if_change,
            "byte_bind": i.byte_bind,
            "bit_bind": i.bit_bind
        }
        array.append(c)
    data = {
        "data": array,
        "id": id,
        "name": b,
    }
    session.close()
    return render_template('value_list.html', data=data)


@app.route('/value_list/<int:id>/add_value_list', methods=['GET'])
@login_required
def add_value_list(id):
    session = Session()
    alarm = session.query(Text_Alarm).filter_by(type="alarm")
    warning = session.query(Text_Alarm).filter_by(type="warning")

    data = {
        "id": id,
        "alarm": alarm,
        "warning": warning
    }
    session.close()
    return render_template('add_value_list.html', data=data)


@app.route('/value_list/<int:id>/add_value_list', methods=['POST'])
@login_required
def add_value(id):
    session = Session()
    name = request.form['name']
    start = request.form['start']
    type_value = request.form['type_value']
    type_table = request.form['type_table']
    try:
        rewrite_time = request.form['rewrite_time']
    except:
        rewrite_time = 600
    try:
        polling_time = request.form['polling_time']
    except:
        polling_time = 1
    if rewrite_time == '':
        rewrite_time = 10
    if polling_time == None:
        polling_time = 1
    try:
        if request.form['divide'] == 'True':
            divide = 1
            divide_number = request.form['divide_number']
        else:
            divide = 0
            divide_number = None
    except:
        divide = 0
        divide_number = None
    if request.form['if_change'] == 'True':
        if_change = 1
    else:
        if_change = 0
    byte_bind = request.form['byte_bind']
    bit_bind = request.form['bit_bind']
    a = ListValue(name=name,
                  start=start,
                  type_value=str(type_value),
                  type_table=str(type_table),
                  connections_id=id,
                  divide=divide,
                  divide_number=divide_number,
                  if_change=if_change,
                  byte_bind=byte_bind,
                  bit_bind=bit_bind,
                  polling_time=polling_time,
                  rewrite_time=rewrite_time
                  )
    session.add(a)
    session.commit()
    if type_value == "bool":
        bit_bool = request.form['bit_bool']
        text_alarm_id = request.form['text_alarm']
        a = session.query(ListValue).filter_by(name=name,
                  start=start,
                  type_value=str(type_value),
                  type_table=str(type_table),
                  connections_id=id
                  ).order_by(ListValue.id.desc()).first()
        alarm = Alarms(bit=bit_bool,
                text_alarm_id=text_alarm_id,
                value_list_id=a.id
                )
        session.add(alarm)
        session.commit()
        session.close()
    return redirect(url_for('value_list', id=id))


@app.route('/value_list/<int:id>/del', methods=['POST'])
@login_required
def del_value(id):
    id1 = request.form['id_val']
    session = Session()
    a = session.query(ListValue).get(id1)
    session.delete(a)
    session.commit()
    session.close()
    return redirect(url_for('value_list', id=id))


@app.route('/value_list/up/<int:id1>/<int:id2>', methods=['GET'])
@login_required
def up_value(id1, id2):
    session = Session()
    a = session.query(ListValue).get(id2)
    alarms = session.query(Alarms).filter_by(value_list_id=a.id)
    alarm = session.query(Text_Alarm).filter_by(type="alarm")
    warning = session.query(Text_Alarm).filter_by(type="warning")
    if len(list(alarms)) != 0:
        alarms = alarms[0]
        alarm_text = session.query(Text_Alarm).get(alarms.text_alarm_id)
    else:
        alarms = None
        alarm_text = None
    data = {
        "a": a,
        "id1": id1,
        "int": "int",
        "real": "real",
        "bool": "bool",
        "double": "double",
        "alarm": alarm,
        "warning": warning,
        "al_id": alarms,
        "alarm_text": alarm_text
    }
    session.close()
    return render_template('up_val.html', data=data)


@app.route('/value_list/up/<int:id1>/<int:id2>', methods=['POST'])
@login_required
def up_value_ch(id1, id2):
    session = Session()
    a = session.query(ListValue).get(id2)
    name = request.form['name']
    start = request.form['start']
    type_value = request.form['type_value']
    type_table = request.form['type_table']
    rewrite_time = request.form['rewrite_time']
    if rewrite_time == '':
        rewrite_time = 10
    try:
        polling_time = request.form['polling_time']
    except:
        polling_time = 1
    if polling_time == None:
        polling_time = 1
    try:
        if request.form['divide'] == "True":
            divide = True
            divide_number = request.form['divide_number']
        else:
            divide = False
            divide_number = None
    except:
        divide = False
        divide_number = None
    if request.form['if_change'] == "True":
        if_change = True
    else:
        if_change = False
    byte_bind = request.form['byte_bind']
    bit_bind = request.form['bit_bind']
    try:
        bit_bool = request.form['bit_bool']
        type_iv = request.form['type_ivent']
        id_text_alarm = request.form['text_alarm']
    except:
        bit_bool = 1
        type_iv = 'alarms'
        id_text_alarm = 2
    a.name = name
    a.start = start
    a.type_value = type_value
    a.type_table = type_table
    a.connections_id = id1
    a.divide = divide
    a.divide_number = divide_number
    a.if_change = if_change
    a.byte_bind = byte_bind
    a.bit_bind = bit_bind
    a.polling_time = polling_time
    a.rewrite_time = rewrite_time
    session.commit()
    # alarm_get = session.query(Alarms).filter_by(value_list_id=a.id).first()
    # alarm_get.bit = bit_bool

    session.close()
    return redirect(url_for('value_list', id=id1))

@app.route('/alarm_text/<int:id_alarm_text>/alarm', methods=['GET'])
@login_required
def alarm_list(id_alarm_text):
    session = Session()
    a = session.query(Alarms).filter_by(text_alarm_id=id_alarm_text)
    b = session.query(Text_Alarm).get(id_alarm_text)
    data = {
        "id_alarm_text": id_alarm_text,
        "array_alarms": a,
        "text": b.name,
        "type": b.type
    }
    session.close()
    return render_template('alarm_list.html', data=data)


@app.route('/alarm_text/<int:id_alarm_text>/alarm/add_alarm', methods=['GET'])
@login_required
def add_alarm_form(id_alarm_text):
    return render_template('add_alarm.html', data=id_alarm_text)


@app.route('/alarm_text/<int:id_alarm_text>/alarm/add_alarm', methods=['POST'])
@login_required
def add_alarm(id_alarm_text):
    bit = request.form['bit']
    session = Session()
    a = Alarms(bit=bit, text_alarm_id=id_alarm_text)
    session.add(a)
    session.commit()
    return redirect(url_for('alarm_list', id_alarm_text=id_alarm_text))


@app.route('/alarm_text/<int:id_alarm_text>/alarm/up/<int:id_alarm>', methods=['GET'])
@login_required
def up_alarm_form(id_alarm_text, id_alarm):
    session = Session()
    a = session.query(Alarms).get(id_alarm)
    data = {
        "array": a,
        "id_alarm_text": id_alarm_text
    }
    return render_template('up_alarm.html', data=data)


@app.route('/alarm_text/<int:id_alarm_text>/alarm/up/<int:id_alarm>', methods=['POST'])
@login_required
def up_alarm(id_alarm_text, id_alarm):
    bit = request.form['bit']
    session = Session()
    a = session.query(Alarms).get(id_alarm)
    a.bit = bit
    session.commit()
    return redirect(url_for('alarm_list', id_alarm_text=id_alarm_text))


@app.route('/alarm_text/<int:id_alarm_text>/alarm/del/<int:id_alarm>', methods=['POST'])
@login_required
def del_alarm(id_alarm_text, id_alarm):
    session = Session()
    a = session.query(Alarms).get(id_alarm)
    session.delete(a)
    session.commit()
    return redirect(url_for('alarm_list', id_alarm_text=id_alarm_text))


def run_flask(status):
    """ run flask in other thread
    :return:
    """
    globals()['connections'] = status
    app.run(host='0.0.0.0', port=5001)