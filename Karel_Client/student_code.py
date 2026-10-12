from karel3d import move, turn_left, pick_beeper

def turn_right():
    turn_left()
    turn_left()
    turn_left()

def main():
    # Drive through the Manila street grid
    move()
    move()
    turn_left()
    move()
    pick_beeper()
    turn_right()
    move()

if __name__ == "__main__":
    main()