Eryon_Umbra_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Eryon_Umbra_RespawnCheckpoint
	.byte 0

@ Native Eryon whiteout checkpoint. Re-entry updates the safe return town.
Eryon_Umbra_RespawnCheckpoint:
	setrespawn HEAL_LOCATION_ERYON_UMBRA
	end

@ Umbra's cargo inspector connects the mountain mystery to the fifth gym city.
EryonUmbra_EventScript_Inspector::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonUmbra_EventScript_InspectorClue
	msgbox EryonUmbra_Text_InspectorBefore, MSGBOX_DEFAULT
	release
	end

EryonUmbra_EventScript_InspectorClue::
	msgbox EryonUmbra_Text_InspectorClue, MSGBOX_DEFAULT
	release
	end

EryonUmbra_EventScript_GymGuide::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonUmbra_EventScript_GymGuideClue
	msgbox EryonUmbra_Text_GymGuideBefore, MSGBOX_DEFAULT
	release
	end

EryonUmbra_EventScript_GymGuideClue::
	msgbox EryonUmbra_Text_GymGuideClue, MSGBOX_DEFAULT
	release
	end

EryonUmbra_Text_InspectorBefore:
	.string "FISCAL: Umbra recebe\n"
	.string "cargas de todo o vale.\p"
	.string "Ultimamente alguns selos\n"
	.string "chegam adulterados.$"

EryonUmbra_Text_InspectorClue:
	.string "FISCAL: Caixas com o\n"
	.string "simbolo da ECLIPSE?\p"
	.string "Foram levadas ao setor\n"
	.string "industrial de Umbra.\p"
	.string "Os registros nao batem.$"

EryonUmbra_Text_GymGuideBefore:
	.string "GUIA: O GINASIO de Umbra\n"
	.string "usa sombras e venenos.\p"
	.string "Explore as ruas antes\n"
	.string "de desafiar o lider.$"

EryonUmbra_Text_GymGuideClue:
	.string "GUIA: A EQUIPE ECLIPSE\n"
	.string "anda pela cidade.\p"
	.string "Nosso lider investiga\n"
	.string "o movimento de cargas.$"

@ The Eclipse courier hints at a larger network without forcing a premature boss fight.
EryonUmbra_EventScript_EclipseCourier::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonUmbra_EventScript_EclipseCourierExposed
	msgbox EryonUmbra_Text_EclipseCourierBefore, MSGBOX_DEFAULT
	release
	end

EryonUmbra_EventScript_EclipseCourierExposed::
	msgbox EryonUmbra_Text_EclipseCourierExposed, MSGBOX_DEFAULT
	release
	end

EryonUmbra_EventScript_IndustrialManifest::
	lock
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonUmbra_EventScript_IndustrialManifestClue
	msgbox EryonUmbra_Text_IndustrialManifestBefore, MSGBOX_DEFAULT
	release
	end

EryonUmbra_EventScript_IndustrialManifestClue::
	msgbox EryonUmbra_Text_IndustrialManifestClue, MSGBOX_DEFAULT
	release
	end

EryonUmbra_Text_EclipseCourierBefore:
	.string "ENTREGADOR: Nao toque\n"
	.string "nas caixas da fabrica.\p"
	.string "O destino e assunto\n"
	.string "exclusivo da empresa.$"

EryonUmbra_Text_EclipseCourierExposed:
	.string "ECLIPSE: Reconheceu\n"
	.string "nosso simbolo?\p"
	.string "O gelo e os cristais\n"
	.string "sao so o comeco.\p"
	.string "Nao interfira em Umbra.$"

EryonUmbra_Text_IndustrialManifestBefore:
	.string "Uma lista de remessas\n"
	.string "esta presa no portao.\p"
	.string "Os codigos estao\n"
	.string "parcialmente apagados.$"

EryonUmbra_Text_IndustrialManifestClue:
	.string "O manifesto cita gelo\n"
	.string "e cristais da serra!\p"
	.string "Destino seguinte: a\n"
	.string "regiao das cachoeiras.$"

