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
