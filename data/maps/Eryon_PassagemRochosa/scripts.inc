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
	msgbox EryonPassagem_Text_Traveler, MSGBOX_DEFAULT
	release
	end

EryonPassagem_EventScript_CrystalMark::
	lock
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonPassagem_EventScript_CrystalMarkClue
	msgbox EryonPassagem_Text_CrystalMarkBefore, MSGBOX_DEFAULT
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

EryonPassagem_Text_CrystalMarkBefore:
	.string "Ha sulcos fundos na pedra.\p"
	.string "Talvez sejam marcas de rodas.$"

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
	trainerbattle_single TRAINER_ERYON_PASSAGEM_ECLIPSE, EryonPassagem_Text_EclipseChallenge, EryonPassagem_Text_EclipseDefeat, EryonPassagem_EventScript_EclipseVictory, FALSE
	msgbox EryonPassagem_Text_EclipseAfter, MSGBOX_DEFAULT
	release
	end

EryonPassagem_EventScript_EclipseVictory::
	msgbox EryonPassagem_Text_EclipseAfter, MSGBOX_DEFAULT
	release
	end

EryonPassagem_EventScript_Medic::
	lock
	faceplayer
	msgbox EryonPassagem_Text_MedicOffer, MSGBOX_YESNO
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

EryonPassagem_Text_MedicOffer:
	.string "SOCORRISTA: Quer recuperar\n"
	.string "sua equipe Pokemon?$"

EryonPassagem_Text_MedicHealed:
	.string "Pronto! Boa sorte na trilha.$"

EryonPassagem_Text_MedicDecline:
	.string "Estarei aqui se precisar.$"
