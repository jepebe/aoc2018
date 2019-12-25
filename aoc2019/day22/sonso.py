def inv_mod(n, m):
    return pow(n, m-2, m)


def solve_task2(in_lines):
    num_cards = 119315717514047
    reps = 101741582076661
    ans = 2020
    #num_cards = 10007
    #reps = 1
    #ans = 6289
    #ans = 4684
    # Regn ut a og b for en runde med instruksjoner
    a = 1
    b = 0
    for l in in_lines:
        parts = l.split()
        if parts[-2] == "increment":
            n = int(parts[-1])
            # Invers av increment med n er invers modulo (a_1 = a_0 n mod c)
            a *= inv_mod(n, num_cards)
        elif parts[-1] == "stack":
            # Invers transformasjon av stack er b_1 = b_0 - a og a_1 = a_0 - 1
            b -= a
            a *= -1
        elif parts[-2] == "cut":
            n = int(parts[-1])
            # Invers transformasjon av cut er b_1 = b_0 + n*a
            b += n * a

    # Regn ut a_n og b_n for å kjøre runden over n ganger (n=reps)
    a_n = pow(a, reps, num_cards)
    b_n = b * (1 - a_n) * inv_mod(1 - a, num_cards) # Dette kan man finne ved å bruke formel for geometrisk rekke​
    # Nå kan vi kjøre den totale transformasjonen på indexen vi ønsker å reverse
    return (ans * a_n + b_n) % num_cards


if __name__ == "__main__":
    with open("input") as f:
        input_lines = [l.strip() for l in f.readlines()]
    print("Part 2:")
    print(solve_task2(input_lines.copy()))
