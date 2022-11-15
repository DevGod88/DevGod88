## Bibliothèques utilisées ##
from tkinter import Tk, Canvas, Label, Button, Toplevel, Scrollbar, Frame, Text # Interface graphique
from tkinter.filedialog import askdirectory # Fenêtre d'enregistrement de fichier
from tkinter.messagebox import askyesno, showerror # Messages d'erreurs et de confirmation
import tkinter.ttk as ttk # Widgets Tkinter modifiées pour ressembler au style de Windows
from PIL import ImageTk, Image # Gérer les images
from datetime import datetime # Date et heure
from os import getcwd # Obteir informations sur le programme en cours d'exécution


__version__ = "1.2"
__author__ = "Renan LAUTIN <1G2>"

## Fonctions ##

def restart() :
    """Remet les valeurs à zéro dans la perspective d'une nouvelle partie

    Returns:
        list: liste contenant les différentes positions possibles
        list: liste initiale contenant plusieurs listes représentant chacune une ligne du plateau
        int: Valeur initiale du tour (1 = rouge)
        bool: Valeur initiale de la condition "Le plateau contient une configuration gagnante"
    """
    # Détermination de la date à laquelle la partie commence
    global jour_debut
    jour_debut = datetime.now().strftime("%d")

    # Initialisation des positions de jeu
    base_x = 40
    base_y = 67
    elts = []
    for i in range(6) :
        for j in range(7) :
            oval = main_can.create_oval(base_x, base_y, base_x+130, base_y+130, fill="thistle1")
            elts.append(oval)
            base_x+=150
        base_y+=166
        base_x=40

    return elts, [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]], 1, False

def test_value(list:list) :
    """
    Teste les valeurs de la liste mise en argument afin
    de savoir si la liste contient une configuration de victoire.

    Args:
        list (list): La liste à tester
    """

    valeur = None # Prend les valeurs 1, 2 ou None
    compt = 0
    correct = 0
    for i in list :
        if len(i) >= 4 : # Ne teste que les listes de listes pouvant contenir 4 pions identiques
            compt+=1
            correct = 0
            for j in range(len(i)) : 
                if i.count(1) >= 4 or i.count(2) >= 4 :
                    if valeur == None : # Si aucune valeur n'a été vue avant
                        if i[j] != 0 :
                            valeur = i[j]
                            correct += 1

                    elif i[j] == valeur : correct += 1 # Si la valeur testée correspond à la valeur d'avant

                    else : # Si la valeur testée ne correspond pas à la valeur d'avant
                        if i[j] != 0 : valeur, correct = i[j], 1 # Si la valeur testée est différente de 0
                        else :correct, valeur = 0, None # Si la valeur testée est nulle

                    if correct >= 4 :
                        global config_gagnante
                        config_gagnante = True
                        victoire(valeur) # Si 4 pions sont allignés, alors une victoire
                        
