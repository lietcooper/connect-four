from game_controller import GameController
WIDTH = 700
HEIGHT = 700
GRID_SIZE = 100
START_LINE = GRID_SIZE  # the height of click area
MAX_DEPTH = 6

# def input(message=''):

def setup():
    global gc
    size(WIDTH, HEIGHT)
    answer = input('enter your name')
    if answer:
        print('hi ' + answer)
    elif answer == '':
        print('[empty string]')
    else:
        print(answer)  # Canceled dialog will print None
    gc = GameController(START_LINE, WIDTH, HEIGHT, GRID_SIZE, answer, MAX_DEPTH)


def input(message=''):
    from javax.swing import JOptionPane
    return JOptionPane.showInputDialog(frame, message)


def draw():
    background(200)
    gc.update()


def mouseDragged():
    if mouseY < START_LINE and 0 <= mouseX <= WIDTH \
       and not gc.disk_falling\
       and gc.is_player_turn:
        drop_x = mouseX // GRID_SIZE * GRID_SIZE + GRID_SIZE // 2
        drop_y = START_LINE // 2
        # If a column has empty space, drop the disk"""
        if len(gc.grid.disks[drop_x // gc.grid.grid_size])\
           < gc.grid.disks_height:
            gc.hold_disk(drop_x, drop_y)


def mouseReleased():
    if mouseY < START_LINE and 0 <= mouseX <= WIDTH\
       and not gc.disk_falling\
       and gc.is_player_turn:
        drop_x = mouseX // GRID_SIZE * GRID_SIZE + GRID_SIZE // 2
        drop_y = START_LINE // 2
        # If a column has empty space, drop the disk"""
        if len(gc.grid.disks[drop_x // gc.grid.grid_size])\
           < gc.grid.disks_height:
            gc.disk_falling = True
            gc.drop_disk(drop_x, drop_y)
        if gc.grid.temp_disk:
            del gc.grid.temp_disk[0]
