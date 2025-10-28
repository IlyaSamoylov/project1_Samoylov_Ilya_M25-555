import labyrinth_game.utils as utils
from labyrinth_game.constants import ROOMS


def show_inventory(game_state):
    '''
    Функция для вывода предметов в инвентаре либо сообщения, что он пуст

    Parameters:
        game_state: dict, словарь состояния игры
    '''
    if game_state['player_inventory']:
        print(f"Инвентарь: {game_state['player_inventory']}")
    else:
        print("В инвентаре хоть шаром покати...")

def get_input(prompt="> "):
    '''
    Функция возвращает ввод игрока, в случае ошибки ввода заканчивает игру

    Parameters:
        prompt="> "
    '''
    try:
        player_com = input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"
    return player_com

def move_player(game_state, direction):
    '''
    Функция для передвижения игрока в доступные из текущей комнаты стороны света:
        Изменяет текущую комнату и число пройденных шагов в game_state либо
        выводит сообщение, что это направление недоступно

    Parameters:
        game_state: dict, словарь игрового состояния
        direction: str, доступная из текущей комнаты сторона света, куда передвигаться
    '''
    current_room_name = game_state['current_room'] # название текущей комнаты
    current_room_dict = ROOMS[current_room_name] # словарь для текущей комнаты из ROOMS

    # если выход в том направлении существует
    if direction in current_room_dict['exits']:
        new_room_name = current_room_dict['exits'][direction] # новая комната
        if new_room_name == 'treasure_room':
            if 'rusty_key' not in game_state['player_inventory']:
                print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
                return
            else:
                print("Вы используете найденный ключ, чтобы открыть путь в комнату "
                      "сокровищ.")

        game_state['current_room'] = new_room_name # обновить комнату в game_state
        game_state['steps_taken'] += 1 # увеличить на один число шагов

        utils.random_event(game_state)

        utils.describe_current_room(game_state) # описать новую комнату

    else:
        print("Нельзя пойти в этом направлении.")

def take_item(game_state, item_name):
    '''
    Функция проверяет,  есть ли предмет в комнате
    Если есть:
     - добавляет предмет из комнаты в инвентарь игрока
     - удаляет из комнаты
     - выводит либо сообщение о том, что предмет поднят
    Иначе: выводит "Такого предмета здесь нет"

    Parameters:
        game_state: dict, словарь игрового состояния
        item_name: str, название предмета для взаимодействия
    '''
    cur_room_dict = ROOMS[game_state['current_room']] #словарь текущей комнаты из ROOMS

    if item_name == 'treasure_chest': # логика для взаимодействия с сундуком сокровищ
        print('Сундук слишком тяжелый, его не сдвинуть')
    elif item_name in cur_room_dict['items']:
        game_state['player_inventory'].append(item_name) # добавить предмет в инвентарь
        # удалить предмет из комнаты в ROOMS
        ROOMS[game_state['current_room']]['items'].remove(item_name)
        print(f'Вы подняли: {item_name}')
    else:
        print('Такого предмета здесь нет')

def use_item(game_state, item_name):
    '''
    Функция использования предмета:

    Args:
        game_state: dict, словарь игрового состояния
        item_name: str, название предмета для использования

    Returns:

    '''
    if item_name not in game_state['player_inventory']:
        print("У вас нет такого предмета.")

    else:
        match item_name:
            case 'torch':
                print("Тьма расступается перед светом факела.")

            case 'candle':
                print('Свеча мягко освещает вам путь')

            case 'sword':
                print("Меч тяжелый, но с ним вы чувствуете себя увереннее")

            case 'bronze_box':
                print("Вы открыли бронзовую шкатулку.")
                if 'rusty_key' not in game_state['player_inventory']:
                    game_state['player_inventory'].append('rusty_key')
                    print("Внутри вы нашли Ржавый ключ!")
                    game_state['player_inventory'].remove('bronze_box')
                else:
                    print("Шкатулка пуста.")

            case _:
                print(f"Вы не знаете, как использовать {item_name}.")