# Fonction au click
def click(event):
    """Fonction qui :
        - Met à jour le plateau
        - Teste la victoire
        - Teste le match nul
    Ces tests sont réalisés seulement quand un click est fait par un utilisateur.

    Args:
        event (tkinter.Event): Informations sur l'évènement qui a déclenché la fonction
    """
    # Place le pion et modifie l'index des listes correspondant
    global recap
    #global window, recap, text, line
    if event.x < 1069 and event.y > 20 and not config_gagnante :
        global tour, row_grid, canvas, line
        if tour %2 == 0 : main_can.itemconfigure(indic, fill = "red")
        elif tour % 2 == 1 : main_can.itemconfigure(indic, fill = "yellow")
        played = 0
        x_click = event.x
        chosen_column = int((x_click-20)/150)
        for i in range(5,-1,-1) :
            if row_grid[i][chosen_column] == 0 and played == 0 :
                if tour % 2 == 0 : row_grid[i][chosen_column] = 1
                else : row_grid[i][chosen_column] = 2
                played = 1
                break
        
        # Modifie le recap et le canvas de droite
        _now_time = datetime.now().strftime("[%H:%M:%S] ")
        if tour%2 == 0 and played == 1:
            recap += f"\n\n{_now_time}{joueur2} a joué en colonne {chosen_column+1}"
            text.config(state="normal")
            text.insert(f"{line}.0", f"{_now_time}{joueur2} a joué en colonne {chosen_column+1}\n\n")
            text.config(state="disabled")
            text.see("end")
            line+=2
        elif tour%2 == 1 and played == 1:
            recap += f"\n\n{_now_time}{joueur1} a joué en colonne {chosen_column+1}"
            text.config(state="normal")
            text.insert(f"{line}.0", f"{_now_time}{joueur1} a joué en colonne {chosen_column+1}\n\n")
            text.config(state="disabled")
            text.see("end")
            line+=2
        
        else : showerror("Erreur", "Vous ne pouvez pas jouer sur une colonne pleine.")

        # Met à jour le plateau visuel
        col = 0
        for i in row_grid :
            for j in i :
                if j == 1 : main_can.itemconfigure(pos[col], fill = "yellow")
                if j == 2 : main_can.itemconfigure(pos[col], fill = "red")
                col+=1

        full_grid = []
        for i in row_grid :
            for j in i :
                full_grid.append(j)


        test_value(row_grid)

        
        # Crée une liste contenant des listes représentant chacune une colonne
        column_grid = []
        for i in range(7) :
            column = []
            for j in range(i,len(full_grid),7) :
                column.append(full_grid[j])
            column_grid.append(column)

        test_value(column_grid)


        # Test des diagonales de gauche à droite
        full_diago = []

        # Reconnait les 7 premières diagonales 
        for i in range(6) :
            diago = []
            for i in range(i,len(full_grid),6) :
                diago.append(full_grid[i])
                if i in [0,7,13,14,20,21,27,28,34,35,41] :
                    break
            full_diago.append(diago)

        # Reconnait les 5 dernières diagonales
        for i in range(6,len(full_grid), 7) :
            diago = []
            for i in range(i,len(full_grid),6) :
                diago.append(full_grid[i])
            full_diago.append(diago)
        test_value(full_diago)


    # Test des diagonales de droite à gauche
        full_diago = []

        # Reconnait les 7 premières diagonales
        for i in range(7) :
            diago = []
            for i in range(i,len(full_grid),8) :
                diago.append(full_grid[i])
                if i in [6,7,13,14,20,21,27,28,34,35,41] :
                    break
            full_diago.append(diago)

        # Reconnait les 5 dernières diagonales
        for i in range(7,len(full_grid), 7) :
            diago = []
            for i in range(i,len(full_grid),8) :
                diago.append(full_grid[i])
            full_diago.append(diago)

        test_value(full_diago)
        
        # Compte le nombre de positions jouables dans la perspective d'un match nul
        compt_0 = 0
        for i in row_grid : 
            for j in i :
                if j == 0 : compt_0 += 1
        
        if compt_0 == 0 : # <=> Si match nul : 
            nul = Toplevel(window)
            nul.geometry("255x160+880+300")
            nul.attributes("-topmost", True)
            nul.resizable(width = False, height = False)
            nul.title("Match nul")
            label = Label(nul, text = "La partie a donné\nlieu à un match nul.\nLes scores ne\nchangent pas.", font = ("Century", 15, "bold"), padx=20)
            label.grid(column = 1, columnspan=2, row = 1)
            ttk.Button(nul, text = "Rejouer", command = lambda:new_grid(nul), width = 15).grid(column = 1, row=2)#.pack(side="left")
            ttk.Button(nul, text = "Quitter", command = lambda:quit_game(window), width = 15).grid(column = 1, row = 3)#.pack(side="left")
            ttk.Button(nul, text = "Télécharger le\nrécapitulatif\nde la partie", command = lambda:downloadrecap(nul), width = 15).grid(column = 2, columnspan=2, row = 2, rowspan=2)
            _now_time = datetime.now().strftime("[%H:%M:%S] ")
            recap+=f"{_now_time} La partie a donné lieu à un match nul. Les scores ne changent pas."
            text.config(state="normal")
            text.insert(f"{line}.0", f"{_now_time}La partie a donné lieu à un match nul. Les scores ne changent pas.\n\n")
            text.config(state="disabled")
            text.see("end")
            line+=2
        
        # Si le joueur a joué dans une colonne pleine
        if played == 0 :
            tour -= 1
            if tour %2 == 0 : main_can.itemconfigure(indic, fill = "red")
            elif tour % 2 == 1 : main_can.itemconfigure(indic, fill = "yellow")
        tour += 1
    

