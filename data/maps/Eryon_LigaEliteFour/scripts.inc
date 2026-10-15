Eryon_LigaEliteFour_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EryonLigaElite_OnTransition
	.byte 0

@ Re-entering the gallery restarts the Elite Four, never the eight qualifiers.
@ Whiteout handles the money penalty; qualification remains permanent.
EryonLigaElite_OnTransition:
	goto_if_set FLAG_ERYON_CHAMPION_CROWNED, EryonLigaElite_OnTransitionDone
	@ Both the scripted progress flags AND the mapped trainer flags must reset.
	@ Otherwise leaving the gallery after one victory permanently skips Aria,
	@ and the next Elite Four attempt is softlocked at Bastian.
	@ Do not reset FLAG_ERYON_QUALIFIED or the eight qualifying rounds.
	clearflag FLAG_ERYON_ELITE_TRAINER_1_DEFEATED
	clearflag FLAG_ERYON_ELITE_TRAINER_2_DEFEATED
	clearflag FLAG_ERYON_ELITE_TRAINER_3_DEFEATED
	clearflag FLAG_ERYON_ELITE_TRAINER_4_DEFEATED
	clearflag FLAG_ERYON_CHAMPION_TRAINER_DEFEATED
	cleartrainerflag TRAINER_ERYON_ELITE_1
	cleartrainerflag TRAINER_ERYON_ELITE_2
	cleartrainerflag TRAINER_ERYON_ELITE_3
	cleartrainerflag TRAINER_ERYON_ELITE_4
	cleartrainerflag TRAINER_ERYON_CHAMPION
EryonLigaElite_OnTransitionDone:
	end

@ Aria - sequence position 1.
EryonLigaElite_EventScript_Aria::
	lock
	faceplayer
	goto_if_unset FLAG_ERYON_QUALIFIED, EryonLigaElite_EventScript_NotQualified
	goto_if_set FLAG_ERYON_ELITE_TRAINER_1_DEFEATED, EryonLigaElite_EventScript_Already
	trainerbattle_single TRAINER_ERYON_ELITE_1, EryonLigaElite_Text_Intro1, EryonLigaElite_Text_Loss1, EryonLigaElite_EventScript_Win1, FALSE
	msgbox EryonLigaElite_Text_Already, MSGBOX_DEFAULT
	release
	end

EryonLigaElite_EventScript_Win1::
	setflag FLAG_ERYON_ELITE_TRAINER_1_DEFEATED
	msgbox EryonLigaElite_Text_Win1, MSGBOX_DEFAULT
	release
	end

@ Bastian - sequence position 2.
EryonLigaElite_EventScript_Bastian::
	lock
	faceplayer
	goto_if_unset FLAG_ERYON_QUALIFIED, EryonLigaElite_EventScript_NotQualified
	goto_if_set FLAG_ERYON_ELITE_TRAINER_2_DEFEATED, EryonLigaElite_EventScript_Already
	goto_if_unset FLAG_ERYON_ELITE_TRAINER_1_DEFEATED, EryonLigaElite_EventScript_Locked
	trainerbattle_single TRAINER_ERYON_ELITE_2, EryonLigaElite_Text_Intro2, EryonLigaElite_Text_Loss2, EryonLigaElite_EventScript_Win2, FALSE
	msgbox EryonLigaElite_Text_Already, MSGBOX_DEFAULT
	release
	end

EryonLigaElite_EventScript_Win2::
	setflag FLAG_ERYON_ELITE_TRAINER_2_DEFEATED
	msgbox EryonLigaElite_Text_Win2, MSGBOX_DEFAULT
	release
	end

@ Selene - sequence position 3.
EryonLigaElite_EventScript_Selene::
	lock
	faceplayer
	goto_if_unset FLAG_ERYON_QUALIFIED, EryonLigaElite_EventScript_NotQualified
	goto_if_set FLAG_ERYON_ELITE_TRAINER_3_DEFEATED, EryonLigaElite_EventScript_Already
	goto_if_unset FLAG_ERYON_ELITE_TRAINER_2_DEFEATED, EryonLigaElite_EventScript_Locked
	trainerbattle_single TRAINER_ERYON_ELITE_3, EryonLigaElite_Text_Intro3, EryonLigaElite_Text_Loss3, EryonLigaElite_EventScript_Win3, FALSE
	msgbox EryonLigaElite_Text_Already, MSGBOX_DEFAULT
	release
	end

EryonLigaElite_EventScript_Win3::
	setflag FLAG_ERYON_ELITE_TRAINER_3_DEFEATED
	msgbox EryonLigaElite_Text_Win3, MSGBOX_DEFAULT
	release
	end

