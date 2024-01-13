import tkinter as tk #inportation de la bibliotheque tkinter pour créer des interfaces graphiques

# Initialiser une liste pour garder trace des cases cochées
cases_cochees = []


# Définition de la fonction pour dessiner le plateau
def dessiner_plateau():
    #Déclaration des variables globales
    global cercle_id  # Identifiant du cercle noir au centre du plateau
    global cases_blanches  # Liste pour stocker les coordonnées des cases blanches
    global cases_vertes  # Liste pour stocker les coordonnées des cases vertes
    
    cases_blanches = []  # Liste pour stocker les coordonnées des cases blanches
    cases_vertes = [] # Liste pour stocker les coordonnées des cases vertes

    
    for i in range(11):# Boucle pour parcourir les lignes du plateau
        for j in range(15):# Boucle pour parcourir les colonnes du plateau
            if i == 0 or i == 10 or j == 0 or j == 14: # Si la case est sur le bord du plateau
                #Rectangle:
                #canvas.create_rectangle(x1, y1, x2, y2,......)
                #(x1,y1) : top left     (x2,y2): bottom right
                canvas.create_rectangle(j*50, i*50, (j+1)*50, (i+1)*50, fill='green', outline='green')
                cases_vertes.append((i, j)) # Ajouter les coordonnées de la case verte à la liste
            else:
                # Dessiner une case blanche pour les cases internes du plateau
                rect_id = canvas.create_rectangle(j*50, i*50, (j+1)*50, (i+1)*50, fill='white', outline='black')
                cases_blanches.append((i, j))  # Ajouter les coordonnées de la case blanche

                # Si la case est à la position spécifique (5, 7), dessiner un cercle noir au centre
                if i == 5 and j == 7:
                    cercle_id = canvas.create_oval(j*50+10, i*50+10, (j+1)*50-10, (i+1)*50-10, fill='black')
                    

global ni
global nj
ni,nj=5,7 #coordonné initial du cercle
                
def cocher_case(event):
    global cercle_id
    x, y = event.x, event.y # Récupérer les coordonnées x et y du clic de la souris
    i, j = y // 50, x // 50 # Convertir les coordonnées en indices de ligne et de colonne
    if 0 < i < 10 and 0 < j < 14 and (i,j)!=(ni,nj): # Vérifier si les indices i et j sont dans la plage valide du plateau
        if (i, j) not in cases_cochees :  # Vérifier si la case n'est pas déjà cochée
            if (i, j) in cases_blanches :  # Vérifier si la case est blanche
                cases_cochees.append((i, j)) # Ajouter les coordonnées de la case cochée à la liste
                canvas.itemconfig(canvas.find_closest(x, y), fill='red')  # Changer la couleur de la case cochée en rouge
                deplacer_cercle_minimax() # Appeler la fonction pour déplacer le cercle noir
            

global i
global j

i, j = 5, 7 #coordonné initial du cercle


def evaluer_etat(etat):
    # Coordonnées du centre fixe
    centre_x = 350
    centre_y = 250
    # Coordonnées du cercle (état)
    cercle_x, cercle_y = etat
    # Calcul de la distance euclidienne entre le centre et le cercle
    distance = ((centre_x - cercle_x) ** 2 + (centre_y - cercle_y) ** 2) ** 0.5
    # Retourne la valeur négative de la distance
    return -distance

def actions_possibles(etat):
    # Déplacements possibles en x et y
    dx = [-1, 0, 1, 0, -1, 1, -1, 1]
    dy = [0, -1, 0, 1, -1, -1, 1, 1]
    x, y = etat# Coordonnées de l'état
    actions = [(x+dx[i], y+dy[i]) for i in range(8)] # Générer les nouvelles coordonnées en fonction des déplacements possibles

    # Filtrer les actions pour ne conserver que celles qui sont dans les cases blanches
    return [(i, j) for i, j in actions if (i, j) in cases_blanches] 

