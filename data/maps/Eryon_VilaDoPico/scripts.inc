Eryon_VilaDoPico_MapScripts::
	.byte 0

@ Quiet resting stop between the dragon trail and the final gym city.
EryonPico_EventScript_Caretaker::
	lock
	faceplayer
	msgbox EryonPico_Text_Caretaker, MSGBOX_DEFAULT
	special HealPlayerParty
	release
	end

EryonPico_EventScript_Elder::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonPico_EventScript_ElderClue
	msgbox EryonPico_Text_ElderBefore, MSGBOX_DEFAULT
	release
	end

EryonPico_EventScript_ElderClue::
	msgbox EryonPico_Text_ElderClue, MSGBOX_DEFAULT
	release
	end

EryonPico_EventScript_Messenger::
	lock
	faceplayer
	msgbox EryonPico_Text_Messenger, MSGBOX_DEFAULT
	release
	end

EryonPico_EventScript_Geologist::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonPico_EventScript_GeologistClue
	msgbox EryonPico_Text_GeologistBefore, MSGBOX_DEFAULT
	release
	end

EryonPico_EventScript_GeologistClue::
	msgbox EryonPico_Text_GeologistClue, MSGBOX_DEFAULT
	release
	end

EryonPico_EventScript_VillageNotice::
	lock
	msgbox EryonPico_Text_Notice, MSGBOX_DEFAULT
	release
	end

EryonPico_EventScript_DrakoniaRoad::
	lock
	msgbox EryonPico_Text_Road, MSGBOX_DEFAULT
	release
	end

EryonPico_Text_Caretaker:
	.string "CUIDADORA: O ar da\n"
	.string "montanha e bem frio.\p"
	.string "Vou curar sua equipe\n"
	.string "para a proxima trilha.$"

EryonPico_Text_ElderBefore:
	.string "ANCIA: DRAKONIA guarda\n"
	.string "os cantos dos dragoes.\p"
	.string "As montanhas tremem\n"
	.string "quando o vento muda.$"

EryonPico_Text_ElderClue:
	.string "ANCIA: A ECLIPSE quer\n"
	.string "capturar o eco antigo.\p"
	.string "Avise os guardioes\n"
	.string "de DRAKONIA!$"

EryonPico_Text_Messenger:
	.string "VIAJANTE: Trouxeram\n"
	.string "caixas pelo desfiladeiro.\p"
	.string "A escolta partiu rumo\n"
	.string "ao santuario dos dragoes.$"

EryonPico_Text_GeologistBefore:
	.string "GEOLOGO: A rocha aqui\n"
	.string "e diferente da serra.\p"
	.string "Estou medindo sua\n"
	.string "ressonancia natural.$"

EryonPico_Text_GeologistClue:
	.string "GEOLOGO: O mesmo pulso\n"
	.string "de IGNIVAR passou aqui.\p"
	.string "O proximo ponto deve\n"
	.string "ser DRAKONIA.$"

EryonPico_Text_Notice:
	.string "VILA DO PICO:\n"
	.string "Descanse antes da subida.\p"
	.string "Relate qualquer som\n"
	.string "estranho aos vigias.$"

EryonPico_Text_Road:
	.string "LESTE: DRAKONIA.\n"
	.string "O caminho esta aberto!\p"
	.string "Descubra o segredo\n"
	.string "do santuario dos dragoes.$"

@ The mountain village responds to the Star Chart discovery.
@ These events provide clues without an HM gate or mandatory battle.
EryonPico_EventScript_RadioOperator::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED, EryonPico_EventScript_RadioReport
	goto_if_set FLAG_ERYON_DRAGON_TRAIL_MANIFEST_READ, EryonPico_EventScript_RadioManifest
	goto_if_set FLAG_ERYON_STAR_CHART_READ, EryonPico_EventScript_RadioAfterChart
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonPico_EventScript_RadioAfterSerra
	msgbox EryonPico_Text_RadioBefore, MSGBOX_DEFAULT
	release
	end

EryonPico_EventScript_RadioAfterSerra::
	msgbox EryonPico_Text_RadioAfterSerra, MSGBOX_DEFAULT
	release
	end

EryonPico_EventScript_RadioAfterChart::
	msgbox EryonPico_Text_RadioAfterChart, MSGBOX_DEFAULT
	release
	end

EryonPico_Text_RadioBefore:
	.string "OPERADOR: As radios\n"
	.string "captam um sinal novo.\p"
	.string "Ele vem das montanhas\n"
	.string "a leste da vila.$"

EryonPico_Text_RadioAfterSerra:
	.string "OPERADOR: A ECLIPSE\n"
	.string "esta usando cristais!\p"
	.string "Nosso sinal aponta\n"
	.string "para DRAKONIA.$"

EryonPico_Text_RadioAfterChart:
	.string "OPERADOR: A carta\n"
	.string "revelou uma rede!\p"
	.string "O ultimo transmissor\n"
	.string "fica perto da LIGA.\p"
	.string "A vila continua\n"
	.string "vigiando o sinal.$"

@ The radio station relays updates as the Eclipse investigation progresses.
EryonPico_EventScript_RadioManifest::
	msgbox EryonPico_Text_RadioManifest, MSGBOX_DEFAULT
	release
	end

EryonPico_EventScript_RadioReport::
	msgbox EryonPico_Text_RadioReport, MSGBOX_DEFAULT
	release
	end

EryonPico_Text_RadioManifest:
	.string "OPERADOR: O registro\n"
	.string "das cargas confirma\n"
	.string "o sinal da ECLIPSE!\p"
	.string "Vou avisar Drakonia.$"

EryonPico_Text_RadioReport:
	.string "OPERADOR: Recebemos\n"
	.string "noticias da LIGA!\p"
	.string "As provas da ECLIPSE\n"
	.string "ja foram entregues.\p"
	.string "A vila esta segura,\n"
	.string "mas seguimos atentos.$"
