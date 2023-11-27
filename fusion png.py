#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Lilly
#
# Created:     22/11/2023
# Copyright:   (c) Lilly 2023
#-------------------------------------------------------------------------------

from PIL import Image
import os

def fusionner_images(repertoire_entree, fichier_sortie, nombre_de_division=2):
    images = []
    masks = []
    nombre_de_colone = nombre_de_division
    nombre_de_fichier = len([f for f in os.listdir(repertoire_entree) if os.path.isfile(os.path.join(repertoire_entree, f))])

    nombre_de_fichier_par_division = nombre_de_fichier // nombre_de_colone
    if nombre_de_fichier < nombre_de_colone:
        nombre_de_colone = nombre_de_fichier - 1
    while nombre_de_fichier_par_division * nombre_de_colone < nombre_de_fichier:
        nombre_de_colone += 1
        nombre_de_fichier_par_division = nombre_de_fichier // nombre_de_colone

    for fichier in os.listdir(repertoire_entree):
        if fichier.endswith(".png"):
            chemin_image = os.path.join(repertoire_entree, fichier)
            image = Image.open(chemin_image).convert('RGBA')
            images.append(image)
            mask = image.split()[3]
            masks.append(mask)

    largeur_totale = sum(img.width for img in images) // nombre_de_colone + nombre_de_fichier_par_division * 100
    hauteur_totale = max(img.height for img in images) * nombre_de_colone

    image_fusionnee = Image.new('RGBA', (largeur_totale, hauteur_totale), (0, 0, 0, 0))

    position_x = 0
    position_y = 0
    compteur = 0
    for img, mask in zip(images, masks):
        image_fusionnee.paste(img, (position_x, position_y), mask)
        position_x += img.width + 100
        compteur += 1
        if compteur == nombre_de_fichier_par_division:
            position_x = 0
            position_y += img.height
            compteur = 0

    image_fusionnee.save(fichier_sortie)
    print(f"Fusion réussie. Image enregistrée sous {fichier_sortie}")
    print(f"{nombre_de_fichier_par_division}*{nombre_de_colone} = {nombre_de_fichier} images au total")

# ----------------Exemple d'utilisation----------------

# repertoire_entree = "map/Isometric/wall"
# fichier_sortie = "map/Isometric/wall.png"

# fusionner_images(repertoire_entree, fichier_sortie, 5)

