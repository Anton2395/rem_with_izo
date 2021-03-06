from django.db import models
from users.models import *
from django.db import connection
import datetime
from structure.models import Agreagat
from project_v_0_0_1.settings import dist_table
from rest_framework.exceptions import ValidationError





class Dashboard(models.Model):
    '''
    Сущность для определения виджетов

      Attributes
    ===========
    - name - str - название для записи

     Methods
    =============
    - None
    '''
    name = models.CharField(max_length=255, default='no name')

    def __str__(self):
        return self.name




class Role(models.Model):
    '''
        Сущность для определения роли пользователя

          Attributes
        ===========
        - name - str - название для записи
        - user - MtM - связь с сущностью UserP
        - dashboard - MtM - связь с сущностью Dashboard

         Methods
        =============
        - None
    '''
    name = models.CharField(max_length=255, default='no name')
    user = models.ManyToManyField(UserP)
    dashboard = models.ManyToManyField(Dashboard)


# def calculate_duration_shift(date, start, end):
#     with connection.cursor() as cursor:
#         sql1 = '''SELECT value, now_time FROM '''
#         sql2 = ''' WHERE now_time>=%s and now_time<%s ORDER BY now_time'''
#         sql = sql1 + dist_table['DurationIntervalDay'][0] + sql2
#         date_start = datetime.datetime(date.year, date.month, date.day, start.hour, start.minute, start.second)
#         date_end = datetime.datetime(date.year, date.month, date.day, end.hour, end.minute, end.second)
#         cursor.execute(sql, [date_start, date_end])
#         a = cursor.fetchall()
#         k = 0
#         for i in a:
#             if i[0] == 1 and k == 0:
#                 k += 1
#                 date_start1 = datetime.time(i[1].hour, i[1].minute, i[1].second)
#             if i[0] == 0 and k == 1:
#                 k = 0
#                 date_end1 = datetime.time(i[1].hour, i[1].minute, i[1].second)
#                 obj = DurationIntervalDay(start=date_start1, end=date_end1, date=date)
#                 obj.save()
#         return 0


# для виджета продолжительность работы
class DurationIntervalDay(models.Model):
    '''
        Сущность для определения начало и времени работы

          Attributes
        ===========
        - start - Time - начало работы
        - end - Time - конец работы
        - date - Date - дата работы

         Methods
        =============
        - None
    '''
    start = models.TimeField('start work')
    end = models.TimeField('end work')
    date = models.DateField(auto_now=False, auto_now_add=False)

    def __exists_table(self, text):
        with connection.cursor() as cursor:
            engine = connection.vendor
            if engine == 'sqlite':
                sql = '''SELECT count(*) FROM sqlite_master WHERE type="table" AND name="'''
            elif engine == 'postgresql':
                sql = '''SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_name ="'''
            sql = sql + text + '"'
            cursor.execute(sql)
            a = cursor.fetchall()[0][0]
        return a

    # def save(self):
    #     a = self.__exists_table(dist_table['DurationIntervalDay'][0])
    #     if a:
    #         super(DurationIntervalDay, self).save()
    #     else:
    #         raise ValidationError('did not find the agreagat table')

# def calculate_duration_day()





class Storehouse(models.Model):
    '''
    Сущность для названия склада

          Attributes
        ===========
        - name - str - название склада

         Methods
        =============
        - None
    '''
    name = models.CharField(max_length=255, default='no name')


    def __str__(self):
        return self.name


class Substance(models.Model):
    '''
    Сущность для названия хранящегося вещества

          Attributes
        ===========
        - name - str - название вещества
        - short_name - str - короткая название вещества
        - parent - FK - внешний ключь с Storehouse

         Methods
        =============
        - calculate - Забись данных в таблицу Django остатка по дате
        - value_date - Возвращает велечину остатка на складе
    '''
    name = models.CharField(max_length=255, default='no name')
    short_name = models.CharField(max_length=255, default='no name')
    table_name = models.CharField(max_length=255, default='no name')
    parent = models.ForeignKey(Storehouse, on_delete=models.CASCADE)

    def __str__(self):
        data = self.name + '(' + self.parent.name + ')'
        return data

    def calculate(self, date):
        '''
        Запись данных в таблицу Django остатка по дате

        :param date date: дата за которую извлекаются данные
        '''
        with connection.cursor() as cursor:
            sql1 = '''SELECT value, now_time FROM '''
            sql2 = ''' WHERE now_time>=%s and now_time<%s ORDER BY now_time DESC LIMIT 1'''
            sql = sql1 + self.table_name + sql2
            date_now = date + datetime.timedelta(days=1)
            cursor.execute(sql, [date, date_now])
            a = cursor.fetchone()
            if a == None:
                a = [0]
            k = DateValue(date=date, value=a[0], parent=self)
            if date != datetime.datetime.now().date():
                k.save()
        return a


    def value_date(self, date):
        '''
        Возвращает велечину остатка на складе

        :param date date: дата за которую извлекаются данные
        '''
        if date == datetime.datetime.now().date():
            try:
                k = self.calculate(date)[0]
            except TypeError:
                k = 0
        else:
            if self.datevalue_set.filter(date=date).exists():
                k = self.datevalue_set.get(date=date).value
            else:
                self.calculate(date)
                k = self.datevalue_set.get(date=date).value
        return k



