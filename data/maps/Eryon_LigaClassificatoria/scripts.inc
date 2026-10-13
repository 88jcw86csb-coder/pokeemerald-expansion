Eryon_LigaClassificatoria_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EryonLigaQual_OnTransition
	.byte 0

@ A new visit starts an entirely new qualifying run unless already certified.
@ A normal trainer loss uses vanilla money loss and Pokemon Center whiteout.
@ Returning to this hall after a loss resets every battle and round flag.
EryonLigaQual_OnTransition:
	goto_if_set FLAG_ERYON_QUALIFIED, EryonLigaQual_OnTransitionDone
	clearflag FLAG_ERYON_QUALIFIER_ROUND_1
	clearflag FLAG_ERYON_QUALIFIER_ROUND_2
	clearflag FLAG_ERYON_QUALIFIER_ROUND_3
	clearflag FLAG_ERYON_QUALIFIER_ROUND_4
	clearflag FLAG_ERYON_QUALIFIER_ROUND_5
	clearflag FLAG_ERYON_QUALIFIER_ROUND_6
	clearflag FLAG_ERYON_QUALIFIER_ROUND_7
	clearflag FLAG_ERYON_QUALIFIER_ROUND_8
	cleartrainerflag TRAINER_ERYON_QUALIFIER_1
	cleartrainerflag TRAINER_ERYON_QUALIFIER_2
	cleartrainerflag TRAINER_ERYON_QUALIFIER_3
	cleartrainerflag TRAINER_ERYON_QUALIFIER_4
	cleartrainerflag TRAINER_ERYON_QUALIFIER_5
	cleartrainerflag TRAINER_ERYON_QUALIFIER_6
	cleartrainerflag TRAINER_ERYON_QUALIFIER_7
	cleartrainerflag TRAINER_ERYON_QUALIFIER_8
EryonLigaQual_OnTransitionDone:
	end

EryonLigaQual_EventScript_ExitMarshal::
	lock
	faceplayer
	msgbox EryonLigaQual_Text_ExitMarshal, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonLigaQual_EventScript_Stay
	closemessage
	warp MAP_ERYON_LIGA_RECEPCAO, 12, 12
	waitstate
	end

EryonLigaQual_EventScript_Stay::
	release
	end

EryonLigaQual_EventScript_Scoreboard::
	lock
	goto_if_set FLAG_ERYON_QUALIFIER_ROUND_8, EryonLigaQual_EventScript_Board8
	goto_if_set FLAG_ERYON_QUALIFIER_ROUND_7, EryonLigaQual_EventScript_Board7
	goto_if_set FLAG_ERYON_QUALIFIER_ROUND_6, EryonLigaQual_EventScript_Board6
	goto_if_set FLAG_ERYON_QUALIFIER_ROUND_5, EryonLigaQual_EventScript_Board5
	goto_if_set FLAG_ERYON_QUALIFIER_ROUND_4, EryonLigaQual_EventScript_Board4
	goto_if_set FLAG_ERYON_QUALIFIER_ROUND_3, EryonLigaQual_EventScript_Board3
	goto_if_set FLAG_ERYON_QUALIFIER_ROUND_2, EryonLigaQual_EventScript_Board2
	goto_if_set FLAG_ERYON_QUALIFIER_ROUND_1, EryonLigaQual_EventScript_Board1
	msgbox EryonLigaQual_Text_Board0, MSGBOX_DEFAULT
	release
	end

EryonLigaQual_EventScript_Board1::
	msgbox EryonLigaQual_Text_Board1, MSGBOX_DEFAULT
	release
	end
EryonLigaQual_EventScript_Board2::
	msgbox EryonLigaQual_Text_Board2, MSGBOX_DEFAULT
	release
	end
EryonLigaQual_EventScript_Board3::
	msgbox EryonLigaQual_Text_Board3, MSGBOX_DEFAULT
	release
	end
EryonLigaQual_EventScript_Board4::
	msgbox EryonLigaQual_Text_Board4, MSGBOX_DEFAULT
	release
	end
EryonLigaQual_EventScript_Board5::
	msgbox EryonLigaQual_Text_Board5, MSGBOX_DEFAULT
	release
	end
EryonLigaQual_EventScript_Board6::
	msgbox EryonLigaQual_Text_Board6, MSGBOX_DEFAULT
	release
	end
EryonLigaQual_EventScript_Board7::
	msgbox EryonLigaQual_Text_Board7, MSGBOX_DEFAULT
	release
	end
