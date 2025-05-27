import config


def get_map1() -> list[list[str]]:
    # Initialize empty 25 x 46 inner field
    map1 = []
    for row in range(25):
        current_row = []
        for col in range(46):
            current_row.append("ground")
        map1.append(current_row)
        # map[y][x] — first index is Y (row), second is X (column)

    # Obstacles ("wall")
    for x in range(3, 13):
        map1[3][x] = "wall"  # top left
    for y in range(10, 13):
        for x in range(20, 26):
            map1[y][x] = "wall"  # center block
    for y in range(19, 22):
        for x in range(38, 39):
            map1[y][x] = "wall"  # bottom right wall

    # Lava spots
    lava_spots = [(4, 21), (2, 42), (8, 2), (14, 40), (16, 31), (21, 17)]
    for y, x in lava_spots:
        map1[y][x] = "lava"  # scattered lava tiles

    # Ice areas
    for y in range(14, 17):
        for x in range(9, 13):
            map1[y][x] = "ice"  # bottom left
    for y in range(4, 7):
        for x in range(35, 38):
            map1[y][x] = "ice"  # top right

    # Sand zones (orange)
    for y in range(0, 4):
        for x in range(13, 15):
            map1[y][x] = "sand"  # top
    for y in range(13, 15):
        for x in range(18, 29):
            map1[y][x] = "sand"  # center wide area
    for y in range(22, 25):
        for x in range(38, 46):
            map1[y][x] = "sand"  # bottom right

    # Bush areas ("bush")
    for y in range(18, 24):
        for x in range(3, 7):
            map1[y][x] = "bush"  # bottom left area 1
    for y in range(20, 24):
        for x in range(7, 11):
            map1[y][x] = "bush"  # bottom left area 2
    for y in range(2, 8):
        for x in range(29, 32):
            map1[y][x] = "bush"  # vertical top right
    for y in range(18, 21):
        for x in range(22, 29):
            map1[y][x] = "bush"  # center bottom

    return map1


# creates a map based on an input text file
def get_map(input=None) -> list[list[str]]:
    # error handling: if no file is provided, the default map from above will be used
    if input is None:
        print(
            "Note: Since no map file was provided for the level,"
            "a default map will be used."
        )
        return get_map1()
    # if a file is provided
    file = open(input, "r", encoding="utf-8")
    lines = file.readlines()
    if len(lines) != config.ROWS - 2:  # check for correct formatting of the input file
        raise ValueError(
            "The file must contain exactly "
            + str(config.ROWS - 2)
            + " lines, but got "
            + str(len(lines))
            + " !"
        )
    map = []
    for line in lines:
        lineList = list(line)  # Convert line to a list of characters
        if lineList[-1] == "\n":  # Remove newline character at the end
            lineList.pop()
        if (
            len(lineList) != config.COLUMNS - 2
        ):  # Check that each line has the expected number of columns
            raise ValueError(
                "Each line in the file must contain exactly "
                + str(config.COLUMNS - 2)
                + " columns, but got "
                + str(len(lineList))
                + " !"
            )
        for i in range(len(lineList)):
            if lineList[i] == "g":  # ground
                lineList[i] = "ground"
            elif lineList[i] == "w":  # wall
                lineList[i] = "wall"
            elif lineList[i] == "l":  # lava
                lineList[i] = "lava"
            elif lineList[i] == "i":  # ice
                lineList[i] = "ice"
            elif lineList[i] == "s":  # sand
                lineList[i] = "sand"
            elif lineList[i] == "b":  # bushes
                lineList[i] = "bush"
            else:  # in case of wrong input
                lineList[i] = "ground"
        map.append(lineList)
    file.close()
    return map