@ Darius - sequence position 4.
EryonLigaElite_EventScript_Darius::
	lock
	faceplayer
	goto_if_unset FLAG_ERYON_QUALIFIED, EryonLigaElite_EventScript_NotQualified
	goto_if_set FLAG_ERYON_ELITE_TRAINER_4_DEFEATED, EryonLigaElite_EventScript_Already
	goto_if_unset FLAG_ERYON_ELITE_TRAINER_3_DEFEATED, EryonLigaElite_EventScript_Locked
	trainerbattle_single TRAINER_ERYON_ELITE_4, EryonLigaElite_Text_Intro4, EryonLigaElite_Text_Loss4, EryonLigaElite_EventScript_Win4, FALSE
	msgbox EryonLigaElite_Text_Already, MSGBOX_DEFAULT
	release
	end

EryonLigaElite_EventScript_Win4::
	setflag FLAG_ERYON_ELITE_TRAINER_4_DEFEATED
	msgbox EryonLigaElite_Text_Win4, MSGBOX_DEFAULT
	release
	end

@ Champion - sequence position 5.
EryonLigaElite_EventScript_Champion::
	lock
	faceplayer
	goto_if_unset FLAG_ERYON_QUALIFIED, EryonLigaElite_EventScript_NotQualified
	goto_if_set FLAG_ERYON_CHAMPION_CROWNED, EryonLigaElite_EventScript_ChampionAfter
	goto_if_set FLAG_ERYON_CHAMPION_TRAINER_DEFEATED, EryonLigaElite_EventScript_Already
	goto_if_unset FLAG_ERYON_ELITE_TRAINER_4_DEFEATED, EryonLigaElite_EventScript_Locked
	trainerbattle_single TRAINER_ERYON_CHAMPION, EryonLigaElite_Text_Intro5, EryonLigaElite_Text_Loss5, EryonLigaElite_EventScript_Win5, FALSE
	msgbox EryonLigaElite_Text_Already, MSGBOX_DEFAULT
	release
	end

EryonLigaElite_EventScript_Win5::
	setflag FLAG_ERYON_CHAMPION_TRAINER_DEFEATED
	setflag FLAG_ERYON_CHAMPION_CROWNED
	goto_if_set FLAG_ERYON_ECLIPSE_NETWORK_SHUT_DOWN, EryonLigaElite_EventScript_Win5Peace
	msgbox EryonLigaElite_Text_Win5, MSGBOX_DEFAULT
	release
	end

@ League victory can come before or after the optional Eclipse finale.
EryonLigaElite_EventScript_Win5Peace::
	msgbox EryonLigaElite_Text_Win5Peace, MSGBOX_DEFAULT
	release
	end

EryonLigaElite_Text_Win5Peace:
	.string "AURELIO: Voce venceu\n"
	.string "a ELITE e a ECLIPSE!\p"
	.string "Ao salvar os cristais,\n"
	.string "protegeu nossa regiao.\p"
	.string "Agora, novo CAMPEAO,\n"
	.string "ERYON celebra seu nome!$"

EryonLigaElite_EventScript_Exit::
	lock
	msgbox EryonLigaElite_Text_Exit, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonLigaElite_EventScript_Stay
	closemessage
	warp MAP_ERYON_LIGA_RECUPERACAO, 12, 14
	waitstate
	end

EryonLigaElite_EventScript_Stay::
	closemessage
	release
	end

EryonLigaElite_EventScript_Rules::
	lock
	goto_if_set FLAG_ERYON_CHAMPION_CROWNED, EryonLigaElite_EventScript_RulesChampion
	msgbox EryonLigaElite_Text_Rules, MSGBOX_DEFAULT
	release
	end

EryonLigaElite_EventScript_Trophy::
	lock
	goto_if_set FLAG_ERYON_CHAMPION_CROWNED, EryonLigaElite_EventScript_TrophyChampion
	msgbox EryonLigaElite_Text_TrophyBefore, MSGBOX_DEFAULT
	release
	end

EryonLigaElite_EventScript_RulesChampion::
	msgbox EryonLigaElite_Text_RulesChampion, MSGBOX_DEFAULT
	release
	end

EryonLigaElite_EventScript_TrophyChampion::
	goto_if_set FLAG_ERYON_PEACE_CEREMONY_RECORDED, EryonLigaElite_EventScript_TrophyPeace
	msgbox EryonLigaElite_Text_TrophyChampion, MSGBOX_DEFAULT
	release
	end

EryonLigaElite_EventScript_ChampionAfter::
	msgbox EryonLigaElite_Text_ChampionAfter, MSGBOX_DEFAULT
	release
	end

EryonLigaElite_EventScript_Already::
	msgbox EryonLigaElite_Text_Already, MSGBOX_DEFAULT
	release
	end

EryonLigaElite_EventScript_Locked::
	msgbox EryonLigaElite_Text_Locked, MSGBOX_DEFAULT
	release
	end

EryonLigaElite_EventScript_NotQualified::
	msgbox EryonLigaElite_Text_NotQualified, MSGBOX_DEFAULT
	release
	end

