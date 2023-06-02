class User:
    def __init__(self, user_id=0, usernamae="", user_link="", age=0, city="", description="", photo=0x0):
        self.user_id = user_id
        self.username = usernamae
        self.user_link = user_link
        self.age = age
        self.city = city
        self.description = description
        self.photo = photo

    def get_listed_params(self):
        return [self.user_id, self.username, self.age, self.city, self.descriptions, self.photo, self.user_link]
    
    @property
    def questionnaire_text(self):
        return f"{self.username} {self.age}, {self.city}\n{self.description}"
