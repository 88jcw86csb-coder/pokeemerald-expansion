Eryon_VilaDosPomares_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Eryon_VilaDosPomares_RespawnCheckpoint
	.byte 0

@ Rest stop: remember the safe village, preserve all Eclipse events.
Eryon_VilaDosPomares_RespawnCheckpoint:
	setrespawn HEAL_LOCATION_ERYON_VILA_DOS_POMARES
	end


@ A real rest stop and story beat before the second gym area.
EryonPomaresVila_EventScript_Healer::
	lock
	faceplayer
	msgbox EryonPomaresVila_Text_Healer, MSGBOX_DEFAULT
	special HealPlayerParty
	release
	end

EryonPomaresVila_EventScript_Elder::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_LUMINA_CLUE_FOUND, 1, EryonPomaresVila_EventScript_ElderInformed
	msgbox EryonPomaresVila_Text_ElderBefore, MSGBOX_DEFAULT
	release
	end

EryonPomaresVila_EventScript_ElderInformed::
	msgbox EryonPomaresVila_Text_ElderInformed, MSGBOX_DEFAULT
	release
	end

EryonPomaresVila_EventScript_Courier::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_ORCHARD_RELAY_TRACED, EryonPomaresVila_EventScript_CourierRelay
	goto_if_set FLAG_ERYON_ORCHARD_LEDGER_READ, EryonPomaresVila_EventScript_CourierLedger
	msgbox EryonPomaresVila_Text_Courier, MSGBOX_DEFAULT
	release
	end

EryonPomaresVila_EventScript_Notice::
	lock
	msgbox EryonPomaresVila_Text_Notice, MSGBOX_DEFAULT
	release
	end

EryonPomaresVila_Text_Healer:
	.string "CUIDADORA: Descanse\n"
	.string "antes da proxima rota.\p"
	.string "Vou curar seus Pokemon\n"
	.string "sem cobrar nada.$"

EryonPomaresVila_Text_ElderBefore:
	.string "ANCIA: Nossos campos\n"
	.string "eram sempre tranquilos.\p"
	.string "Um som estranho vem\n"
	.string "debaixo das raizes.$"

EryonPomaresVila_Text_ElderInformed:
	.string "ANCIA: O sinal encontrado\n"
	.string "no BOSQUE e importante.\p"
	.string "Uma carga misteriosa\n"
	.string "seguiu para NEONARA.$"

EryonPomaresVila_Text_Courier:
	.string "ENTREGADOR: Deixei\n"
	.string "caixas no pomar.\p"
	.string "Nunca soube quem\n"
	.string "pagou o transporte.$"

EryonPomaresVila_Text_Notice:
	.string "VILA DOS POMARES:\n"
	.string "centro de descanso.\p"
	.string "Saida leste: ROTA 04\n"
	.string "rumo a NEONARA.$"


@ Optional side-story acknowledgements; original village checkpoint retained.
EryonPomaresVila_EventScript_CourierLedger::
	msgbox EryonPomaresVila_Text_CourierLedger, MSGBOX_DEFAULT
	release
	end

EryonPomaresVila_EventScript_CourierRelay::
	msgbox EryonPomaresVila_Text_CourierRelay, MSGBOX_DEFAULT
	release
	end

EryonPomaresVila_Text_CourierLedger:
	.string "ENTREGADOR: O livro de\n"
	.string "cargas estava no pomar?\p"
	.string "Vi um vigia perto das\n"
	.string "pedras ao sul da ROTA 04.$"

EryonPomaresVila_Text_CourierRelay:
	.string "ENTREGADOR: A ECLIPSE\n"
	.string "escondia seus embarques!\p"
	.string "Vou informar a vila.\n"
	.string "Mostre o sinal em NEONARA.$"
