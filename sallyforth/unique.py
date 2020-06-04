class Unique:
    """
    Simple untility class that only exists to be different.
    """
    def __str__(self):
        return f'Unique[{id(self)}]'
