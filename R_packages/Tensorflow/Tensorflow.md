Title : Tenserflow
author: Nicolas Allix & Marko Arsic

# Tenserflow

## Introduction

### L'installation :
TensorFlow est une plate-forme d'apprentissage automatisé open source de bout en bout. Il fournit un écosystème complet et flexible d'outils, de bibliothèques et de ressources communautaires, permettant aux chercheurs de progresser dans le domaine de l'apprentissage automatisé, et les développeurs peuvent facilement créer et déployer des applications qui utilisent la technologie. TensorFlow a été initié par Google en 2011, et est doté d'une interface pour Python, Julia et R.

TensorFlow utilise un écosystème complet de machine learning pour résoudre des problèmes complexes.

L’une des particularités de TensorFlow est l’utilisation des graphes de flux de données aussi appelé data flow graphs.

L’interface TensorFlow se compose de nœuds qui représente des calculs matématiques et de tenseurs (les arêtes du graph). Un tenseur peut être un entier, un vecteur, une image… Chaque nœud du graphe prend donc en entrée différents tenseurs, effectue son calcul, puis retourne de nouveaux tenseurs.

## Les avantages de TensorFlow

### Créer des modèles avec des API :

TensorFlow fournit différents niveaux d'abstraction. Il suffit de choisir le niveau
Tout d'abord, installez le package tensorflow R de GitHub : 

> install.packages("tensorflow")

Ensuite, utilisez la fonction install_tensorflow() pour installer TensorFlow. Sous Windows, il faut disposer d'une installation fonctionnelle d'Anaconda.
>library(tensorflow)

>install_tensorflow()

Pour vérifier que l'installation a bien fonctionné :

>library(tensorflow)

>tf$constant("Hellow Tensorflow")

## tf.Tensor(b'Hellow Tensorflow', shape=(), dtype=string)

Vous disposerez ainsi d'une installation par défaut de TensorFlow adaptée à l'utilisation du paquet tensorflow R.

retrouver la documentation ici : https://tensorflow.rstudio.com/guide/


Source :
https://www.tensorflow.org/?hl=fr
https://www.margo-group.com/fr/actualite/introduction-a-tensorflow-datalab-de-google-cloud-platform/