EryonLigaQual_EventScript_Board8::
	msgbox EryonLigaQual_Text_Board8, MSGBOX_DEFAULT
	release
	end
EryonLigaQual_EventScript_Fighter1::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_QUALIFIER_ROUND_1, EryonLigaQual_EventScript_Already
	trainerbattle_single TRAINER_ERYON_QUALIFIER_1, EryonLigaQual_Text_Intro1, EryonLigaQual_Text_Lose1, EryonLigaQual_EventScript_Win1, FALSE
	msgbox EryonLigaQual_Text_Already, MSGBOX_DEFAULT
	release
	end

EryonLigaQual_EventScript_Win1::
	setflag FLAG_ERYON_QUALIFIER_ROUND_1
	msgbox EryonLigaQual_Text_Pass1, MSGBOX_DEFAULT
	release
	end

EryonLigaQual_EventScript_Fighter2::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_QUALIFIER_ROUND_2, EryonLigaQual_EventScript_Already
	goto_if_unset FLAG_ERYON_QUALIFIER_ROUND_1, EryonLigaQual_EventScript_Locked
	trainerbattle_single TRAINER_ERYON_QUALIFIER_2, EryonLigaQual_Text_Intro2, EryonLigaQual_Text_Lose2, EryonLigaQual_EventScript_Win2, FALSE
	msgbox EryonLigaQual_Text_Already, MSGBOX_DEFAULT
	release
	end

EryonLigaQual_EventScript_Win2::
	setflag FLAG_ERYON_QUALIFIER_ROUND_2
	msgbox EryonLigaQual_Text_Pass2, MSGBOX_DEFAULT
	release
	end

EryonLigaQual_EventScript_Fighter3::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_QUALIFIER_ROUND_3, EryonLigaQual_EventScript_Already
	goto_if_unset FLAG_ERYON_QUALIFIER_ROUND_2, EryonLigaQual_EventScript_Locked
	trainerbattle_single TRAINER_ERYON_QUALIFIER_3, EryonLigaQual_Text_Intro3, EryonLigaQual_Text_Lose3, EryonLigaQual_EventScript_Win3, FALSE
	msgbox EryonLigaQual_Text_Already, MSGBOX_DEFAULT
	release
	end

EryonLigaQual_EventScript_Win3::
	setflag FLAG_ERYON_QUALIFIER_ROUND_3
	msgbox EryonLigaQual_Text_Pass3, MSGBOX_DEFAULT
	release
	end

EryonLigaQual_EventScript_Fighter4::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_QUALIFIER_ROUND_4, EryonLigaQual_EventScript_Already
	goto_if_unset FLAG_ERYON_QUALIFIER_ROUND_3, EryonLigaQual_EventScript_Locked
	trainerbattle_single TRAINER_ERYON_QUALIFIER_4, EryonLigaQual_Text_Intro4, EryonLigaQual_Text_Lose4, EryonLigaQual_EventScript_Win4, FALSE
	msgbox EryonLigaQual_Text_Already, MSGBOX_DEFAULT
	release
	end

EryonLigaQual_EventScript_Win4::
	setflag FLAG_ERYON_QUALIFIER_ROUND_4
	msgbox EryonLigaQual_Text_Pass4, MSGBOX_DEFAULT
	release
	end

EryonLigaQual_EventScript_Fighter5::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_QUALIFIER_ROUND_5, EryonLigaQual_EventScript_Already
	goto_if_unset FLAG_ERYON_QUALIFIER_ROUND_4, EryonLigaQual_EventScript_Locked
	trainerbattle_single TRAINER_ERYON_QUALIFIER_5, EryonLigaQual_Text_Intro5, EryonLigaQual_Text_Lose5, EryonLigaQual_EventScript_Win5, FALSE
	msgbox EryonLigaQual_Text_Already, MSGBOX_DEFAULT
	release
	end

EryonLigaQual_EventScript_Win5::
	setflag FLAG_ERYON_QUALIFIER_ROUND_5
	msgbox EryonLigaQual_Text_Pass5, MSGBOX_DEFAULT
	release
	end

EryonLigaQual_EventScript_Fighter6::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_QUALIFIER_ROUND_6, EryonLigaQual_EventScript_Already
	goto_if_unset FLAG_ERYON_QUALIFIER_ROUND_5, EryonLigaQual_EventScript_Locked
	trainerbattle_single TRAINER_ERYON_QUALIFIER_6, EryonLigaQual_Text_Intro6, EryonLigaQual_Text_Lose6, EryonLigaQual_EventScript_Win6, FALSE
	msgbox EryonLigaQual_Text_Already, MSGBOX_DEFAULT
	release
	end

