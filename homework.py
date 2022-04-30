from typing import Union, Sequence
from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return(f'Тип тренировки: {self.training_type};'
               f' Длительность: {self.duration:.3f} ч.;'
               f' Дистанция: {self.distance:.3f} км;'
               f' Ср. скорость: {self.speed:.3f} км/ч;'
               f' Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    HOURS_INTO_MINS: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(f'Определите get_spent_calories в'
                                  f'{type(self).__name__}')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    RUNNING_FACTOR: int = 18
    RUNNING_SPEED_DECREASEMENT: int = 20

    def get_spent_calories(self) -> float:
        return ((self.RUNNING_FACTOR
                 * self.get_mean_speed()
                 - self.RUNNING_SPEED_DECREASEMENT)
                * self.weight / self.M_IN_KM
                * self.duration
                * self.HOURS_INTO_MINS)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_PER_MINUTE: float = 0.035
    MEAN_SPEED_COEFF: int = 2
    SPORTSWALKING_CALORIES_FACTOR: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_PER_MINUTE * self.weight
                 + (self.get_mean_speed()
                    ** self.MEAN_SPEED_COEFF
                    // self.height)
                 * self.SPORTSWALKING_CALORIES_FACTOR * self.weight)
                * self.duration * self.HOURS_INTO_MINS)


class Swimming(Training):
    """Тренировка: плавание."""
    SWIMMING_SPEED_INCREASEMENT: float = 1.1
    SWIMMING_FACTOR: int = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                 + self.SWIMMING_SPEED_INCREASEMENT)
                * self.SWIMMING_FACTOR * self.weight)

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM


def read_package(workout_type: str,
                 data: Sequence[Union[int, float]]) -> Training:
    """Прочитать данные полученные от датчиков."""
    trainings: dict[str:type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in trainings:
        raise KeyError(f'Неизвестное значение: {workout_type}')
    return trainings[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
