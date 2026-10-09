Eryon_VilaDaNeblina_MapScripts::
	.byte 0

@ An elder hints at the frozen trail without unlocking an unfinished area.
EryonVilaNeblina_EventScript_Elder::
	lock
	faceplayer
	msgbox EryonVilaNeblina_Text_Elder, MSGBOX_DEFAULT
	release
	end

EryonVilaNeblina_Text_Elder:
	.string "ANCIÃ: A neblina esconde\n"
	.string "os caminhos mais antigos.\p"
	.string "A Trilha Glacial fica alem\n"
	.string "da vila, entre montanhas.$"