EryonLigaQual_EventScript_Win6::
	setflag FLAG_ERYON_QUALIFIER_ROUND_6
	msgbox EryonLigaQual_Text_Pass6, MSGBOX_DEFAULT
	release
	end

EryonLigaQual_EventScript_Fighter7::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_QUALIFIER_ROUND_7, EryonLigaQual_EventScript_Already
	goto_if_unset FLAG_ERYON_QUALIFIER_ROUND_6, EryonLigaQual_EventScript_Locked
	trainerbattle_single TRAINER_ERYON_QUALIFIER_7, EryonLigaQual_Text_Intro7, EryonLigaQual_Text_Lose7, EryonLigaQual_EventScript_Win7, FALSE
	msgbox EryonLigaQual_Text_Already, MSGBOX_DEFAULT
	release
	end

EryonLigaQual_EventScript_Win7::
	setflag FLAG_ERYON_QUALIFIER_ROUND_7
	msgbox EryonLigaQual_Text_Pass7, MSGBOX_DEFAULT
	release
	end

EryonLigaQual_EventScript_Fighter8::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_QUALIFIER_ROUND_8, EryonLigaQual_EventScript_Already
	goto_if_unset FLAG_ERYON_QUALIFIER_ROUND_7, EryonLigaQual_EventScript_Locked
	trainerbattle_single TRAINER_ERYON_QUALIFIER_8, EryonLigaQual_Text_Intro8, EryonLigaQual_Text_Lose8, EryonLigaQual_EventScript_Win8, FALSE
	msgbox EryonLigaQual_Text_Already, MSGBOX_DEFAULT
	release
	end

EryonLigaQual_EventScript_Win8::
	setflag FLAG_ERYON_QUALIFIER_ROUND_8
	setflag FLAG_ERYON_QUALIFIED
	msgbox EryonLigaQual_Text_Champion, MSGBOX_DEFAULT
	warp MAP_ERYON_LIGA_RECUPERACAO, 12, 14
	waitstate
	end

EryonLigaQual_EventScript_Already::
	msgbox EryonLigaQual_Text_Already, MSGBOX_DEFAULT
	release
	end

EryonLigaQual_EventScript_Locked::
	msgbox EryonLigaQual_Text_Locked, MSGBOX_DEFAULT
	release
	end

EryonLigaQual_Text_ExitMarshal:
	.string "OFICIAL: Pode voltar\n"
	.string "a recepcao pelo sul.\p"
	.string "Se sair agora, uma\n"
	.string "nova entrada reinicia\n"
	.string "as fases pendentes.$"

EryonLigaQual_Text_Already:
	.string "O combate desta fase\n"
	.string "ja foi vencido.\p"
	.string "Enfrente o proximo\n"
	.string "competidor.$"

EryonLigaQual_Text_Locked:
	.string "OFICIAL: Siga a ordem!\p"
	.string "Primeiro venca todas\n"
	.string "as fases anteriores.$"

EryonLigaQual_Text_Champion:
	.string "CLASSIFICACAO COMPLETA!\p"
	.string "Oito vitorias seguidas!\n"
	.string "Voce esta aprovado.\p"
	.string "Siga para a sala de\n"
	.string "recuperacao da LIGA.$"

EryonLigaQual_Text_Board0:
	.string "CLASSIFICATORIA:\n"
	.string "0 de 8 vitorias.\p"
	.string "Comece pelo IVO.$"

EryonLigaQual_Text_Board1:
	.string "CLASSIFICATORIA:\n"
	.string "1 de 8 vitorias.\p"
	.string "Proximo: MARTA.$"

EryonLigaQual_Text_Board2:
	.string "CLASSIFICATORIA:\n"
	.string "2 de 8 vitorias.\p"
	.string "Proximo: PEDRO.$"

EryonLigaQual_Text_Board3:
	.string "CLASSIFICATORIA:\n"
	.string "3 de 8 vitorias.\p"
	.string "Proximo: NOAH.$"

EryonLigaQual_Text_Board4:
	.string "CLASSIFICATORIA:\n"
	.string "4 de 8 vitorias.\p"
	.string "Proximo: RAVI.$"

