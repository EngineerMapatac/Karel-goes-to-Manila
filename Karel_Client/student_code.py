from karel3d import move, turn_left, pick_beeper

def turn_right():
    turn_left()
    turn_left()
    turn_left()

def turn_around():
    turn_left()
    turn_left()

def main():
    print("Starting Karel's route through Manila...")
    
    # Example route: Move forward 3 tiles, turn left, move 2 tiles
    move()
    move()
    move()
    turn_left()
    move()
    move()
    turn_right()
    move()

    print("Route complete!")

if __name__ == "__main__":
    main()