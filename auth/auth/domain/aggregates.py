class Account:
    def __init__(self, id : int, username : str):
        self.id = id
        self.username = username

class Profile:
    def __init__(self, id : int, username : str):
        self.id = id
        self.username = username

        self.first_name : str
        self.last_name : str
        self.birthdate : str