EryonLigaQual_Text_Board5:
	.string "CLASSIFICATORIA:\n"
	.string "5 de 8 vitorias.\p"
	.string "Proximo: LUNA.$"

EryonLigaQual_Text_Board6:
	.string "CLASSIFICATORIA:\n"
	.string "6 de 8 vitorias.\p"
	.string "Proximo: DANTE.$"

EryonLigaQual_Text_Board7:
	.string "CLASSIFICATORIA:\n"
	.string "7 de 8 vitorias.\p"
	.string "Proximo: ELISA.$"

EryonLigaQual_Text_Board8:
	.string "CLASSIFICATORIA:\n"
	.string "8 de 8 vitorias.\p"
	.string "Aprovado para a ELITE 4.$"

EryonLigaQual_Text_Intro1:
	.string "FASE 1: IVO!\p"
	.string "Mostre sua forca\n"
	.string "nesta classificatoria.$"

EryonLigaQual_Text_Lose1:
	.string "IVO: Boa batalha!\n"
	.string "Voce passou de fase.$"

EryonLigaQual_Text_Pass1:
	.string "FASE 1 CONCLUIDA!\p"
	.string "A proxima fase foi\n"
	.string "liberada.$"

EryonLigaQual_Text_Intro2:
	.string "FASE 2: MARTA!\p"
	.string "Mostre sua forca\n"
	.string "nesta classificatoria.$"

EryonLigaQual_Text_Lose2:
	.string "MARTA: Boa batalha!\n"
	.string "Voce passou de fase.$"

EryonLigaQual_Text_Pass2:
	.string "FASE 2 CONCLUIDA!\p"
	.string "A proxima fase foi\n"
	.string "liberada.$"

EryonLigaQual_Text_Intro3:
	.string "FASE 3: PEDRO!\p"
	.string "Mostre sua forca\n"
	.string "nesta classificatoria.$"

EryonLigaQual_Text_Lose3:
	.string "PEDRO: Boa batalha!\n"
	.string "Voce passou de fase.$"

EryonLigaQual_Text_Pass3:
	.string "FASE 3 CONCLUIDA!\p"
	.string "A proxima fase foi\n"
	.string "liberada.$"

EryonLigaQual_Text_Intro4:
	.string "FASE 4: NOAH!\p"
	.string "Mostre sua forca\n"
	.string "nesta classificatoria.$"

EryonLigaQual_Text_Lose4:
	.string "NOAH: Boa batalha!\n"
	.string "Voce passou de fase.$"

EryonLigaQual_Text_Pass4:
	.string "FASE 4 CONCLUIDA!\p"
	.string "A proxima fase foi\n"
	.string "liberada.$"

EryonLigaQual_Text_Intro5:
	.string "FASE 5: RAVI!\p"
	.string "Mostre sua forca\n"
	.string "nesta classificatoria.$"

EryonLigaQual_Text_Lose5:
	.string "RAVI: Boa batalha!\n"
	.string "Voce passou de fase.$"

EryonLigaQual_Text_Pass5:
	.string "FASE 5 CONCLUIDA!\p"
	.string "A proxima fase foi\n"
	.string "liberada.$"

EryonLigaQual_Text_Intro6:
	.string "FASE 6: LUNA!\p"
	.string "Mostre sua forca\n"
	.string "nesta classificatoria.$"

EryonLigaQual_Text_Lose6:
	.string "LUNA: Boa batalha!\n"
	.string "Voce passou de fase.$"

EryonLigaQual_Text_Pass6:
	.string "FASE 6 CONCLUIDA!\p"
	.string "A proxima fase foi\n"
	.string "liberada.$"

EryonLigaQual_Text_Intro7:
	.string "FASE 7: DANTE!\p"
	.string "Mostre sua forca\n"
	.string "nesta classificatoria.$"

EryonLigaQual_Text_Lose7:
	.string "DANTE: Boa batalha!\n"
	.string "Voce passou de fase.$"

EryonLigaQual_Text_Pass7:
	.string "FASE 7 CONCLUIDA!\p"
	.string "A proxima fase foi\n"
	.string "liberada.$"

EryonLigaQual_Text_Intro8:
	.string "FASE 8: ELISA!\p"
	.string "Mostre sua forca\n"
	.string "nesta classificatoria.$"

EryonLigaQual_Text_Lose8:
	.string "ELISA: Boa batalha!\n"
	.string "Voce passou de fase.$"

