#IMPORT
from keras.models import load_model
from PIL import Image
import numpy as np
import time
import os
from flask import Flask, request,  jsonify

# On definit les chemins d'acces au différentes hyper parametre


# Classe permettant de realiser une prediction sur une nouvelle donnee



 
app = Flask(__name__)

@app.route('/')
def index():
    return 'Server Works!'

@app.route('/IA_flowers/' , methods=['POST'])
def predict():
    """
    # Fonction qui permet de convertir une image en array, de charger le modele et de lui injecter notre image pour une prediction
    :param modelPath: chemin du modele au format hdf5
    :param imagePath: chemin de l image pour realiser une prediction
    :param imageSize: défini la taille de l image. IMPORTANT : doit être de la même taille que celle des images
    du dataset d'entrainements
    :param label: nom de nos 5 classes de sortie
    """
    
    path = os.getcwd()
    image = request.files['image']
    modelPath = path + '/Model/moModel2.hdf5'
    #imagePath =  path + '/image/tulipe.jpg'
    imageSize = (50,50)
    label = ['dahlia', 'marguerite', 'pissenlit', 'rose', 'tournesol', 'tulipe']

    start = time.time()

    # Chargement du modele
    print("Chargement du modele :\n")
    model = load_model(modelPath)
    print("\nModel charge.")

    #Chargement de notre image et traitement
    data = []
    img = Image.open(image)
    img.load()
    img = img.resize(size=imageSize)
    img = np.asarray(img) / 255.
    data.append(img)
    data = np.asarray(data)

    #On reshape pour correspondre aux dimensions de notre modele
    # Arg1 : correspond au nombre d'image que on injecte
    # Arg2 : correspond a la largeur de l image
    # Arg3 : correspond a la hauteur de l image
    # Arg4 : correspond au nombre de canaux de l image (1 grayscale, 3 couleurs)
    
    dimension = data[0].shape

    #Reshape pour passer de 3 à 4 dimension pour notre reseau
    data = data.astype(np.float32).reshape(data.shape[0], dimension[0], dimension[1], dimension[2])

    #On realise une prediction
    prediction = model.predict(data)


    #On recupere le numero de label qui a la plus haut prediction
    maxPredict = np.argmax(prediction)

    #On recupere le mot correspondant à l indice precedent
    word = label[maxPredict]
    pred = int(prediction[0][maxPredict] * 100.)
    prediction = str(pred)+ ' %'
    DataFleur  = get_flower_data(word)
    datafleurs = [prediction]
    
    for t in DataFleur : 
        datafleurs.extend(t)
        
    print(datafleurs)
    #fonction de la recuperation des data de la fleur



  
    return datafleurs
import sqlite3

def get_flower_data(flower_name):
    conn = sqlite3.connect('fleurs.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Plante WHERE Nom_Plante = ?", (flower_name,))
    flower_data = c.fetchall()
    conn.close()
    return flower_data
# Afficher les annonce
@app.route('/Annonce/', methods=['POST'])
def viewAnnonce():
    conn = sqlite3.connect('fleurs.db')
    c = conn.cursor()
    c.execute("SELECT * FROM annonce")
    annonce_data = c.fetchall()
    conn.close()
    return jsonify(annonce_data)

# ajouter une annonce
@app.route('/Ajouter/', methods=['POST'])
def addAnnonce():
    annonce_data = request.json # Récupère les données envoyées dans la requête HTTP POST sous forme de JSON
    conn = sqlite3.connect('fleurs.db')
    c = conn.cursor()
    c.execute("INSERT INTO annonce(Titre_Annonce, Description_Annonce, Adresse1_Annonce, DatePub_Annonce, Lat_Annonce, Long_Annonce) VALUES (?, ?, ?,?,?,?)", (annonce_data['Titre_Annonce'], annonce_data['Description_Annonce'], annonce_data['Adresse1_Annonce'],annonce_data['DatePub_Annonce'], annonce_data['Lat_Annonce'], annonce_data['Long_Annonce']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Annonce ajoutée avec succès !'})

    
if __name__ == '__main__':
      app.run(host='0.0.0.0', port='3400',debug=True)
