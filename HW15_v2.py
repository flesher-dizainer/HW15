from dataclasses import dataclass, field
import json
from typing import Any
import random


class JsonFile:
    '''
    Класс для работы с json файлом. Загрузки и сохранения файла
    '''

    def __init__(self, path_file_name: str):
        '''
        Инициализация экземпляра класса
        :param path_file_name: путь к json файлу
        '''
        self.patch_file = path_file_name

    # Читает данные из JSON-файла и возвращает их.
    def read_data(self):
        '''
        метод открытия json файла
        :return: список json данных или None
        '''
        with open(self.patch_file, 'r', encoding='utf-8') as file_json:
            try:
                return json.load(file_json)
            except FileNotFoundError:
                return None

    # Записывает данные в JSON-файл.
    def write_data(self, data):
        '''
        метод сохранения json данных в файл
        :param data:
        :return: None
        '''
        with open(self.patch_file, 'w', encoding='utf-8') as file_json:
            try:
                json.dump(data, file_json)
            except Exception as err:
                print(err)


@dataclass
class City:
    '''
    Дата класс представления информации о городе
    '''
    name: str = field(compare=True)
    population: int = field(compare=False, default=0)
    subject: str = field(compare=False, default='')
    district: str = field(compare=False, default='')
    coords: dict = field(compare=False, default_factory=lambda: {'lat': '', 'lon': ''})
    is_used: bool = field(compare=True, default=False)


class CitiesSerializer:
    '''
    Класс для создания списка обьектов городов
    '''

    def __init__(self, cities_data: list[dict[str, Any]]):
        self.cities_object: list[City] = [City(**city_data) for city_data in cities_data]


# здесь будут методы игры
class CityGame:
    def __init__(self, json_data: list):
        self.name_gamer = 'Computer'
        self.flag_human = False
        self.cities_objects = CitiesSerializer(json_data)
        self.city_name_compare = ''

    def start(self):
        int_rand = random.randint(0, len(self.cities_objects.cities_object) - 1)
        name_city_start = self.cities_objects.cities_object[int_rand].name
        self.city_name_compare = name_city_start
        print(f'Начало игры. Ход {self.name_gamer}')
        return self.check_game_over(name_city_start)

    def turn(self):
        '''
        ход игры
        :return:
        '''
        print(f'Ход {self.name_gamer}. Необходимо выбрать город начинающийся на букву {self.city_name_compare[-1].upper()}')
        city_name = ''

        if self.flag_human:
            city_name = input('Введите название города: ')
        else:
            for city_obj in self.cities_objects.cities_object:
                if self.city_name_compare[-1].lower() == city_obj.name[0].lower():
                    if not city_obj.is_used:
                        city_name = city_obj.name
        return self.check_game_over(city_name)

    def check_game_over(self, city_name):
        '''
        Проверяем наличие города в списке
        :param city_name: название города
        :return: результат проверки bool
        '''
        print(f'{self.name_gamer} выбрал город с названием {city_name}')
        for i in range(len(self.cities_objects.cities_object)):
            if city_name.lower() == self.cities_objects.cities_object[i].name.lower():
                if not self.cities_objects.cities_object[i].is_used:
                    self.cities_objects.cities_object[i].is_used = True
                    self.flag_human = True if not self.flag_human else False
                    self.name_gamer = 'Computer' if not self.flag_human else 'Human'
                    self.city_name_compare = city_name
                    return True
        print(f'Игрок {self.name_gamer} проиграл, выбрав город с названием {city_name}')
        return False


# в менеджере будем крутить игру
class GameManager:
    def __init__(self, json_data: list):
        self.city_game = CityGame(json_data)

    def __call__(self):
        if self.city_game.start():
            while self.city_game.turn():
                pass


if __name__ == '__main__':
    json_file = JsonFile("cities.json")
    game_manager = GameManager(json_file.read_data())
    game_manager()
