# Assurez-vous d'être dans le répertoire où se trouve votre fichier install.txt
# Installez les dépendances Python en utilisant le fichier install.txt

pip install -r install.txt

# Déplacer vous dans le répertoire du Makefile 

cd anonym_meth

# Executez le Makefile 

make

# Executez le fichier launch.py en précisant les 3 arguments

python3 launch.py <dossierEntree> <dossierSortie> <dossierAnonyme>

## dossierEntree = "../data/multivariate/";
## dossierSortie = "../data/CSV_output/"; 
## dossierAnonyme = "../gener_simulated_data_meth/";

python3 launch.py ../data/multivariate/ ../data/CSV_output/ ../gener_simulated_data_meth/


# Choix pour l'execution des tests statistiques 

Voulez-vous effectuer des tests stats ? (O/n): O

# Choix de la sélection des paramètres

Voulez-vous passer par une interface graphique ? (O/n): O

# Une interface graphique va apparaitre vous laissant le choix de plusieurs paramètres

## dossier patients réels : "../data/CSV_output/"
## dossier patients anonymes : "../gener_simulated_data_meth/"
## dossier de sortie : "../analyse_anonym_meth/" ou sélectionner un autre dossier avec l'explorateur de fichiers via le bouton [PARCOURIR]
## Taille de l'échantillon pour calcul des distances : sélecion entre 1 et 20
## Nombre total de patients anonymes : sélection entre 1 et 1000

# Si vous êtes sur un serveur et que vous ne pouvez pas afficher d'interface 

système d'arguments ou de fichier texte pour renseigner les paramètres