EryonLigaElite_Text_Rules:
	.string "SALA DA ELITE FOUR:\n"
	.string "Venca os quatro mestres\n"
	.string "na ordem da galeria.\p"
	.string "So entao enfrente\n"
	.string "o CAMPEAO de ERYON.\p"
	.string "Sair reinicia a serie,\n"
	.string "mas preserva as oito\n"
	.string "vitorias classificatorias.$"

EryonLigaElite_Text_Exit:
	.string "Voltar para a sala\n"
	.string "de recuperacao?\p"
	.string "A ELITE 4 recomecara\n"
	.string "se voce retornar.$"

EryonLigaElite_Text_NotQualified:
	.string "Seu registro ainda\n"
	.string "nao foi confirmado!\p"
	.string "Venca as oito batalhas\n"
	.string "da CLASSIFICATORIA.$"

EryonLigaElite_Text_Locked:
	.string "MESTRE: Primeiro,\n"
	.string "venca o membro anterior\n"
	.string "da ELITE FOUR.$"

EryonLigaElite_Text_Already:
	.string "MESTRE: Duelo concluido!\p"
	.string "Prossiga pela galeria\n"
	.string "ate o proximo desafio.$"

EryonLigaElite_Text_TrophyBefore:
	.string "MONUMENTO DE ERYON:\p"
	.string "Os maiores treinadores\n"
	.string "alcancaram este salao.$"

EryonLigaElite_Text_TrophyChampion:
	.string "CAMPEAO DE ERYON!\p"
	.string "Sua conquista foi\n"
	.string "registrada nesta Liga.$"

EryonLigaElite_Text_RulesChampion:
	.string "O novo CAMPEAO\n"
	.string "concluiu o torneio!\p"
	.string "A LIGA DE ERYON esta\n"
	.string "aberta a novos duelos.$"

EryonLigaElite_Text_ChampionAfter:
	.string "AURELIO: Seu nome\n"
	.string "pertence a historia\n"
	.string "da regiao ERYON!\p"
	.string "Proteja a paz que\n"
	.string "conquistou na jornada.$"

EryonLigaElite_Text_Intro1:
	.string "ARIA: O gelo exige\n"
	.string "coragem e precisao!$"

EryonLigaElite_Text_Loss1:
	.string "ARIA: A tempestade\n"
	.string "encontrou seu mestre!$"

EryonLigaElite_Text_Win1:
	.string "ARIA: Foi uma bela luta!\n"
	.string "Siga para BASTIAN.$"

EryonLigaElite_Text_Intro2:
	.string "BASTIAN: As montanhas\n"
	.string "testarao sua vontade!$"

EryonLigaElite_Text_Loss2:
	.string "BASTIAN: Sua forca\n"
	.string "supera ate as rochas!$"

EryonLigaElite_Text_Win2:
	.string "BASTIAN: Avance!\n"
	.string "SELENE esta esperando.$"

EryonLigaElite_Text_Intro3:
	.string "SELENE: Ate nas sombras\n"
	.string "brilha um grande heroi.$"

EryonLigaElite_Text_Loss3:
	.string "SELENE: Seu brilho\n"
	.string "venceu a escuridao!$"

EryonLigaElite_Text_Win3:
	.string "SELENE: DARIUS guarda\n"
	.string "o ultimo duelo.$"

EryonLigaElite_Text_Intro4:
	.string "DARIUS: Dragoes protegem\n"
	.string "o destino de ERYON!$"

EryonLigaElite_Text_Loss4:
	.string "DARIUS: Seu espirito\n"
	.string "e digno dos dragoes!$"

EryonLigaElite_Text_Win4:
	.string "DARIUS: Venceu a ELITE!\n"
	.string "O CAMPEAO espera!$"

EryonLigaElite_Text_Intro5:
	.string "AURELIO: Voce venceu\n"
	.string "oito classificatorias\n"
	.string "e quatro mestres!\n"
	.string "Agora, nossa batalha!$"

EryonLigaElite_Text_Loss5:
	.string "AURELIO: Um novo\n"
	.string "CAMPEAO nasceu!$"

EryonLigaElite_Text_Win5:
	.string "AURELIO: Parabens!\n"
	.string "Voce e o novo CAMPEAO\n"
	.string "da regiao ERYON!\n"
	.string "A LIGA celebra!$"



@ After the public ceremony, the League's trophy carries the epilogue.
EryonLigaElite_EventScript_TrophyPeace::
	msgbox EryonLigaElite_Text_TrophyPeace, MSGBOX_DEFAULT
	release
	end

EryonLigaElite_Text_TrophyPeace:
	.string "HALL DA FAMA DE ERYON:\p"
	.string "O CAMPEAO da paz\n"
	.string "concluiu sua jornada!\p"
	.string "Oito insignias, oito\n"
	.string "duelos e a ELITE FOUR.\p"
	.string "A historia de RIOLU\n"
	.string "agora pertence a ERYON.$"