def minimax(etat, profondeur, alpha, beta, maximizing):
    if profondeur == 0: # Cas de base : profondeur atteinte, retourner l'évaluation de l'état
        return evaluer_etat(etat)

    # Cas où l'on maximise la valeur
    if maximizing:
        valeur = float('-inf') # Initialisation de la valeur par moins l'infini


        # Parcours de toutes les actions possibles à partir de l'état actuel
        for action in actions_possibles(etat):
            # Appel récursif pour évaluer l'action et mettre à jour la valeur maximale
            valeur = max(valeur, minimax(action, profondeur-1, alpha, beta, False))
            # Mise à jour de la valeur alpha pour l'élagage alpha-bêta
            alpha = max(alpha, valeur)
            # algo alpha-bêta : arrêt de la recherche si beta <= alpha
            if beta <= alpha:
                break

        # Retourne la valeur maximale trouvée
        return valeur
    else:
        # Cas où l'on minimise la valeur
        valeur = float('inf') # Initialisation de la valeur par l'infini


        # Parcours de toutes les actions possibles à partir de l'état actuel
        for action in actions_possibles(etat):
            # Appel récursif pour évaluer l'action et mettre à jour la valeur minimale
            valeur = min(valeur, minimax(action, profondeur-1, alpha, beta, True))

            # Mise à jour de la valeur beta pour l'élagage alpha-bêta
            beta = min(beta, valeur)

            # Élagage alpha-bêta : arrêt de la recherche si beta <= alpha
            if beta <= alpha:
                break
        # Retourne la valeur minimale trouvée
        return valeur



def deplacer_cercle_minimax():
    # Déclarations des variables globales utilisées dans la fonction
    global cercle_id
    global cases_blanches
    global i
    global j
    global cases_cochees
    global ni
    global nj
    # Directions possibles pour le déplacement du cercle
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    # Initialisation des meilleures actions et de la meilleure valeur
    meilleures_actions = []
    meilleure_valeur = float('-inf')

    # Boucle à travers les directions possibles
    for dx, dy in directions:
        ni, nj = i + dx, j + dy
        if (ni, nj) not in cases_cochees: # Vérifier si la case n'est pas déjà cochée
            # Évaluation de l'état résultant par l'algorithme minimax
            valeur = minimax((ni, nj), profondeur=3, alpha=float('-inf'), beta=float('inf'), maximizing=False)

            # Mettre à jour les meilleures actions si une valeur meilleure est trouvée
            if valeur > meilleure_valeur:
                meilleure_valeur = valeur
                meilleures_actions = [(ni, nj)]
            elif valeur == meilleure_valeur:
                meilleures_actions.append((ni, nj))

    # Si des meilleures actions sont trouvées
    if meilleures_actions:
        ni, nj = meilleures_actions[0]
        # Supprimer le cercle actuel et créer un nouveau cercle à la meilleure position
        canvas.delete(cercle_id)
        cercle_id = canvas.create_oval(nj*50+10, ni*50+10, (nj+1)*50-10, (ni+1)*50-10, fill='black')

        # Vérifier si le nouveau cercle est sur une case verte
        if (ni, nj) in cases_vertes:
            canvas.create_text(375, 525, text="Le chat a échappé !", fill="black", font=("Helvetica", 12))
        else:
            # Mettre à jour les coordonnées i, j
            i, j = ni, nj
    else:
        # Si aucune meilleure action n'est trouvée
        canvas.create_text(375, 525, text="vous avez réussi à attraper le chat", fill="black", font=("Helvetica", 12))


# Créer une fenêtre
fenetre = tk.Tk()
fenetre.title("Plateau de jeu")

# Créer un canevas pour dessiner le plateau
canvas = tk.Canvas(fenetre, width=750, height=550)
canvas.pack()

# Dessiner le plateau
dessiner_plateau()

# Lier la fonction cocher_case à un clic de souris
canvas.bind("<Button-1>", cocher_case)

# Démarrer la boucle principale
fenetre.mainloop()








