def show_main_menu(u_id):
	print("Main menu for " + str(u_id))

bot_functions = {
	"главное меню": show_main_menu
	"анкеты": show_questionnaires,
	"профиль": show_profile,
	"взаимные лайки": show_mutual_likes,
	"входящие лайки": show_incoming_likes,
	"исходящие лайки": show_outcoming_likes
}