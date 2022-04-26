class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories
    def get_message(self):
        print (f'Тип тренировки: {self.training_type};' 'Длительность: {self.duration:.3f} ч.;' 'Дистанция: {self.distance:.3f} км.;' 'Ср. скорость: {self.speed:.3f} км/ч;' 'Потрачено ккал: {self.calories:.3f}.')
    pass

class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        pass

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance
        pass

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed
        pass

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(self.__class__.__name__,
                                   self.duration,
                                   self.get_distance(),
                                   self.get_mean_speed(),
                                   self.get_spent_calories())
        return message
        pass


class Running(Training):
    coeff_calories_running_1: int = 18
    coeff_calories_running_2: int = 20
    MINS_INTO_SECONDS = 60
    M_IN_KM = 1000
    """Тренировка: бег."""
    def __init__(self, action, duration, weight):
        super().__init__(action, duration, weight)
    def get_spent_calories(self):
        spent_calories = ((self.coeff_calories_running_1 * self.get_mean_speed()
                 - self.coeff_calories_running_2) 
                 * self.weight/self.M_IN_KM * self.duration* self.MINS_INTO_SECONDS)
        return spent_calories
    pass


class SportsWalking(Training):        
    coeff_calories_walking_1 = 0.035
    coeff_calories_walking_2 = 2
    coeff_calories_walking_3 = 0.029
    MINS_INTO_SECONDS = 60
    """Тренировка: спортивная ходьба."""
    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height
    def get_spent_calories(self):
        spent_calories = ((self.coeff_calories_walking_1 * self.weight 
                + (self.get_mean_speed**self.coeff_calories_walking_2 // self.height) 
                * self.coeff_calories_walking_3*self.weight) 
                * self.duration*self.MINS_INTO_SECONDS)
        return spent_calories

    pass


class Swimming(Training):
    coeff_calorie_swimming_1: float = 1.1
    coeff_calorie_swimming_2: int = 2
    M_IN_KM = 1000
    LEN_STEP = 1.38
    """Тренировка: плавание."""
    def __init__(self, action, duration, weight, lenght_pool, count_pool):
        super().__init__(action, duration, weight)
        self.lenght_pool = lenght_pool
        self.count_pool = count_pool
    def get_mean_speed(self):
        mean_speed = (self.lenght_pool * self.count_pool / self.M_IN_KM / self.duration)
        return mean_speed
    def get_spent_calories(self):
        spent_calories = ((self.get_mean_speed() + self.coeff_calorie_swimming_1) 
                 * self.coeff_calorie_swimming_2  * self.weight)
        return spent_calories
    def get_distance(self):
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance
    pass


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    trainings = {
        'SWM' : Swimming,
        'RUN' : Running,
        'WLK' : SportsWalking
    }
    return trainings[workout_type](*data)
    pass

def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())
    pass


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