def downloadrecap(toplevel:Toplevel) :
    """Fonction utilisant le système builtin Python pour écrire dans un fichier.
        /!\ Utilisation de tkinter.filedialog.askdirectory()
    """
    toplevel.attributes("-topmost", False)
    _dir = askdirectory(title="Enregistrer le fichier", initialdir=getcwd())
    save_date = datetime.now().strftime("%Y-%m-%d - %Hh %Mmin %Ss")
    with open(_dir+f"/recap_{save_date}.txt", "w") as _file :
        _file.write(recap)
        _file.close()
        toplevel.attributes("-topmost", True)
        toplevel.iconify()
        toplevel.deiconify()

def victoire(gagnant) :
    """
    Fonction qui se lance lors d'une victoire.
    Ouvre un toplevel qui propose trois options :
        - Rejouer : Recommencer une partie
        - Quitter : Fin du programme.
        - Télécharger le récapitulatif de la partie : Ecrit dans un fichier le contenu de la variable recap

    Args:
        gagnant (int): id de la couleur gagnante
    """
    # Détermination du jour de fin de partie
    global joueur1, joueur2, score1label, score2label, line, text, score1, score2, recap
    _now_time = datetime.now().strftime("[%H:%M:%S] ")

    # Mise à jour du recap et du canvas à droite
    if gagnant == 1 :
        gagnant = joueur2
        score2 += 1
        score2label['text'] = "Score : "+ str(score2)
        recap+=f"\n\n{_now_time}{joueur2} a gagné ! Nouveaux scores : {joueur1} : {score1} - {score2} : {joueur2}"
        text.config(state="normal")
        text.insert(f"{line}.0", f"{_now_time}{joueur2} a gagné ! Nouveaux scores : {joueur1} : {score1} - {score2} : {joueur2}\n\n")
        text.config(state="disabled")
        text.see("end")
        line+=2
    else :
        gagnant = joueur1
        score1 += 1
        score1label['text'] = "Score : "+ str(score1)
        recap+=f"\n\n{_now_time}{joueur1} a gagné ! Nouveaux scores : {joueur1} : {score1} - {score2} : {joueur2}"
        text.config(state="normal")
        text.insert(f"{line}.0", f"{_now_time}{joueur1} a gagné ! Nouveaux scores : {joueur1} : {score1} - {score2} : {joueur2}\n\n")
        text.config(state="disabled")
        line+=2


    # Calcul de la durée

    global jour_debut
    jour_fin = datetime.now().strftime("%d")

    h_debut_split = h_debut.split(":")
    end_date = datetime.now().strftime("%H:%M:%S")
    end_date_split = end_date.split(":")

    debut_sec = 0
    debut_sec += int(h_debut_split[0])*3600 + int(h_debut_split[1])*60 + int(h_debut_split[2])
    end_sec = 0
    end_sec += int(end_date_split[0])*3600 + int(end_date_split[1])*60 + int(end_date_split[2])

    if jour_debut == jour_fin : # <=> Si la partie était sur un seul jour : 
        duree = end_sec - debut_sec
        
    else : # <=> Si la partie s'est commencé un jour et a fini le jour suivant
        print("autre jour")
        duree = (86400 - debut_sec) + end_sec 
    
    duree_min = int(duree / 60)
    duree_sec = duree % 60

    # Mise à jour du recap et du canvas à droite
    recap += f"\n\nLa partie s'est terminée à {end_date} pour une durée totale de {duree_min} minute(s) et {duree_sec} seconde(s)."
    text.config(state="normal")
    text.insert(f"{line}.0", f"La partie s'est terminée à {end_date} pour une durée totale de {duree_min} minute(s) et {duree_sec} seconde(s).\n\n")
    text.config(state="disabled")
    text.see("end")
    line+=2

    # Toplevel de victoire
    global win_screen
    win_screen = Toplevel(window)
    win_screen.geometry("200x130+880+300")
    win_screen.title("Résulats de la partie")
    win_screen.attributes("-topmost", True)
    win_screen.resizable(width = False, height = False)
    label = Label(win_screen, text = f"Fin de partie.\nLe gagnant est\n{gagnant}", font = ("Century", 15, "bold"), padx=20)
    label.grid(column = 1, columnspan=2, row = 1)
    ttk.Button(win_screen, text = "Rejouer", command = lambda:new_grid(win_screen), width = 15).grid(column = 1, row=2)
    ttk.Button(win_screen, text = "Quitter", command = lambda:quit_game(window), width = 15).grid(column = 1, row = 3)
    ttk.Button(win_screen, text = "Télécharger le\nrécapitulatif\nde la partie", command = lambda:downloadrecap(win_screen), width = 15).grid(column = 2, columnspan=2, row = 2, rowspan=2)#.pack(side="right")
    
    
