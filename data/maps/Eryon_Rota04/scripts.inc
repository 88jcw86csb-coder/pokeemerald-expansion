Eryon_Rota04_MapScripts::
	.byte 0

@ The orchard scout points travelers toward the longer regional trail.
EryonRota04_EventScript_OrchardScout::
	lock
	faceplayer
	msgbox EryonRota04_Text_OrchardScout, MSGBOX_DEFAULT
	release
	end

EryonRota04_Text_OrchardScout:
	.string "EXPLORADOR: Os pomares ficam\n"
	.string "para oeste, perto da vila.\p"
	.string "A leste, a trilha encontra\n"
	.string "a antiga Rota 03.$"
