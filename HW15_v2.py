from dataclasses import dataclass, field
import json
from typing import Any


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


if __name__ == '__main__':
    json_file = JsonFile("cities.json")
    cities_serializer = CitiesSerializer(json_file.read_data())
    # n = City('Абакан')
    # for i in cities_serializer.cities_object:
    #     print(i == n)
