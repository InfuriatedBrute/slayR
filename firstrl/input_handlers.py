from game_states import GameStates


def handle_keys(user_input, game_state):
    if(user_input):
        universal_output = handle_universal_keys(user_input)
        if(universal_output):
            return universal_output
        elif game_state == GameStates.PLAYERS_TURN:
            return handle_player_turn_keys(user_input)
        elif game_state == GameStates.PLAYER_DEAD:
            return handle_player_dead_keys(user_input)
        elif game_state == GameStates.TARGETING:
            return handle_targeting_keys(user_input)
        elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
            return handle_inventory_keys(user_input)
        elif game_state == GameStates.LEVEL_UP:
            return handle_level_up_menu(user_input)
        elif game_state == GameStates.CHARACTER_SCREEN:
            return handle_character_screen(user_input)
    return {}

    
def handle_universal_keys(user_input):
    if user_input:
        
        key = user_input.key
        char = user_input.char
        alt = user_input.alt
        if key == 'ENTER' and alt:
            return {'fullscreen': True}
        elif key == 'ESCAPE':
            return {'exit': True}
        elif char == 'q' and alt:
            return {'quit': True}
    return {}


def handle_player_turn_keys(user_input):
    char = user_input.char
    key = user_input.key
    if key == 'UP' or char == 'k' or key == 'KP8':
        return {'move': (0, -1)}
    elif key == 'DOWN' or char == 'j' or key == 'KP2':
        return {'move': (0, 1)}
    elif key == 'LEFT' or char == 'h' or key == 'KP4':
        return {'move': (-1, 0)}
    elif key == 'RIGHT' or char == 'l' or key == 'KP6':
        return {'move': (1, 0)}
    elif char == 'y' or key == 'KP7':
        return {'move': (-1, -1)}
    elif char == 'u' or key == 'KP9':
        return {'move': (1, -1)}
    elif char == 'b' or key == 'KP1':
        return {'move': (-1, 1)}
    elif char == 'n'  or key == 'KP3':
        return {'move': (1, 1)}
    elif char == '.'  or char == 'z' or key == 'KP5':
        return {'wait': True}
    elif char == 'g' or char == ',' or key == 'SPACE':
        return {'interact': True}
    elif char == 'i':
        return {'show_inventory': True}
    elif char == 'd':
        return {'drop_inventory': True}
    elif char == 'c':
        return {'show_character_screen': True}
    return {}

        
def handle_player_dead_keys(user_input):
    if user_input:
        universal_output = handle_universal_keys(user_input)
        if(universal_output):
            return universal_output
        if user_input.char == 'i':
            return {'show_inventory': True}
    return {}

    
def handle_inventory_keys(user_input):
    if user_input:
        universal_output = handle_universal_keys(user_input)
        if(universal_output):
            return universal_output
        if user_input.char:
            index = ord(user_input.char) - ord('a')
            if index >= 0:
                return {'inventory_index': index}
    return {}


def handle_main_menu(user_input):
    if user_input:
        char = user_input.char
        universal_output = handle_universal_keys(user_input)
        if(universal_output):
            return universal_output
        elif char == 'a':
            return {'new_game': True}
        elif char == 'b':
            return {'load_game': True}
        elif char == 'c':
            return {'quit': True}
    return {}

    
def handle_targeting_keys(user_input):
    return handle_universal_keys(user_input)

    
def handle_mouse(mouse_event):
    if mouse_event:
        (x, y) = mouse_event.cell

        if mouse_event.button == 'LEFT':
            return {'left_click': (x, y)}
        elif mouse_event.button == 'RIGHT':
            return {'right_click': (x, y)}

    return {}


def handle_level_up_menu(user_input):
    char = user_input.char
    if user_input:
        universal_output = handle_universal_keys(user_input)
        if(universal_output):
            return universal_output
        if char == 'a':
            return {'level_up': 'hp'}
        elif char == 'b':
            return {'level_up': 'str'}
        elif char == 'c':
            return {'level_up': 'def'}
    return {}


def handle_character_screen(user_input):
    return handle_universal_keys(user_input)
