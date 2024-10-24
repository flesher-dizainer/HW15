from dataclasses import dataclass, field
import json


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
                json.dump(file_json, data)
            except Exception as err:
                print(err)


class CitiesSerializer:
    '''
    Класс для создания списка обьектов городов
    '''

    def __init__(self, cities_data: list):
        self.cities_object: list[City] = [City(
            latitude=float(city_data.get('coords').get('lat', 0)),
            longitude=float(city_data.get('coords').get('lon', 0)),
            name=city_data.get('name', '').capitalize(),
            population=city_data.get('population', 0),
            subject=city_data.get('subject', ''),
            district=city_data.get('district', '')
        ) for city_data in cities_data]

    def get_all_cities(self):
        """
        метод возврата списка обьектов городов
        """
        return self.cities_object


@dataclass
class City:
    # Датакласс для представления города.
    name: str = field(compare=True)  # Название города.
    population: int = field(compare=False, default=0)  # Население города.
    subject: str = field(compare=False, default='')  # Субъект федерации.
    district: str = field(compare=False, default='')  # Район.
    latitude: float = field(compare=False, default=0.0)  # Широта.
    longitude: float = field(compare=False, default=0.0)  # Долгота.
    is_used: bool = field(compare=True, default=False)  # Флаг, указывающий, использован ли город в игре.


class CityGame:
    # Управляет логикой игры.
    def __init__(self, cities: CitiesSerializer):
        self.city_obj = cities
        self.human_turn_now = False  # флаг показывающий ход игрока или компьютера
        self.name_city_game = ''  # Название города для определения названия нового города

    def start_game(self):  # Начинает игру, включая первый ход компьютера.
        self.name_city_game = 'А'
        self.human_turn_now = False
        return self.computer_turn()

    def human_turn(self):  # Обрабатывает ход человека.
        name = self.name_city_game[-1].upper()
        print(f'Ход Человека. Ищет слово на букву {name}')
        human_city_name = input(
            f'Введите название города которая начинается на букву {self.name_city_game[-1].upper()}:\n').capitalize()
        human_city_obj = City(human_city_name)
        print(f'Человек выбрал название города {human_city_name}')
        return self.check_game_over(human_city_obj)

    def computer_turn(self):  # Выполняет ход компьютера.
        name = self.name_city_game[-1].upper()
        print(f'Ход компьютера. Ищет слово на букву {name}')
        for city in self.city_obj.cities_object:
            if not city.is_used and (city.name[:1] == name):
                print(f'Компьютер выбрал название города {city.name}')
                computer_city_obj = City(city.name)
                return self.check_game_over(computer_city_obj)
        return False

    def check_game_over(self, obj_city):  # Проверяет завершение игры и определяет победителя.
        if obj_city.name[0:1].lower() != self.name_city_game[-1].lower():
            return False
        for number_obj_city in range(len(self.city_obj.cities_object)):
            if obj_city == self.city_obj.cities_object[number_obj_city]:
                self.city_obj.cities_object[number_obj_city].is_used = True
                self.human_turn_now = False if self.human_turn_now else True
                self.name_city_game = self.city_obj.cities_object[number_obj_city].name.capitalize()
                return True
        return False

    def save_game_state(self):  # Сохраняет состояние игры, если необходимо.
        pass


class GameManager:
    # Фасад, который инкапсулирует взаимодействие между компонентами.
    def __init__(self, class_json_file: JsonFile, class_cities_serializer: CitiesSerializer, class_city_game: CityGame):
        self.json_file = class_json_file  # Экземпляр класса `JsonFile`.
        self.cities_serializer = class_cities_serializer  # Экземпляр класса `CitiesSerializer`.
        self.city_game = class_city_game  # Экземпляр класса `CityGame`.

    def __call__(self):
        # Запускает игру, вызывая методы `start_game()`, `human_turn()`, и `computer_turn()` до завершения игры.
        if self.city_game.start_game():
            result = True
            while result:
                if self.city_game.human_turn():
                    if not self.city_game.computer_turn():
                        result = False
                else:
                    result = False
            if not result:
                self.display_game_result()

    def run_game(self):  # Координирует выполнение игры.
        pass

    def display_game_result(self):  # Отображает результат игры после её завершения (опционально).
        name_gamer = 'Человек' if self.city_game.human_turn_now else 'Компьютер'
        print(f'Игрок {name_gamer} проиграл')


if __name__ == '__main__':
    json_file = JsonFile("cities.json")
    cities_serializer = CitiesSerializer(json_file.read_data())
    city_game = CityGame(cities_serializer)
    game_manager = GameManager(json_file, cities_serializer, city_game)
    game_manager()
