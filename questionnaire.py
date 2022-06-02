class Questionnaire():
	def __init__(self, photo, name, age, description, user_link, chat_id):
		self.photo = photo
		self.name = name
		self.age = age
		self.description = description
		self.user_link = user_link
		self.chat_id = chat_id

	def getPreparedText(self):
		return f"{self.name}, {self.age}\n{self.description}"