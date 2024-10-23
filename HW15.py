from dataclasses import dataclass
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
        self._cities_object = [City(
            latitude=float(city_data.get('coords').get('lat', 0)),
            longitude=float(city_data.get('coords').get('lon', 0)),
            name=city_data.get('name', ''),
            population=city_data.get('population', 0),
            subject=city_data.get('subject', ''),
            district=city_data.get('district', '')
        ) for city_data in cities_data]

    def get_all_cities(self):
        """
        метод возврата списка обьектов городов
        """
        return self._cities_object

    def compare_city_name(self, name):
        """
        Метод сравнения названия города и установка флага, что город использован
        """
        for city_number in range(len(self._cities_object)):
            city_obj = self._cities_object[city_number]
            if (name.lower() == city_obj.name.lower()) and (not city_obj.is_used):
                self._cities_object[city_number].is_used = True
                return True
        return False


@dataclass
class City:
    # Датакласс для представления города.
    name: str  # Название города.
    population: int  # Население города.
    subject: str  # Субъект федерации.
    district: str  # Район.
    latitude: float  # Широта.
    longitude: float  # Долгота.
    is_used: bool = False  # Флаг, указывающий, использован ли город в игре.


class CityGame:
    # Управляет логикой игры.
    def __init__(self, cities: CitiesSerializer):
        self.city_obj = cities

    def start_game(self):  # Начинает игру, включая первый ход компьютера.
        pass

    def human_turn(self, city_input):  # Обрабатывает ход человека.
        pass

    def computer_turn(self):  # Выполняет ход компьютера.
        pass

    def check_game_over(self):  # Проверяет завершение игры и определяет победителя.
        pass

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
        pass

    def run_game(self):  # Координирует выполнение игры.
        pass

    def display_game_result(self):  # Отображает результат игры после её завершения (опционально).
        pass


if __name__ == '__main__':
    json_file = JsonFile("cities.json")
    cities_serializer = CitiesSerializer(json_file.read_data())
    city_game = CityGame(cities_serializer)
    game_manager = GameManager(json_file, cities_serializer, city_game)
    game_manager()
