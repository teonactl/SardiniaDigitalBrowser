

categorie_str="""
VIDEO
    Cortometraggi
    Cinegiornali
    Concerti e festival
    Convegni e seminari
    Documentari
    Documenti multimediali
    Film
    Gare poetiche
    Interviste
    Programmi televisivi
    Rappresentazioni teatrali
    Spot
    Video istituzionali
IMMAGINI
    Ambiente e territorio
    Archeologia
    Architettura
    Arte
    Artigianato
    Atti di governo
    Economia e società
    Cartografia
    Enogastronomia
    Eventi
    Flora e fauna
    Letteratura
    Luoghi della cultura
    Spettacolo
    Sport
    Storia e tradizioni
AUDIO
    Canti a chitarra
    Canti a tenore
    Canti monodici
    Canti polivocali
    Canti sacri
    Discorsi
    Favole
    Gare poetiche
    Interviste
    Musica contemporanea
    Narrativa
    Poesie
    Strumenti
    Trasmissioni radiofoniche
TESTI
    Annuari
    Atti di convegno
    Brochure
    Cataloghi
    Dizionari - enciclopedie
    Documenti d'archivio
    Guide
    Epistolari
    Libretti
    Monografie - saggi
    Narrativa
    Periodici
    Poesie
ARGOMENTI
    Ambiente e territorio
    Archeologia
    Architettura
    Arte
    Artigianato
    Atti di governo
    Cartografia
    Economia e società
    Enogastronomia
    Eventi
    Flora e fauna
    Letteratura
    Lingua sarda
    Luoghi della cultura
    Musica
    Spettacolo
    Sport
    Storia e tradizioni
"""




with open("out", "w+") as f :

	for item in categorie_str.strip().split("\n"):
		model = f'\n\t\t\t\t\tDrawerClickableItem:\n\t\t\t\t\t\ttext:"{item.strip()}"\n\t\t\t\t\t\ton_press : app.but_cb(self)\n\t\t\t\t\t\ttext_color : "#4a4939"'                    

		

		print(model)
		f.write(model)
