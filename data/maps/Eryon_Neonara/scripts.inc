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
