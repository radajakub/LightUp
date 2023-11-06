from instance import Instance

if __name__ == '__main__':
    instance = Instance('01')
    print(instance)

    instance.print_map()
    print(instance.get_empty())

    # instance.place_bulb((4, 2))
    # instance.print_map()
    # instance.place_bulb((0, 2))
    # instance.print_map()