@ Umbra's port manifest foreshadows the relay installation at Solaris.
EryonUmbra_EventScript_DesertCargoLedger::
	lock
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonUmbra_EventScript_DesertCargoLedgerClue
	msgbox EryonUmbra_Text_DesertCargoLedgerBefore, MSGBOX_DEFAULT
	release
	end

EryonUmbra_EventScript_DesertCargoLedgerClue::
	msgbox EryonUmbra_Text_DesertCargoLedgerClue, MSGBOX_DEFAULT
	release
	end

EryonUmbra_Text_DesertCargoLedgerBefore:
	.string "REGISTRO: Maquinas de\n"
	.string "medicao foram enviadas.\p"
	.string "Destino: SOLARIS.\n"
	.string "Remetente: desconhecido.$"

EryonUmbra_Text_DesertCargoLedgerClue:
	.string "REGISTRO: Material\n"
	.string "cristalino de Umbra.\p"
	.string "Transporte via SOLARIS\n"
	.string "ate a usina de IGNIVAR.$"

@ Eryon: NYX is the city leader, separate from the Gym guide.
EryonUmbra_EventScript_GymLeader::
	lock
	faceplayer
	goto_if_set FLAG_BADGE05_GET, EryonUmbra_EventScript_GymAfter
	goto_if_unset FLAG_BADGE04_GET, EryonUmbra_EventScript_GymNotReady
	goto EryonUmbra_EventScript_GymOffer
	end

@ Tactical badge battle — Umbra: ace level 41, badge 5.
EryonUmbra_EventScript_GymOffer::
	msgbox EryonUmbra_Text_GymOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonUmbra_EventScript_GymDecline
	closemessage
	trainerbattle_single TRAINER_ERYON_GYM_UMBRA, EryonUmbra_Text_GymIntro, EryonUmbra_Text_GymLoss, EryonUmbra_EventScript_GymVictory, FALSE
	msgbox EryonUmbra_Text_GymAfter, MSGBOX_DEFAULT
	release
	end

EryonUmbra_EventScript_GymVictory::
	message EryonUmbra_Text_GymBadge
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	setflag FLAG_BADGE05_GET
	msgbox EryonUmbra_Text_GymAfter, MSGBOX_DEFAULT
	release
	end

EryonUmbra_EventScript_GymDecline::
	closemessage
	release
	end

EryonUmbra_EventScript_GymNotReady::
	msgbox EryonUmbra_Text_GymNotReady, MSGBOX_DEFAULT
	release
	end

EryonUmbra_EventScript_GymAfter::
	goto_if_set FLAG_ERYON_ECLIPSE_NETWORK_SHUT_DOWN, EryonUmbra_EventScript_GymAfterEclipse
	msgbox EryonUmbra_Text_GymAfter, MSGBOX_DEFAULT
	release
	end

EryonUmbra_Text_GymOffer:
	.string "NYX: Meu GINASIO\n"
	.string "treina com sombras.\p"
	.string "Desafiar meu time\n"
	.string "de Pokemon agora?$"

EryonUmbra_Text_GymIntro:
	.string "NYX: Mostre sua\n"
	.string "forca e estrategia!$"

EryonUmbra_Text_GymLoss:
	.string "NYX: Voce encontrou\n"
	.string "uma boa resposta!$"

EryonUmbra_Text_GymBadge:
	.string "Venceu o 5o GINASIO!\p"
	.string "Recebeu a INSIGNIA\n"
	.string "de numero 5!$"

EryonUmbra_Text_GymAfter:
	.string "NYX: Bela vitoria!\p"
	.string "Investigue os selos da ECLIPSE.$"

EryonUmbra_Text_GymNotReady:
	.string "NYX: Primeiro,\n"
	.string "conquiste a INSIGNIA\n"
	.string "do GINASIO anterior.$"
 
@ Epilogue only; previous badge, Serra and battle routes remain unchanged.
EryonUmbra_EventScript_GymAfterEclipse::
	msgbox EryonUmbra_Text_GymAfterEclipse, MSGBOX_DEFAULT
	release
	end

EryonUmbra_Text_GymAfterEclipse:
	.string "NYX: As cargas ilegais\n"
	.string "foram interrompidas.\p"
	.string "UMBRA voltou a ser uma\n"
	.string "cidade de caminhos livres.$"
