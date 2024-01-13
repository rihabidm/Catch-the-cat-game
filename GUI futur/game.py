import pygame
import pytmx
import pyscroll
from cat import Cat
import tkinter as tk



pygame.init()
screen=pygame.display.set_mode((950,640))
pygame.display.set_caption("catch the cat")

tmx_data= pytmx.util_pygame.load_pygame('C:/Users/PC/Desktop/game/carte.tmx')
map_data=pyscroll.data.TiledMapData(tmx_data)
map_layer=pyscroll.orthographic.BufferedRenderer(map_data,screen.get_size())


chat=Cat(450,300)
grp=pyscroll.PyscrollGroup(map_layer=map_layer,default_layer=0)
grp.add(chat)

# Création de la fenêtre Tkinter et du canevas
fenetre = tk.Tk()
fenetre.title("Plateau de jeu")
canvas = tk.Canvas(fenetre, width=950, height=640)
canvas.pack()


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




dessiner_plateau()


#boucle du jeu
running = True


while running:
    grp.draw(screen)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running = False

 
fenetre.mainloop()
pygame.quit()
