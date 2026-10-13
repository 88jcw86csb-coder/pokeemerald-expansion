Eryon_VilaDaNeblina_MapScripts::
	.byte 0

@ An elder hints at the frozen trail without unlocking an unfinished area.
EryonVilaNeblina_EventScript_Elder::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_MIST_SIGNAL_REPAIRED, EryonVilaNeblina_EventScript_ElderSignal
	msgbox EryonVilaNeblina_Text_Elder, MSGBOX_DEFAULT
	release
	end

EryonVilaNeblina_Text_Elder:
	.string "ANCIA: A neblina esconde\n"
	.string "os caminhos mais antigos.\p"
	.string "A Trilha Glacial fica alem\n"
	.string "da vila, entre montanhas.$"

@ The village receives the restored mountain warning system.
EryonVilaNeblina_EventScript_ElderSignal::
	msgbox EryonVilaNeblina_Text_ElderSignal, MSGBOX_DEFAULT
	release
	end

EryonVilaNeblina_Text_ElderSignal:
	.string "ANCIA: A vila recebeu\n"
	.string "seu aviso de NEONARA!\p"
	.string "A neblina nao esconde\n"
	.string "mais a carga da ECLIPSE.\p"
	.string "FROSTHEIM fica no fim\n"
	.string "da TRILHA GLACIAL.$"
