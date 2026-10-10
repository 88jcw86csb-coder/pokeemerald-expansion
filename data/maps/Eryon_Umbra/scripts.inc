Eryon_Umbra_MapScripts::
	.byte 0

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
