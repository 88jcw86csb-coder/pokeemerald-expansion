Eryon_LigaRecepcao_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Eryon_LigaRecepcao_RespawnCheckpoint
	.byte 0

@ Native Eryon whiteout checkpoint. Re-entry updates the safe return town.
Eryon_LigaRecepcao_RespawnCheckpoint:
	setrespawn HEAL_LOCATION_ERYON_LIGA_RECEPCAO
	end

EryonLigaLobby_EventScript_Medic::
	lock
	faceplayer
	msgbox EryonLigaLobby_Text_Medic, MSGBOX_DEFAULT
	special HealPlayerParty
	release
	end

EryonLigaLobby_EventScript_Register::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_QUALIFIED, EryonLigaLobby_EventScript_Qualified
	goto_if_unset FLAG_BADGE01_GET, EryonLigaLobby_EventScript_MissingBadges
	goto_if_unset FLAG_BADGE02_GET, EryonLigaLobby_EventScript_MissingBadges
	goto_if_unset FLAG_BADGE03_GET, EryonLigaLobby_EventScript_MissingBadges
	goto_if_unset FLAG_BADGE04_GET, EryonLigaLobby_EventScript_MissingBadges
	goto_if_unset FLAG_BADGE05_GET, EryonLigaLobby_EventScript_MissingBadges
	goto_if_unset FLAG_BADGE06_GET, EryonLigaLobby_EventScript_MissingBadges
	goto_if_unset FLAG_BADGE07_GET, EryonLigaLobby_EventScript_MissingBadges
	goto_if_unset FLAG_BADGE08_GET, EryonLigaLobby_EventScript_MissingBadges
	msgbox EryonLigaLobby_Text_RegisterOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonLigaLobby_EventScript_Decline
	closemessage
	warp MAP_ERYON_LIGA_CLASSIFICATORIA, 22, 30
	waitstate
	end

EryonLigaLobby_EventScript_Qualified::
	msgbox EryonLigaLobby_Text_Qualified, MSGBOX_DEFAULT
	closemessage
	warp MAP_ERYON_LIGA_RECUPERACAO, 12, 14
	waitstate
	end

EryonLigaLobby_EventScript_MissingBadges::
	msgbox EryonLigaLobby_Text_MissingBadges, MSGBOX_DEFAULT
	release
	end

EryonLigaLobby_EventScript_Decline::
	msgbox EryonLigaLobby_Text_Decline, MSGBOX_DEFAULT
	release
	end

EryonLigaLobby_EventScript_Rules::
	lock
	faceplayer
	msgbox EryonLigaLobby_Text_Rules, MSGBOX_DEFAULT
	release
	end

EryonLigaLobby_EventScript_Notice::
	lock
	msgbox EryonLigaLobby_Text_Notice, MSGBOX_DEFAULT
	release
	end

EryonLigaLobby_Text_Medic:
	.string "ENFERMEIRA: Vou curar\n"
	.string "seus Pokemon antes\n"
	.string "da CLASSIFICATORIA.$"

EryonLigaLobby_Text_RegisterOffer:
	.string "OFICIAL: Tem as 8\n"
	.string "INSIGNIAS de ERYON!\p"
	.string "Iniciar oito batalhas\n"
	.string "seguidas agora?$"

EryonLigaLobby_Text_Qualified:
	.string "OFICIAL: Voce venceu\n"
	.string "todas as oito fases!\p"
	.string "Siga para a sala de\n"
	.string "cura e para a ELITE 4.$"

EryonLigaLobby_Text_MissingBadges:
	.string "OFICIAL: A inscricao\n"
	.string "exige 8 INSIGNIAS.\p"
	.string "Volte apos vencer os\n"
	.string "oito lideres de ERYON.$"

EryonLigaLobby_Text_Decline:
	.string "OFICIAL: Boa sorte!\n"
	.string "Volte quando quiser.$"

EryonLigaLobby_Text_Rules:
	.string "REGRAS: Oito fases.\n"
	.string "Uma vitoria por fase.\p"
	.string "Se perder, perdera\n"
	.string "dinheiro e voltara\n"
	.string "ao inicio da serie.$"

EryonLigaLobby_Text_Notice:
	.string "CAMPEONATO DA LIGA:\n"
	.string "Etapa 1: 8 duelos.\p"
	.string "Etapa 2: cura livre.\n"
	.string "Etapa 3: ELITE FOUR.$"