class DateValue(models.Model):
    '''
    Сущность для количество вещества по времени

          Attributes
        ===========
        - date - date - дата
        - value - float - количество вещества
        - parent - FK - внешний ключь с Substance

         Methods
        =============
        - None
    '''
    date = models.DateField(auto_now=False, auto_now_add=False)
    value = models.FloatField()
    parent = models.ForeignKey(Substance, on_delete=models.CASCADE)

    def __str__(self):
        data = str(self.date) + ':  ' + self.parent.name + '-' + str(self.value)
        return data




# для виджета Выпуск панелей
class EditionDay(models.Model):
    '''
        Сущность для определения выпуска

          Attributes
        ===========
        - suitable - float - количество годного
        - substandard - float - количество некондиции
        - defect - float - количество брака
        - flooded - float - количество залитого
        - sum - float - сумма годного, некондиции, брака
        - date - Date - дата

         Methods
        =============
        - None

    '''
    suitable = models.FloatField()
    substandard = models.FloatField()
    defect = models.FloatField()
    flooded = models.FloatField()
    sum = models.FloatField()
    date = models.DateField(auto_now=False, auto_now_add=False, unique=True)

    def __str__(self):
        return str(self.date)






# для виджета Суммарный расход
class SumexpenseDay(models.Model):
    '''
        Сущность для определения сумарного расхода

          Attributes
        ===========
        - iso - float - количество расхода изоцианата
        - pol - float - количество расхода полиола
        - pen - float - количество расхода пентана
        - kat1 - float - количество расхода катализатора 1
        - kat2 - float - количество расхода катализатора 2
        - kat3 - float - количество расхода катализатора 3
        - date - Date - дата

         Methods
        =============
        - None
    '''
    iso = models.FloatField()
    pol = models.FloatField()
    pen = models.FloatField()
    kat1 = models.FloatField()
    kat2 = models.FloatField()
    kat3 = models.FloatField()
    date = models.DateField(auto_now=False, auto_now_add=False, unique=True)


def calculate_energy_consumption(date):
    """

    извлекание и запись данных для виджета сумарного расхода энергоресурсов

    :param date date: дата за которую извлекаются данные

    """
    with connection.cursor() as cursor:
        sql1 = '''SELECT value, now_time FROM '''
        sql21 = ''' WHERE now_time>=%s and now_time<%s ORDER BY now_time DESC LIMIT 1'''
        sql22 = ''' WHERE now_time>=%s and now_time<%s ORDER BY now_time ASC LIMIT 1'''
        sql = sql1 + dist_table['EnergyConsumptionDay']['input1'] + sql21
        date_now = date + datetime.timedelta(days=1)
        cursor.execute(sql, [date, date_now])
        data1 = cursor.fetchone()
        if data1 == None:
            data1 = [0]
        sql = sql1 + dist_table['EnergyConsumptionDay']['input1'] + sql22
        cursor.execute(sql, [date, date_now])
        data2 = cursor.fetchone()
        if data2 == None:
            data2 = [0]
        data_in_1 = data1[0]-data2[0]
        sql = sql1 + dist_table['EnergyConsumptionDay']['input2'] + sql21
        date_now = date + datetime.timedelta(days=1)
        cursor.execute(sql, [date, date_now])
        data1 = cursor.fetchone()
        if data1 == None:
            data1 = [0]
        sql = sql1 + dist_table['EnergyConsumptionDay']['input2'] + sql22
        cursor.execute(sql, [date, date_now])
        data2 = cursor.fetchone()
        if data2 == None:
            data2 = [0]
        data_in_2 = data1[0]-data2[0]
        sql = sql1 + dist_table['EnergyConsumptionDay']['gas'] + sql21
        date_now = date + datetime.timedelta(days=1)
        cursor.execute(sql, [date, date_now])
        data1 = cursor.fetchone()
        if data1 == None:
            data1 = [0]
        sql = sql1 + dist_table['EnergyConsumptionDay']['gas'] + sql22
        cursor.execute(sql, [date, date_now])
        data2 = cursor.fetchone()
        if data2 == None:
            data2 = [0]
        data_gas = data1[0] - data2[0]

        k = EnergyConsumptionDay(input1=data_in_1, input2=data_in_2, gas=data_gas, date=date)
        if datetime.datetime.now().date() != date:
            k.save()
        return k


