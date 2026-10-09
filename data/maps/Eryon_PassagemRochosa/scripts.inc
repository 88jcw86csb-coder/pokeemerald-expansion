Eryon_PassagemRochosa_MapScripts::
	.byte 0

@ Eryon: narrow trail after the crystal highlands.
EryonPassagem_EventScript_Guard::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonPassagem_EventScript_GuardClue
	msgbox EryonPassagem_Text_GuardBefore, MSGBOX_DEFAULT
	release
	end

EryonPassagem_EventScript_GuardClue::
	msgbox EryonPassagem_Text_GuardClue, MSGBOX_DEFAULT
	release
	end

EryonPassagem_EventScript_Traveler::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonPassagem_EventScript_TravelerAfterClue
	msgbox EryonPassagem_Text_Traveler, MSGBOX_DEFAULT
	release
	end

EryonPassagem_EventScript_TravelerAfterClue::
	msgbox EryonPassagem_Text_TravelerAfterClue, MSGBOX_DEFAULT
	release
	end

@ The cart tracks tell a different story once the Eclipse camp has been examined.
EryonPassagem_EventScript_CrystalMark::
	lock
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonPassagem_EventScript_CrystalMarkClue
	goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonPassagem_EventScript_CrystalMarkBadge
	msgbox EryonPassagem_Text_CrystalMarkBefore, MSGBOX_DEFAULT
	release
	end

EryonPassagem_EventScript_CrystalMarkBadge::
	msgbox EryonPassagem_Text_CrystalMarkBadge, MSGBOX_DEFAULT
	release
	end

EryonPassagem_EventScript_CrystalMarkClue::
	msgbox EryonPassagem_Text_CrystalMarkClue, MSGBOX_DEFAULT
	release
	end

EryonPassagem_Text_GuardBefore:
	.string "GUARDA: Os trilhos de pedra\n"
	.string "levam a um velho desfiladeiro.\p"
	.string "Cuidado com o terreno.$"

EryonPassagem_Text_GuardClue:
	.string "GUARDA: Voce viu o simbolo\n"
	.string "do eclipse na serra?\p"
	.string "Carrocas seguiram por aqui\n"
	.string "antes do amanhecer.$"

EryonPassagem_Text_Traveler:
	.string "VIAJANTE: As montanhas\n"
	.string "escondem caminhos antigos.\p"
	.string "Ainda falta muito ate a\n"
	.string "proxima cidade.$"

EryonPassagem_Text_TravelerAfterClue:
	.string "VIAJANTE: Voce encontrou\n"
	.string "caixas marcadas na serra?\p"
	.string "Ouvi carrocas seguindo\n"
	.string "para alem do desfiladeiro.\p"
	.string "A estrada adiante e longa.\n"
	.string "Nao perca as pistas.$"

EryonPassagem_Text_CrystalMarkBefore:
	.string "Ha sulcos fundos na pedra.\p"
	.string "Talvez sejam marcas de rodas.$"

EryonPassagem_Text_CrystalMarkBadge:
	.string "Os sulcos sao recentes.\p"
	.string "Entre as marcas de rodas ha\n"
	.string "um brilho parecido com o po\n"
	.string "visto na Rota 03.\p"
	.string "Talvez a Serra dos Cristais\n"
	.string "guarde mais respostas.$"

EryonPassagem_Text_CrystalMarkClue:
	.string "Os sulcos combinam com as\n"
	.string "rodas vistas na serra.\p"
	.string "A carga seguiu para leste.$"


@ Optional rocky passage trainer challenges.
EryonPassagem_EventScript_HikerBattle::
	lock
	faceplayer
	trainerbattle_single TRAINER_ERYON_PASSAGEM_HIKER, EryonPassagem_Text_HikerChallenge, EryonPassagem_Text_HikerDefeat, EryonPassagem_EventScript_HikerVictory, FALSE
	msgbox EryonPassagem_Text_HikerAfter, MSGBOX_DEFAULT
	release
	end

EryonPassagem_EventScript_HikerVictory::
	msgbox EryonPassagem_Text_HikerAfter, MSGBOX_DEFAULT
	release
	end

EryonPassagem_EventScript_EclipseBattle::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonPassagem_EventScript_EclipseBattleAfterClue
	trainerbattle_single TRAINER_ERYON_PASSAGEM_ECLIPSE, EryonPassagem_Text_EclipseChallenge, EryonPassagem_Text_EclipseDefeat, EryonPassagem_EventScript_EclipseVictory, FALSE
	msgbox EryonPassagem_Text_EclipseAfter, MSGBOX_DEFAULT
	release
	end

EryonPassagem_EventScript_EclipseBattleAfterClue::
	trainerbattle_single TRAINER_ERYON_PASSAGEM_ECLIPSE, EryonPassagem_Text_EclipseClueChallenge, EryonPassagem_Text_EclipseDefeat, EryonPassagem_EventScript_EclipseVictory, FALSE
	msgbox EryonPassagem_Text_EclipseAfterClue, MSGBOX_DEFAULT
	release
	end

EryonPassagem_EventScript_EclipseVictory::
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonPassagem_EventScript_EclipseVictoryAfterClue
	msgbox EryonPassagem_Text_EclipseAfter, MSGBOX_DEFAULT
	release
	end

EryonPassagem_EventScript_EclipseVictoryAfterClue::
	msgbox EryonPassagem_Text_EclipseAfterClue, MSGBOX_DEFAULT
	release
	end

