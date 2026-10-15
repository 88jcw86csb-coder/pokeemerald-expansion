Eryon_VilaDaNeblina_MapScripts::
	.byte 0

@ An elder hints at the frozen trail without unlocking an unfinished area.
EryonVilaNeblina_EventScript_Elder::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_GLACIAL_BERGMITE_RESOLVED, EryonVilaNeblina_EventScript_ElderBergmiteSafe
	goto_if_set FLAG_ERYON_GLACIAL_RIFT_LOG_READ, EryonVilaNeblina_EventScript_ElderRiftFound
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

@ The mist village hears news from the optional northern ice research path.
EryonVilaNeblina_EventScript_ElderRiftFound::
	msgbox EryonVilaNeblina_Text_ElderRiftFound, MSGBOX_DEFAULT
	release
	end

EryonVilaNeblina_EventScript_ElderBergmiteSafe::
	msgbox EryonVilaNeblina_Text_ElderBergmiteSafe, MSGBOX_DEFAULT
	release
	end

EryonVilaNeblina_Text_ElderRiftFound:
	.string "ANCIA: Encontrou o\n"
	.string "DIARIO GLACIAL?\p"
	.string "A ECLIPSE pesquisava\n"
	.string "uma fenda na encosta.\p"
	.string "Proteja os Pokemon\n"
	.string "que vivem no gelo.$"

EryonVilaNeblina_Text_ElderBergmiteSafe:
	.string "ANCIA: A FENDA GLACIAL\n"
	.string "esta em paz novamente!\p"
	.string "A vila agradece\n"
	.string "por salvar BERGMITE.$"
