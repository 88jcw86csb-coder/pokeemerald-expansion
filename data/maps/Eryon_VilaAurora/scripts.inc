@ Eryon: initial Professor Elya dialogue (placeholder overworld graphic).
@ Starter award and story flags will be implemented in a separate verified event.
EryonVilaAurora_EventScript_ProfessorElya::
	lock
	faceplayer
	msgbox EryonVilaAurora_Text_ProfessorElya, MSGBOX_DEFAULT
	release
	end

EryonVilaAurora_Text_ProfessorElya:
	.string "PROF. ELYA: Bem-vindo a Eryon!\\p"
	.string "A natureza daqui guarda segredos.\\p"
	.string "Logo teremos muito a descobrir!$"