@ Inspectable caravan ledger: gives the player a concrete destination clue.
EryonPassagem_EventScript_CaravanLedger::
	lock
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonPassagem_EventScript_CaravanLedgerClue
	msgbox EryonPassagem_Text_CaravanLedgerBefore, MSGBOX_DEFAULT
	release
	end

EryonPassagem_EventScript_CaravanLedgerClue::
	msgbox EryonPassagem_Text_CaravanLedgerClue, MSGBOX_DEFAULT
	release
	end

EryonPassagem_Text_CaravanLedgerBefore:
	.string "Um papel rasgado preso\n"
	.string "entre as pedras.\p"
	.string "Ha horarios de passagem,\n"
	.string "mas o destino foi apagado.$"

EryonPassagem_Text_CaravanLedgerClue:
	.string "O registro fala de caixas\n"
	.string "vindas da Serra dos Cristais.\p"
	.string "Destino: estrada oriental.\n"
	.string "Entrega antes do amanhecer.\p"
	.string "O selo tem um eclipse.$"

EryonPassagem_EventScript_Medic::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonPassagem_EventScript_MedicClue
	msgbox EryonPassagem_Text_MedicOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonPassagem_EventScript_MedicDecline
	special HealPlayerParty
	msgbox EryonPassagem_Text_MedicHealed, MSGBOX_DEFAULT
	release
	end

EryonPassagem_EventScript_MedicClue::
	msgbox EryonPassagem_Text_MedicClueOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonPassagem_EventScript_MedicDecline
	special HealPlayerParty
	msgbox EryonPassagem_Text_MedicHealed, MSGBOX_DEFAULT
	release
	end

EryonPassagem_EventScript_MedicDecline::
	msgbox EryonPassagem_Text_MedicDecline, MSGBOX_DEFAULT
	release
	end

EryonPassagem_Text_HikerChallenge:
	.string "BRUNO: Vamos medir nossas\n"
	.string "forcas nesta subida!$"

EryonPassagem_Text_HikerDefeat:
	.string "BRUNO: Voce venceu!$"

EryonPassagem_Text_HikerAfter:
	.string "BRUNO: A trilha ainda\n"
	.string "guarda muitos desafios.$"

EryonPassagem_Text_EclipseChallenge:
	.string "VIGIA: Ninguem pode seguir\n"
	.string "as carrocas do Eclipse!$"

EryonPassagem_Text_EclipseDefeat:
	.string "VIGIA: Isso nao acabou!$"

EryonPassagem_Text_EclipseAfter:
	.string "VIGIA: Nosso lider ja\n"
	.string "levou os cristais daqui.$"

EryonPassagem_Text_EclipseClueChallenge:
	.string "VIGIA: Voce achou as caixas\n"
	.string "na Serra dos Cristais?!\p"
	.string "Nao pode seguir o comboio!$"

EryonPassagem_Text_EclipseAfterClue:
	.string "VIGIA: Os cristais ja foram\n"
	.string "enviados para mais longe.\p"
	.string "Nem eu sei o destino final.\n"
	.string "A ordem veio de cima.$"

EryonPassagem_Text_MedicOffer:
	.string "SOCORRISTA: Quer recuperar\n"
	.string "sua equipe Pokemon?$"

EryonPassagem_Text_MedicClueOffer:
	.string "SOCORRISTA: Vi carrocas\n"
	.string "partirem antes do sol nascer.\p"
	.string "Sua equipe precisa de\n"
	.string "cuidados antes de seguir?$"

EryonPassagem_Text_MedicHealed:
	.string "Pronto! Boa sorte na trilha.$"

EryonPassagem_Text_MedicDecline:
	.string "Estarei aqui se precisar.$"

@ A second optional observation connects the rocky passage to the stolen crystals.
EryonPassagem_EventScript_BrokenCrate::
	lock
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonPassagem_EventScript_BrokenCrateClue
	msgbox EryonPassagem_Text_BrokenCrateBefore, MSGBOX_DEFAULT
	release
	end

EryonPassagem_EventScript_BrokenCrateClue::
	msgbox EryonPassagem_Text_BrokenCrateClue, MSGBOX_DEFAULT
	release
	end

EryonPassagem_Text_BrokenCrateBefore:
	.string "Madeira quebrada e cordas\n"
	.string "estao espalhadas na trilha.\p"
	.string "Parece uma caixa de carga.$"

EryonPassagem_Text_BrokenCrateClue:
	.string "A caixa tem o mesmo simbolo\n"
	.string "visto no acampamento.\p"
	.string "Ha poeira de cristal na\n"
	.string "madeira. O rastro segue.$"

@ The road survey adds world-building without advancing the main quest prematurely.
EryonPassagem_EventScript_RoadSurvey::
	lock
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonPassagem_EventScript_RoadSurveyClue
	msgbox EryonPassagem_Text_RoadSurveyBefore, MSGBOX_DEFAULT
	release
	end

EryonPassagem_EventScript_RoadSurveyClue::
	msgbox EryonPassagem_Text_RoadSurveyClue, MSGBOX_DEFAULT
	release
	end

EryonPassagem_Text_RoadSurveyBefore:
	.string "Uma placa de pesquisa\n"
	.string "marca a antiga estrada.\p"
	.string "O desfiladeiro e longo.\n"
	.string "Leve suprimentos.$"

EryonPassagem_Text_RoadSurveyClue:
	.string "A placa registra carrocas\n"
	.string "que cruzaram a serra.\p"
	.string "Algumas cargas passaram\n"
	.string "fora do horario normal.\p"
	.string "A trilha oriental continua.$"
