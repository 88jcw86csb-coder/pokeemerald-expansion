EryonRota01_EventScript_Explorer::
	lock
	faceplayer
	msgbox EryonRota01_Text_Explorer, MSGBOX_DEFAULT
	release
	end

EryonRota01_Text_Explorer:
	.string "O Bosque de Lumina fica adiante!\p"
	.string "Dizem que as luzes entre as arvores\n"
	.string "mudaram nos ultimos dias.$"

@ An optional trail marker encourages exploring the forest before reaching Verdelume.
EryonRota01_EventScript_TrailMarker::
	lock
	msgbox EryonRota01_Text_TrailMarker, MSGBOX_DEFAULT
	release
	end

EryonRota01_Text_TrailMarker:
	.string "ROTA 01 - TRILHA DA AURORA\p"
	.string "Adiante: Bosque de Lumina.\n"
	.string "Observe as clareiras com calma.$"
