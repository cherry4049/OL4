from fsm import FSM

def main():
    # TODO: initialize robot
    # TODO: create FSM instance

    fsm = FSM()

    while True:
        # TODO: read sensors
        sensor_data = None

        # TODO: update FSM with sensor input
        fsm.update(sensor_data)

        # TODO: execute movement output
        action = fsm.get_action()

        # TODO: send action to movement controller
        pass


if __name__ == "__main__":
    main()