@ Eryon: the first foothills beyond the eastern trail.
EryonSerra_EventScript_Geologist::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonSerra_EventScript_GeologistBadge
	msgbox EryonSerra_Text_GeologistBefore, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_GeologistBadge::
	msgbox EryonSerra_Text_GeologistBadge, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_Explorer::
	lock
	faceplayer
	msgbox EryonSerra_Text_Explorer, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_CrystalOutcrop::
	lock
	msgbox EryonSerra_Text_CrystalOutcrop, MSGBOX_DEFAULT
	release
	end

EryonSerra_Text_GeologistBefore:
	.string "GEOLOGO: Esta serra e antiga.\p"
	.string "As pedras guardam marcas\n"
	.string "de muito antes das cidades.$"

EryonSerra_Text_GeologistBadge:
	.string "GEOLOGO: O simbolo do eclipse\n"
	.string "apareceu nos meus estudos.\p"
	.string "Alguem retirou cristais\n"
	.string "desta encosta recentemente.$"

EryonSerra_Text_Explorer:
	.string "EXPLORADORA: Nao tenha pressa.\p"
	.string "Ha caminhos escondidos\n"
	.string "entre as pedras da serra.$"

EryonSerra_Text_CrystalOutcrop:
	.string "Uma rocha foi escavada.\p"
	.string "Pequenos fragmentos brilham\n"
	.string "sob a luz do sol.$"
