Eryon_Neonara_MapScripts::
	.byte 0

@ Neonara is the future second gym city; interiors remain unfinished.
EryonNeonara_EventScript_Resident::
	lock
	faceplayer
	msgbox EryonNeonara_Text_Resident, MSGBOX_DEFAULT
	release
	end

EryonNeonara_Text_Resident:
	.string "MORADORA: Bem-vindo a\n"
	.string "Neonara, cidade das luzes!\p"
	.string "O caminho oeste leva a\n"
	.string "Rota 03 e aos pomares.$"

@ City power grid reacts to the forest and crystal investigation.
EryonNeonara_EventScript_Technician::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonNeonara_EventScript_TechnicianAfterClue
	msgbox EryonNeonara_Text_TechnicianBefore, MSGBOX_DEFAULT
	release
	end

EryonNeonara_EventScript_TechnicianAfterClue::
	msgbox EryonNeonara_Text_TechnicianAfter, MSGBOX_DEFAULT
	release
	end

EryonNeonara_EventScript_GymSteward::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_LUMINA_CLUE_FOUND, 1, EryonNeonara_EventScript_GymStewardClue
	msgbox EryonNeonara_Text_GymStewardBefore, MSGBOX_DEFAULT
	release
	end

EryonNeonara_EventScript_GymStewardClue::
	msgbox EryonNeonara_Text_GymStewardClue, MSGBOX_DEFAULT
	release
	end

EryonNeonara_Text_TechnicianBefore:
	.string "TECNICO: As luzes da\n"
	.string "cidade estao oscilando.\p"
	.string "A energia da serra pode\n"
	.string "explicar esse misterio.$"

EryonNeonara_Text_TechnicianAfter:
	.string "TECNICO: Os cristais\n"
	.string "roubados reagem a luz!\p"
	.string "A ECLIPSE pode estar\n"
	.string "testando uma nova fonte.$"

EryonNeonara_Text_GymStewardBefore:
	.string "GUIA: O GINASIO de Neonara\n"
	.string "esta sendo preparado.\p"
	.string "Explore a cidade e\n"
	.string "converse com os moradores.$"

EryonNeonara_Text_GymStewardClue:
	.string "GUIA: O simbolo da ECLIPSE\n"
	.string "apareceu no bosque?\p"
	.string "As luzes da cidade\n"
	.string "tambem estao estranhas.$"
