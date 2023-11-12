class Room:
    def __init__(self, name, matrix, total_rooms, current_position):
        self.name = name
        self.matrix = matrix
        self.total_rooms = total_rooms
        self.current_position = current_position

    def get_current_room(self):
        row_index = -1
        col_index = -1

        for i in range(len(self.matrix)):
            if '*' in self.matrix[i]:
                row_index = i
                col_index = self.matrix[i].index('*')
                break

        return row_index, col_index