def valider(player:int, entry:Text, toplevel:Toplevel) :
    """
    Fonction qui se lance lors de la validation du changement de nom.

    Args:
        player (int): id du joueur changeant de nom
        entry (Text): tkinter.Text() qui contient (au moment de la validation) le nom tapé par l'utilisateur
        toplevel (Toplevel): Fenêtre à fermer
    """
    global joueur1, joueur2, joueur1label, joueur2label, score1, score2, score1label, score2label, recap, text, line
    if askyesno("Confirmation", "Le changement des noms entrainera\nla réinitialisation des scores et du plateau.\nContinuer ?") :
        if len(entry.get("1.0", "end-1c")) > 0  and len(entry.get("1.0", "end-1c")) <= 15 and "\n" not in entry.get("1.0", "end-1c") : #Le nom du joueur doit contenir entre 1 et 15 caractères inclus (espaces compris) et ne doit pas contenir de retour à la ligne
            _now_time = datetime.now().strftime("[%H:%M:%S] ")
            if player == 1 :
                old_player = joueur1
                joueur1 = entry.get("1.0", "end-1c")
                joueur1label["text"] = joueur1
                recap += f"\n\n{_now_time}{old_player} a laissé sa place à {joueur1}"
                text.config(state="normal")
                text.insert(f"{line}.0", f"{_now_time}{old_player} a laissé sa place à {joueur1}\n\n")
                text.config(state="disabled")
                text.see("end")
                line+=2
            elif player == 2 :
                old_player = joueur2
                joueur2 = entry.get("1.0", "end-1c")
                joueur2label["text"] = joueur2
                recap += f"\n\n{_now_time}{old_player} a laissé sa place à {joueur2}"
                text.config(state="normal")
                text.insert(f"{line}.0", f"{_now_time}{old_player} a laissé sa place à {joueur2}\n\n")
                text.config(state="disabled")
                text.see("end")
                line+=2
            score1, score2 = 0, 0
            score1label['text'] = "Score : "+str(score1)
            score2label['text'] = "Score : "+str(score2)
            new_grid(toplevel)
            toplevel.destroy()
        elif len(entry.get("1.0", "end-1c")) == 0 : showerror("Echec", "Le nom doit contenir au moins un caractère.")
        elif "\n" in entry.get("1.0", "end-1c") : showerror("Erreur", "Le nom de joueur ne doit pas contenir de retour à la ligne")
        else : showerror("Echec", "Le nom de joueur ne peut pas dépasser une longueur de 15 caractères.")
    else :
        toplevel.destroy()

def quit_game(fenetre:Tk) :
    """Fonction permettant de quitter le jeu avec confirmation"""
    proceed = askyesno("Attention", "Vous allez quitter le jeu.\nConfirmer ?")
    if proceed : fenetre.destroy()

def change_name(player:int) :
    """
    Fonction qui ouvre un tkinter.Toplevel() qui contient un tkinter.Text() qui permet de saisir un nouveau nom

    Args:
        player (int): id du joueur qui change de nom
    """
    toplevel = Toplevel(window)
    toplevel.geometry("100x50+1150+200")
    toplevel.attributes("-topmost", True)
    toplevel.resizable(width = False, height = False)
    toplevel.title("Changement de nom")
    entry = Text(toplevel, height = 1, width = 14)
    entry.pack()
    entry.focus_force()
    validate_button = ttk.Button(toplevel, text = "Valider", command=lambda:valider(player, entry, toplevel))
    validate_button.pack()
    

