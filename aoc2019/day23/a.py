import intcode as ic


def create_network():
    computers = {}

    for i in range(50):
        sm = ic.load_state_machine('input')
        computers[i] = sm
        ic.add_input(sm, i)
        ic.run_state_machine(sm)

    return computers


def send_message(computers, cid, x, y):
    ic.add_input(computers[cid], x)
    ic.add_input(computers[cid], y)
    ic.run_state_machine(computers[cid])


def receive_message(computers, cid):
    computer = computers[cid]
    if ic.has_output(computer):
        cid = ic.get_output(computer)
        x = ic.get_output(computer)
        y = ic.get_output(computer)
    else:
        ic.add_input(computer, -1)
        ic.run_state_machine(computer)
        cid = None
        x = None
        y = None

    return cid, x, y


def network_is_idle(computers):
    return all([not ic.has_output(sm) for sm in computers.values()])


computers = create_network()
nat = (0, 0)
sent_nat = None
iter_count = 0
while True:
    iter_count += 1
    for computer_id in computers:
        cid, x, y = receive_message(computers, computer_id)
        if cid == 255:
            if nat == (0, 0):
                print(f'solution to part 1 is {y} = 23815')
            nat = x, y
        elif cid is not None:
            send_message(computers, cid, x, y)

    if network_is_idle(computers):
        send_message(computers, 0, *nat)
        if sent_nat is not None and sent_nat[1] == nat[1]:
            print(f'solution to part 2 is {nat[1]} = 16666')
            break
        else:
            sent_nat = nat
print(iter_count)