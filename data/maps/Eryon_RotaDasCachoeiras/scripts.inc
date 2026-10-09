Eryon_RotaDasCachoeiras_MapScripts::
	.byte 0

@ The waterway carries the trail of Eclipse cargo beyond Umbra.
EryonCachoeiras_EventScript_Ranger::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonCachoeiras_EventScript_RangerClue
	msgbox EryonCachoeiras_Text_RangerBefore, MSGBOX_DEFAULT
	release
	end

EryonCachoeiras_EventScript_RangerClue::
	msgbox EryonCachoeiras_Text_RangerClue, MSGBOX_DEFAULT
	release
	end

EryonCachoeiras_EventScript_EclipseScout::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonCachoeiras_EventScript_EclipseScoutExposed
	msgbox EryonCachoeiras_Text_EclipseScoutBefore, MSGBOX_DEFAULT
	release
	end

EryonCachoeiras_EventScript_EclipseScoutExposed::
	msgbox EryonCachoeiras_Text_EclipseScoutExposed, MSGBOX_DEFAULT
	release
	end

EryonCachoeiras_EventScript_CrystalResidue::
	lock
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonCachoeiras_EventScript_CrystalResidueClue
	msgbox EryonCachoeiras_Text_CrystalResidueBefore, MSGBOX_DEFAULT
	release
	end

EryonCachoeiras_EventScript_CrystalResidueClue::
	msgbox EryonCachoeiras_Text_CrystalResidueClue, MSGBOX_DEFAULT
	release
	end

EryonCachoeiras_Text_RangerBefore:
	.string "GUARDA: As cachoeiras\n"
	.string "escondem trilhas antigas.\p"
	.string "Nao se aproxime das\n"
	.string "correntezas sozinho.$"

EryonCachoeiras_Text_RangerClue:
	.string "GUARDA: Homens da ECLIPSE\n"
	.string "levaram caixas rio abaixo.\p"
	.string "Uma barcaca seguiu\n"
	.string "para a Vila das Aguas.$"

EryonCachoeiras_Text_EclipseScoutBefore:
	.string "VIAJANTE: Estou apenas\n"
	.string "observando o nivel do rio.\p"
	.string "Siga seu caminho.$"

EryonCachoeiras_Text_EclipseScoutExposed:
	.string "ECLIPSE: Voce veio de\n"
	.string "Umbra? Tarde demais!\p"
	.string "Nossa carga ja desceu\n"
	.string "o rio. Nao nos siga.$"

EryonCachoeiras_Text_CrystalResidueBefore:
	.string "Ha um po brilhante\n"
	.string "preso nas pedras molhadas.\p"
	.string "A correnteza e forte.$"

EryonCachoeiras_Text_CrystalResidueClue:
	.string "O po combina com os\n"
	.string "cristais roubados!\p"
	.string "Alguem despejou residuos\n"
	.string "da carga na agua.$"