def _help() :
    aide = Toplevel(window)
    aide.geometry("900x275+520+400")
    aide.attributes("-topmost", True)
    aide.resizable(width=False, height=False)
    aide.title("Comment jouer au Puissance 4 ?")

    Label(aide, text="""Le joueur rouge commence à jouer dans la colonne de son choix.
    C'est ensuite au tour du joueur jaune de jouer
    dans la colonne de son choix et ainsi de suite
    jusqu'à ce que quatre pions de la même couleur
    soient alignés en ligne, en colonne ou en diagonale.
    Si le plateau est rempli sans qu'aucun joueur n'ait aligné
    quatre pions, la partie est déclarée nulle.""", font="System 20 bold").pack()

    return_b = ttk.Button(aide, text="Retour au jeu", command = aide.destroy)
    return_b.pack()
        
def begin() :
    """Fonction qui s'exécute quand le jeu commence."""
    global window, main_can, indic, pos, row_grid, tour, config_gagnante
    start.destroy() # On détruit le menu pour laisser place au jeu.

    global score1, score2
    score1 = 0
    score2 = 0
    
    window = Tk()
    window.attributes("-fullscreen", True)
    window.title(f"Puissance4 - {__author__}")
    #window.attributes("-alpha", 0.5) # Utile lors de tests à faire. Rend la fenêtre légèrement transparente

    # Définition du canvas principal
    main_can = Canvas(window, height = 1080, width = 1920, bg = "pale goldenrod")
    main_can.place(x=0,y=0)
    
    # Boutons en haut à droite
    Button(main_can, text = "Recommencer une grille", command = lambda:new_grid(None), font = "Helvetica 15 bold", height=3, width = 20, bg = "DarkSlateGray1").place(x=1600, y=50)#.pack(side="top", anchor = "e")
    Button(main_can, text = "Comment jouer ?", command = _help, font = "Helvetica 15 bold", height=3, width = 20, bg = "DarkSlateGray1").place(x=1600, y=160)#.pack(side="top", anchor = "e")
    Button(main_can, text = "Quitter le jeu", command = lambda:quit_game(window), font = "Helvetica 15 bold", height=3, width = 20, bg = "DarkSlateGray1").place(x=1600, y=270)#.pack(side="top", anchor = "e")
    
    # Initialisation du système de changement de nom
    global joueur1label, joueur2label, joueur1, joueur2, score1label, score2label
    joueur1 = "Joueur1"
    joueur2 = "Joueur2"

    modify_im = ImageTk.PhotoImage(Image.open("Pictures/modify.png"), master = window)
    
    # Bouton de modification du nom du joueur 1
    change_name_1 = Button(image = modify_im, command = lambda:change_name(1), height = 38, width = 38)
    change_name_1.place(x = 1210, y = 50)

    # Label contenant le nom par défaut du joueur 1
    joueur1label = Label(text = "Joueur1", bg = "red", font = "Century 25 bold")
    joueur1label.place(x=1260, y = 50)

    # Label contenant le score du joueur 1
    score1label = Label(text = "Score : "+str(score1), font = "Century 25 bold")
    score1label.place(x=1260, y=95)
    
    # Bouton de modification du nom du joueur 2
    change_name_2 = Button(image = modify_im, command = lambda:change_name(2), height = 38, width = 38)
    change_name_2.place(x = 1210, y = 200)

    # Label contenant le nom par défaut du joueur 2
    joueur2label = Label(text = "Joueur2", bg = "yellow", font = "Century 25 bold")
    joueur2label.place(x = 1260, y = 200)

    # Label contenant le score du joueur 2
    score2label = Label(text = "Score : "+str(score2), font = "Century 25 bold")
    score2label.place(x=1260, y=245)

    # Définition du canvas à droite contenant un récapitulatif des actions des joueurs pour la session de jeu en cours
    global text, line
    canvas = Canvas(window) # On crée un canvas
    canvas.pack(side = "right", padx = 300) # On le place

    frame = Frame(window) # On crée une frame (en gros, une fenêtre qui peut apartenir à une autre fenêtre)

    canvas.create_window((0,0), window = frame, anchor="nw") # On place la frame dans le canvas
    text = Text(frame, font=("Lucida Sans", 15, "bold"), width = 45, height = 20) # On crée la zone de texte

    # create a scrollbar widget and set its command to the text widget
    scrollbar_y = Scrollbar(frame, orient='vertical', command=text.yview) # On crée l'ascenseur
    scrollbar_y.pack(side = "right", fill = "y") # On le place
    text.pack(side = "right") # Seulement maintenant, on place la zone de texte de façon à ce que la scrollbar se retrouve à droite de la zone de texte
    
    # On initialise la zone de texte
    line = 1
    text.config(state="normal")
    text.insert(f"{line}.0", f"Début de la partie à {h_debut}\n\n")
    text.config(state="disabled")
    text.see("end")
    line+=2

    # On lie la scrollbar et la zone de texte
    text['yscrollcommand'] = scrollbar_y.set

    # On permet à l'utilisateur de scroller avec la molette de la souris
    canvas.bind("<MouseWheel>", lambda event:canvas.yview_scroll(-1*(event.delta/120), "units"))

    
    # On affiche la zone de jeu
    img = ImageTk.PhotoImage(Image.open("Pictures/gamezone.png"), master = window)
    main_can.create_image(0,0, image = img, anchor = "nw")
    Button(text = "Recommencer", command = lambda:restart())

    # Crée l'indicateur en bas de la zone de jeu qui indique qui doit jouer pour ce tour
    Label(text = "C'est au tour du joueur : ", font = "Helvetica 18 bold", bg = "pale goldenrod").place(x=1160, y=900)

    indic = main_can.create_oval(1235, 950, 1355, 1070, fill = "red")

    # Affichage du logo
    logo_im_in_game = ImageTk.PhotoImage(Image.open("Pictures/logo_in_game.png"), master = window)
    main_can.create_image(1700, 950, image = logo_im_in_game)

    Label(text = f"Fait par {__author__}, 2022", font = ("Helvetica", 15, "bold"), bg = "pale goldenrod").place(x=1530, y=1000)
    
    # Début de la partie
    pos, row_grid, tour, config_gagnante = restart()

    # On active la fonction click
    main_can.bind("<ButtonPress-1>", click)

    window.mainloop()

