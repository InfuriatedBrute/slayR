import os
import shelve


save_directory = 'saves\\'

def save_game(player, entities, game_map, message_log, game_state, saveName='1'):
    with shelve.open(save_directory + saveName, 'n') as data_file:
        data_file['player_index'] = entities.index(player)
        data_file['entities'] = entities
        data_file['game_map'] = game_map
        data_file['message_log'] = message_log
        data_file['game_state'] = game_state


def load_game(saveName='1'):
    if not os.path.isfile(save_directory + saveName + '.dat'):
        raise FileNotFoundError

    with shelve.open('saves\\' + saveName, 'r') as data_file:
        player_index = data_file['player_index']
        entities = data_file['entities']
        game_map = data_file['game_map']
        message_log = data_file['message_log']
        game_state = data_file['game_state']

    player = entities[player_index]

    return player, entities, game_map, message_log, game_state


def delete_game(saveName='1'):
    if not os.path.isfile(save_directory + saveName + '.dat'):
        raise FileNotFoundError
    os.remove(save_directory + saveName + '.dat')