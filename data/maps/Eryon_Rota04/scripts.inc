Eryon_Rota04_MapScripts::
	.byte 0

@ The orchard scout points travelers toward the longer regional trail.
EryonRota04_EventScript_OrchardScout::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_ORCHARD_RELAY_TRACED, EryonRota04_EventScript_ScoutTraced
	goto_if_set FLAG_ERYON_ORCHARD_LEDGER_READ, EryonRota04_EventScript_ScoutLedger
	msgbox EryonRota04_Text_OrchardScout, MSGBOX_DEFAULT
	release
	end

EryonRota04_Text_OrchardScout:
	.string "EXPLORADOR: Os pomares ficam\n"
	.string "para oeste, perto da vila.\p"
	.string "A leste, a trilha encontra\n"
	.string "a antiga Rota 03.$"


@ Optional investigation on existing orchard and rocky lookout terrain.
EryonRota04_EventScript_OrchardLedger::
	lock
	goto_if_set FLAG_ERYON_ORCHARD_LEDGER_READ, EryonRota04_EventScript_LedgerAgain
	msgbox EryonRota04_Text_LedgerFirst, MSGBOX_DEFAULT
	setflag FLAG_ERYON_ORCHARD_LEDGER_READ
	release
	end

EryonRota04_EventScript_LedgerAgain::
	msgbox EryonRota04_Text_LedgerAgain, MSGBOX_DEFAULT
	release
	end

@ The road remains open regardless of optional clue flags.
EryonRota04_EventScript_RelayMarker::
	lock
	goto_if_set FLAG_ERYON_ORCHARD_RELAY_TRACED, EryonRota04_EventScript_RelayAgain
	goto_if_unset FLAG_ERYON_ORCHARD_LEDGER_READ, EryonRota04_EventScript_RelayUnclear
	msgbox EryonRota04_Text_RelayDecoded, MSGBOX_DEFAULT
	setflag FLAG_ERYON_ORCHARD_RELAY_TRACED
	release
	end

EryonRota04_EventScript_RelayUnclear::
	msgbox EryonRota04_Text_RelayUnclear, MSGBOX_DEFAULT
	release
	end

EryonRota04_EventScript_RelayAgain::
	msgbox EryonRota04_Text_RelayAgain, MSGBOX_DEFAULT
	release
	end

EryonRota04_EventScript_Lookout::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_ORCHARD_RELAY_TRACED, EryonRota04_EventScript_LookoutTraced
	goto_if_ge VAR_ERYON_LUMINA_CLUE_FOUND, 1, EryonRota04_EventScript_LookoutClue
	msgbox EryonRota04_Text_LookoutBefore, MSGBOX_DEFAULT
	release
	end

EryonRota04_EventScript_LookoutClue::
	msgbox EryonRota04_Text_LookoutClue, MSGBOX_DEFAULT
	release
	end

EryonRota04_EventScript_LookoutTraced::
	msgbox EryonRota04_Text_LookoutTraced, MSGBOX_DEFAULT
	release
	end

EryonRota04_EventScript_ScoutLedger::
	msgbox EryonRota04_Text_ScoutLedger, MSGBOX_DEFAULT
	release
	end

EryonRota04_EventScript_ScoutTraced::
	msgbox EryonRota04_Text_ScoutTraced, MSGBOX_DEFAULT
	release
	end

EryonRota04_Text_LedgerFirst:
	.string "Um livro molhado repousa\n"
	.string "entre as raizes do pomar.\p"
	.string "Cargas noturnas de cristal\n"
	.string "seguiam ate NEONARA.\p"
	.string "Uma pagina cita o marco\n"
	.string "de pedra ao sul da rota.$"

EryonRota04_Text_LedgerAgain:
	.string "O registro menciona cargas\n"
	.string "e o marco ao sul da rota.$"

EryonRota04_Text_RelayUnclear:
	.string "Ha um emissor quebrado\n"
	.string "sob a pedra antiga.\p"
	.string "Os codigos nao fazem\n"
	.string "sentido sem um registro.$"

EryonRota04_Text_RelayDecoded:
	.string "Os codigos batem com o\n"
	.string "livro achado no pomar!\p"
	.string "A ECLIPSE redirecionou\n"
	.string "cristais para NEONARA.\p"
	.string "A rede usa a energia da\n"
	.string "cidade para testar sinais.$"

EryonRota04_Text_RelayAgain:
	.string "O emissor confirma a rota\n"
	.string "das cargas da ECLIPSE.\p"
	.string "Um tecnico em NEONARA\n"
	.string "pode explicar os sinais.$"

EryonRota04_Text_LookoutBefore:
	.string "VIGIA: Daqui vejo as trilhas\n"
	.string "e as luzes de NEONARA.\p"
	.string "Algumas carrocas passam\n"
	.string "somente de madrugada.$"

EryonRota04_Text_LookoutClue:
	.string "VIGIA: O simbolo do bosque\n"
	.string "tambem apareceu aqui.\p"
	.string "Procure o registro perdido\n"
	.string "no pomar ao norte.$"

EryonRota04_Text_LookoutTraced:
	.string "VIGIA: Agora entendo as\n"
	.string "cargas e os sinais!\p"
	.string "Avise o tecnico de NEONARA\n"
	.string "antes que a rede aumente.$"

EryonRota04_Text_ScoutLedger:
	.string "EXPLORADOR: Esse registro\n"
	.string "nao devia estar no pomar.\p"
	.string "O marco de pedra fica\n"
	.string "ao sul desta estrada.$"

EryonRota04_Text_ScoutTraced:
	.string "EXPLORADOR: Voce ligou\n"
	.string "o pomar ao sinal da serra!\p"
	.string "Em NEONARA, as luzes\n"
	.string "podem dar outra pista.$"


@ Visible guide to the otherwise subtle ledger inspection tile in the grove.
EryonRota04_EventScript_OrchardKeeper::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_ORCHARD_RELAY_TRACED, EryonRota04_EventScript_KeeperTraced
	goto_if_set FLAG_ERYON_ORCHARD_LEDGER_READ, EryonRota04_EventScript_KeeperLedger
	msgbox EryonRota04_Text_KeeperBefore, MSGBOX_DEFAULT
	release
	end

EryonRota04_EventScript_KeeperLedger::
	msgbox EryonRota04_Text_KeeperLedger, MSGBOX_DEFAULT
	release
	end

EryonRota04_EventScript_KeeperTraced::
	msgbox EryonRota04_Text_KeeperTraced, MSGBOX_DEFAULT
	release
	end

EryonRota04_Text_KeeperBefore:
	.string "CUIDADORA: Vi um livro\n"
	.string "caido perto das raizes.\p"
	.string "Procure a noroeste daqui,\n"
	.string "entre as arvores do pomar.$"

EryonRota04_Text_KeeperLedger:
	.string "CUIDADORA: Encontrou o livro?\p"
	.string "O vigia viu carrocas perto\n"
	.string "das pedras ao sul da rota.$"

EryonRota04_Text_KeeperTraced:
	.string "CUIDADORA: Entao a ECLIPSE\n"
	.string "usou mesmo nossos pomares!\p"
	.string "A vila precisa saber o que\n"
	.string "voce achou no transmissor.$"