def new_grid(toplevel:Toplevel) :
    """Réinitialisation du plateau

    Args:
        toplevel (Toplevel): toplevel à détruire au moment de la réinitialisation
    """
    global game_zone, main_can, indic, pos, row_grid, tour, config_gagnante, h_debut, line, recap
    h_debut = datetime.now().strftime("%H:%M:%S")
    recap += f"\n\nNouvelle partie. Début de la partie à {h_debut}"
    text.config(state="normal")
    text.insert(f"{line}.0", f"Nouvelle partie. Début de la partie à {h_debut}\n\n")
    text.config(state="disabled")
    text.see("end")
    line+=2
    if toplevel != None : toplevel.destroy()
    indic = main_can.create_oval(1235, 950, 1355, 1070, fill = "red")
    pos, row_grid, tour, config_gagnante = restart()


## Programme principal ##

h_debut = datetime.now().strftime("%H:%M:%S")
recap = f"*** Voici l'historique de jeu pour cette partie. ***\n\nDébut de la partie à {h_debut}" # On initialise la variable de récapitulatif

# Définition du menu
start = Tk()
start.geometry("600x600+650+150")
start.title(f"Puissance 4 - {__author__} - Menu")

# Fond bleu
background = Canvas(height=600, width=600, bg = "#5B6FE5")
background.place(x=0,y=0)

# Logo
logo_pic = ImageTk.PhotoImage(Image.open("Pictures/logo.png"), master = start)
background.create_image(50, 0, image = logo_pic, anchor = "nw")

# Les deux boutons
Button(start, text = "Quitter", command=lambda:quit_game(start), width = 20, height = 5, relief="solid", font = "Helbetica 20 bold", bg = "#5B6FE5").pack(side="bottom",anchor = "n", pady = 35)
Button(start, text = "Nouvelle partie", command = begin, width = 20, height = 5, relief = "solid", font = "Helbetica 20 bold", bg = "#5B6FE5").pack(side = "bottom", anchor = "s", pady = 20)

start.mainloop()