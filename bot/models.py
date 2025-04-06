import pytz
from datetime import datetime
from sqlalchemy.dialects.postgresql import TIMESTAMP

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.orm import relationship, declarative_base


moscow_time = pytz.timezone('Europe/Moscow')

Base = declarative_base()


class Coin(Base):
    __tablename__ = 'coins'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    coin_id = Column(Integer, ForeignKey('coin_rate.id'))
    date = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(moscow_time))  # TIMESTAMP WITH TIME ZONE  DateTime, default=datetime.now(moscow_time)
    coin_name = Column(String(50))
    border_value = Column(Float, nullable=False)
    expectations = Column(Boolean, nullable=False)
    # coin_price = Column(Float, ForeignKey('coin_rate.coin_price'))
    users = relationship('User', back_populates='coins')
    coin_rate = relationship('Coins_rates', back_populates='coin')

    # __mapper_args__ = {
    #     'polymorphic_identity': 'coin',
    #     'polymorphic_on': type
    # }

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, nullable=False, unique=True)
    name = Column(String(80), nullable=False)
    chat_id = Column(Integer, nullable=False)
    # height = Column(Float)

    coins = relationship('Coin', back_populates='users')


class Coins_rates(Base):
    __tablename__ = 'coin_rate'

    id = Column(Integer, primary_key=True)
    coin_price = Column(Float, nullable=False)
    coin_name = Column(String(70), nullable=False)
    # speed = Column(Float, nullable=False)
    # spent_calories = Column(Float, nullable=False)
    # distance = Column(Float, nullable=False)

    coin = relationship('Coin', back_populates='coin_rate')

# class Coin_name(Base):
#     __tablename__ = 'names'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(70))
#
#     __mapper_args__ = {
#         'polymorphic_identity': 'running',
#         'inherit_condition': id == Workout.id
#     }
#
#     def history_message(self) -> str:
#         """
#         Функция выводит информацию об истории тренировок
#         :return: сообщение с данными о тренировке
#         """
#         sport_type = 'Бег'
#         return (f"Дата тренировки: {self.date.strftime('%d %B %Y %H:%M')}, \n"
#                 f"Тип тренировки: {sport_type}, \n"
#                 f"дистанция: {self.distance} км, \n"
#                 f"потраченные калории: {self.spent_calories} \n")
#
#
# class Swimming(Workout):
#     __tablename__ = 'swimming'
#
#     id = Column(Integer, ForeignKey('workout.id'), primary_key=True)
#     action = Column(Integer, nullable=False)
#     duration = Column(Integer, nullable=False)
#     length_pool = Column(Float, nullable=False)
#     count_pool = Column(Integer, nullable=False)
#     speed = Column(Float, nullable=False)
#     spent_calories = Column(Float, nullable=False)
#     distance = Column(Float, nullable=False)
#
#     workout = relationship('Workout', back_populates='swimming')
#
#     __mapper_args__ = {
#         'polymorphic_identity': 'swimming',
#         'inherit_condition': id == Workout.id
#     }
#
#     def history_message(self) -> str:
#         """
#         Функция выводит информацию об истории тренировок
#         :return: сообщение с данными о тренировке
#         """
#         sport_type = 'Плавание'
#         return (f"Дата тренировки: {self.date}, \n"
#                 f"Тип тренировки: {sport_type}, \n"
#                 f"дистанция: {self.distance} км, \n"
#                 f"потраченные калории: {self.spent_calories} \n")
#
#
# class Walking(Workout):
#     __tablename__ = 'walking'
#
#     id = Column(Integer, ForeignKey('workout.id'), primary_key=True)
#     action = Column(Integer, nullable=False)
#     duration = Column(Integer, nullable=False)
#     speed = Column(Float, nullable=False)
#     spent_calories = Column(Float, nullable=False)
#     distance = Column(Float, nullable=False)
#
#     workout = relationship('Workout', back_populates='walking')
#
#     __mapper_args__ = {
#         'polymorphic_identity': 'walking',
#         'inherit_condition': id == Workout.id
#     }
#
#     def history_message(self) -> str:
#         """
#         Функция выводит информацию об истории тренировок
#         :return: сообщение с данными о тренировке
#         """
#         sport_type = 'Ходьба'
#         return (f"Дата тренировки: {self.date}, \n"
#                 f"Тип тренировки: {sport_type}, \n"
#                 f"дистанция: {self.distance} км, \n"
#                 f"потраченные калории: {self.spent_calories} \n")


# class User(Base):
#     __tablename__ = 'users'
#
#     id = Column(Integer, primary_key=True)
#     tg_id = Column(Integer, nullable=False, unique=True)
#     age = Column(Float, nullable=False)
#     weight = Column(Float, nullable=False)
#     height = Column(Float)
#
#     workouts = relationship('Workout', back_populates='user')

    # def __repr__(self):
    #     return f"<User(id={self.id}, username={self.username}"
#
# Workout.running = relationship('Running', back_populates='workout', uselist=False)
# Workout.swimming = relationship('Swimming', back_populates='workout', uselist=False)
# Workout.walking = relationship('Walking', back_populates='workout', uselist=False)