def calculate_energy_consumption_shift(date, start, end):
    date_start = datetime.datetime(date.year, date.month, date.day, start.hour, start.minute, start.second)
    date_end = datetime.datetime(date.year, date.month, date.day, end.hour, end.minute, end.second)
    sql1 = '''SELECT value, now_time FROM '''
    sql21 = ''' WHERE now_time>=%s and now_time<%s ORDER BY now_time DESC LIMIT 1'''
    sql22 = ''' WHERE now_time>=%s and now_time<%s ORDER BY now_time ASC LIMIT 1'''
    with connection.cursor() as cursor:
        sql = sql1 + dist_table['EnergyConsumptionDay']['input1'] + sql21
        cursor.execute(sql, [date_start, date_end])
        data_end = cursor.fetchone()
        if data_end == None:
            data_end = [0]
        sql = sql1 + dist_table['EnergyConsumptionDay']['input1'] + sql22
        cursor.execute(sql, [date_start,date_end])
        data_start = cursor.fetchone()
        if data_start == None:
            data_start = [0]
        data_in1 = data_end[0] - data_start[0]
        sql = sql1 + dist_table['EnergyConsumptionDay']['input2'] + sql21
        cursor.execute(sql, [date_start, date_end])
        data_end = cursor.fetchone()
        if data_end == None:
            data_end = [0]
        sql = sql1 + dist_table['EnergyConsumptionDay']['input2'] + sql22
        cursor.execute(sql, [date_start, date_end])
        data_start = cursor.fetchone()
        if data_start == None:
            data_start = [0]
        data_in2 = data_end[0] - data_start[0]
        sql = sql1 + dist_table['EnergyConsumptionDay']['gas'] + sql21
        cursor.execute(sql, [date_start, date_end])
        data_end = cursor.fetchone()
        if data_end == None:
            data_end = [0]
        sql = sql1 + dist_table['EnergyConsumptionDay']['gas'] + sql22
        cursor.execute(sql, [date_start, date_end])
        data_start = cursor.fetchone()
        if data_start == None:
            data_start = [0]
        data_gas = data_end[0] - data_start[0]
        data = {
            "input1": data_in1,
            "input2": data_in2,
            "gas": data_gas
        }
    return data









# для виджета Расход энергоресурсов
class EnergyConsumptionDay(models.Model):
    '''
        Сущность для определения сумарного расхода энергоресурсов

          Attributes
        ===========
        - input1 - float - расход эл.энергии ввода 1
        - input2 - float - расход эл.энергии ввода 2
        - gas - float - расход газа
        - date - Date - дата

         Methods
        =============
        - None

    '''
    input1 = models.FloatField()
    input2 = models.FloatField()
    gas = models.FloatField()
    date = models.DateField(auto_now=False, auto_now_add=False, unique=True)

    def __str__(self):
        return 'i1:'+str(self.input1)+' i2:'+str(self.input2)+' g:'+str(self.gas)




# для виджета Удельный расход на км
class SpecificConsumptionDay(models.Model):
    '''
        Сущность для определения удельного расхода

          Attributes
        ===========
        - iso - float - количество удельного расхода изоцианата
        - pol - float - количество удельного расхода полиола
        - pen - float - количество удельного расхода пентана
        - kat1 - float - количество удельного расхода катализатора 1
        - kat2 - float - количество удельного расхода катализатора 2
        - kat3 - float - количество удельного расхода катализатора 3
        - date - Date - дата

         Methods
        =============
        - None
    '''
    iso = models.FloatField()
    pol = models.FloatField()
    pen = models.FloatField()
    kat1 = models.FloatField()
    kat2 = models.FloatField()
    kat3 = models.FloatField()
    date = models.DateField(auto_now=False, auto_now_add=False, unique=True)



class StatePressureRange(models.Model):
    '''
    Сущность для хранение границ и названия давления данного диапазона

      Attributes
    ===========
    - name - str - имя диапазона давления
    - from_data - int - начала диапазона давления
    - to_data - int - конец диапазона давления
    - color - str - цвет отображения данного диапазона


     Methods
    =============
    - get_struc - вазвращает все параметры запеси в dict


    '''
    name = models.CharField(max_length=255, default='no name')
    from_data = models.IntegerField()
    to_data = models.IntegerField()
    color = models.CharField(max_length=255, default='#ffffff')


    def get_struc(self) -> dict:
        k = {
                "name": self.name,
                "from": self.from_data,
                "to": self.to_data,
                "color": self.color
            }
        return k

