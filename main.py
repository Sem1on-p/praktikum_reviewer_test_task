import datetime as dt


# Общий комментарий: в классах и методах не хватает докстрингов

class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # Я бы поменял местами strptime if date else now,
        # потому что принято не отрицательное условие ставить
        # А т.к. строка получилось большой(не очень читаемо), 
        # лучше разделить на обычный if
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # Record не с большой буквы, pep8 + есть класс с таким названием
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                # today_stats += record.amount
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            # можно ограничиться  0 <= (today - record.date).days < 7
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # x - плохое название для переменной 
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        # можно это сделать без else, т.к. если условие не выполнится
        # то код всё равно продолжит тут выполняться
        else:
            # можно без скобочек :)
            return('Хватит есть!')


class CashCalculator(Calculator):
    # можно же сразу сделать вещественными константы
    # и т.к. название это просто перевод комментарии не нужны
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # Значения констант не надо передавать в метод, тк
    # мы можем использовать их через self 
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        # Не обязательное присваиваение, можно проверять currency
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        # 1. Я бы заменил это условие на словарь, где currency был бы ключом, 
        # а currency_type и коэффицент деления значением
        # 2. Если делать через условие, то проверял бы везде currency, и изменял currency_type,
        # а так могут возникуть проблемы, если, например, currency_type в каком-то случае 
        # будет равнятся какому-нибудь currency
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # Не совсем понятно зачем получать булево значение,
            # Которое дальше не используется к тому же
            cash_remained == 1.00
            currency_type = 'руб'
        # я бы добавил пустую строку чтобы логически отделить,
        # читаемость стало бы лучше 
        if cash_remained > 0:
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # Тут можно обойтись else
        elif cash_remained < 0:
            # Лучше использовать f-строки
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)
    # Если метод не переопределяется, то можно его вызвать напрямую через родитеский класс
    def get_week_stats(self):
        super().get_week_stats()
