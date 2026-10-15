Eryon_Neonara_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Eryon_Neonara_RespawnCheckpoint
	.byte 0

@ Native whiteout/Teleport checkpoint. Preserve all existing NPC and gym scripts.
Eryon_Neonara_RespawnCheckpoint:
	setrespawn HEAL_LOCATION_ERYON_NEONARA
	end

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
	goto_if_set FLAG_ERYON_MIST_SIGNAL_REPAIRED, EryonNeonara_EventScript_TechnicianRestored
	goto_if_set FLAG_BADGE02_GET, EryonNeonara_EventScript_TechnicianBadge
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

@ Eryon: VOLT is the city leader, separate from the Gym guide.
EryonNeonara_EventScript_GymLeader::
	lock
	faceplayer
	goto_if_set FLAG_BADGE02_GET, EryonNeonara_EventScript_GymAfter
	goto_if_unset FLAG_BADGE01_GET, EryonNeonara_EventScript_GymNotReady
	goto EryonNeonara_EventScript_GymOffer
	end

@ Tactical badge battle — Neonara: ace level 25, badge 2.
EryonNeonara_EventScript_GymOffer::
	msgbox EryonNeonara_Text_GymOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonNeonara_EventScript_GymDecline
	closemessage
	trainerbattle_single TRAINER_ERYON_GYM_NEONARA, EryonNeonara_Text_GymIntro, EryonNeonara_Text_GymLoss, EryonNeonara_EventScript_GymVictory, FALSE
	msgbox EryonNeonara_Text_GymAfter, MSGBOX_DEFAULT
	release
	end

EryonNeonara_EventScript_GymVictory::
	message EryonNeonara_Text_GymBadge
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	setflag FLAG_BADGE02_GET
	msgbox EryonNeonara_Text_GymAfter, MSGBOX_DEFAULT
	release
	end

EryonNeonara_EventScript_GymDecline::
	closemessage
	release
	end

EryonNeonara_EventScript_GymNotReady::
	msgbox EryonNeonara_Text_GymNotReady, MSGBOX_DEFAULT
	release
	end

EryonNeonara_EventScript_GymAfter::
	msgbox EryonNeonara_Text_GymAfter, MSGBOX_DEFAULT
	release
	end

EryonNeonara_Text_GymOffer:
	.string "VOLT: Meu GINASIO\n"
	.string "treina com eletricidade.\p"
	.string "Desafiar meu time\n"
	.string "de Pokemon agora?$"

EryonNeonara_Text_GymIntro:
	.string "VOLT: Mostre sua\n"
	.string "forca e estrategia!$"

EryonNeonara_Text_GymLoss:
	.string "VOLT: Voce encontrou\n"
	.string "uma boa resposta!$"

EryonNeonara_Text_GymBadge:
	.string "Venceu o 2o GINASIO!\p"
	.string "Recebeu a INSIGNIA\n"
	.string "de numero 2!$"

EryonNeonara_Text_GymAfter:
	.string "VOLT: Bela vitoria!\p"
	.string "As luzes voltarao a brilhar.$"

EryonNeonara_Text_GymNotReady:
	.string "VOLT: Primeiro,\n"
	.string "conquiste a INSIGNIA\n"
	.string "do GINASIO anterior.$"

@ Gym 2 victory opens a non-mandatory weather transmitter quest.
EryonNeonara_EventScript_TechnicianBadge::
	msgbox EryonNeonara_Text_TechnicianBadge, MSGBOX_DEFAULT
	release
	end

EryonNeonara_EventScript_TechnicianRestored::
	msgbox EryonNeonara_Text_TechnicianRestored, MSGBOX_DEFAULT
	release
	end

EryonNeonara_Text_TechnicianBadge:
	.string "TECNICO: Essa INSIGNIA\n"
	.string "permite usar meu painel!\p"
	.string "Visite o observatorio\n"
	.string "nas COLINAS DA NEBLINA.\p"
	.string "O sinal pode revelar\n"
	.string "a carga da ECLIPSE.$"

EryonNeonara_Text_TechnicianRestored:
	.string "TECNICO: O sinal voltou!\p"
	.string "A VILA DA NEBLINA e\n"
	.string "FROSTHEIM receberam\n"
	.string "avisos sobre a ECLIPSE.$"
