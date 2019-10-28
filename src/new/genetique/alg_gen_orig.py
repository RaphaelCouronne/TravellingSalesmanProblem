from common import *
from pylab import *


### Génération d'une population aléatoire ###

def Indices_Alea(n) :
    """ renvoie une liste [sigma(1),...sigma(n-1)] avec sigma aléatoire"""
    Liste_Indices=[k+1 for k in range(n-1)]
    Liste_Alea=[]
    for i in range(n-1) :
        Indice_Alea=randint(0,n-1-i)
        Liste_Alea.append(Liste_Indices[Indice_Alea])
        Liste_Indices.remove(Liste_Indices[Indice_Alea]) # on gère une file d'attente !
    return Liste_Alea

#print(Indices_Alea(6)) # test OK

def Individu_Alea(Liste_Sommets) :
    """ renvoie une trajectoire - cycle hamiltonien - aléatoire"""
    n=len(Liste_Sommets)
    return [Liste_Sommets[0]]+[Liste_Sommets[k] for k in Indices_Alea(n)]

#print(Individu_Alea([[1,2],[6,4],[9,0],[7,8],[8,2],[6,-7]]))

def Generation_Pop_Alea(Liste_Sommets,p) :
    """ génère p individus aléatoireement """
    return [Individu_Alea(Liste_Sommets) for k in range(p)]

#print(Generation_Pop_Alea(['a','b','c','d'],10)) # test OK
Population=Generation_Pop_Alea([[1,2],[5,4],[6,2],[3,2],[5,3],[1,6]],3)
#print(Population) # test OK

def Individu_Plus_Courts_Trajets(Liste_Sommets,i) :
    """détermine à partir du sommet i un cycle hamiltonien en cherchant les sommets plus proches """
    Sommets=Liste_Sommets.copy()
    Liste_Temp=[Sommets[i]]
    Sommets.remove(Sommets[i]) # on gère une file d'attente
    
    while Sommets!= [] :
        Distance_Mini,Ville_Mini=Poids_Arete(Sommets[0],Liste_Temp[-1]),Sommets[0]
        for Ville in Sommets[1:] :
            Poids_Temp=Poids_Arete(Ville,Liste_Temp[-1])
            if Poids_Temp<Distance_Mini :
                Distance_Mini,Ville_Mini=Poids_Temp,Ville
        Liste_Temp.append(Ville_Mini)
        Sommets.remove(Ville_Mini)
    # il faut maintenant effectuer le cycle sur Liste_Temp pour commencer à Sommets[0]
    for k in range(len(Liste_Temp)) :
        if Liste_Temp[k]==Liste_Sommets[0] :
            break
    return Liste_Temp[k:]+Liste_Temp[:k]
                
def Generation_Pop_Semi_Alea(Liste_Sommets,p) :
    """ génère une population semi-aléatoire """
    return [Individu_Alea(Liste_Sommets) for k in range(p//2)]+[Individu_Plus_Courts_Trajets(Liste_Sommets,randint(0,len(Liste_Sommets)-1))  for k in range(p//2)]

### Construction de la fonction d'adaptation d'un individu à son environnement ###

def Poids_Arete(M,N):
    """ calcule le poids associé à l'arête  {M,N} """
    return sqrt((M[0]-N[0])**2+(M[1]-N[1])**2)


def Adaptation_Individu(Individu) :
    """ calcule la fonction d'adaptation correspondant  à un individu <-> cycle hamiltonien """
    n = len(Individu)
    Adapt_Temp=0
    for k in range(n-1) :
        Adapt_Temp+=Poids_Arete(Individu[k],Individu[k+1])
    return Adapt_Temp+Poids_Arete(Individu[-1],Individu[0]) # pour boucler le cycle

#print(Adaptation_Individu([[1,2],[6,4],[9,0]])) # test OK

### Hybridations, mutations ###

def Hybridation(Individu1,Individu2,i) :
    """ renvoie à partir de deux individus <-> cycles hamiltoniens deux autres individus après un cross-over des chromosomes à l'allèle i avec i compris entre 2 et n-1"""
    Liste1,Liste2=Individu1.copy(),Individu2.copy()
    n=len(Liste1)
    return [Liste1[:i]+[x for x in Liste2 if Liste1[:i].count(x)==0],
    Liste2[:i]+[x for x in Liste1 if Liste2[:i].count(x)==0]]

Individu1=list(range(10))
Individu2=[0,4,1,6,3,9,8,2,5,7]  
print(Individu1,Individu2)
print(Hybridation(Individu1,Individu2,9)) #test OK

def Hybridation_Alea(Individu1,Individu2):
    """ modélise une hybridation aléatoire entre deux individus"""
    n=len(Individu1)
    i=randint(2,n-2)  # i=1 ou i=n n'engendre pas d'hybridation effective
    return Hybridation(Individu1,Individu2,i)

#print(Hybridation_Alea(Individu1,Individu2)) # test OK

def Mutation(Individu,k,l) :
    """ mute l'individu en modifiant les indices k,k+1,...,l-1,l en l,l-1,...,k+1,k en partant de 1<=k<l<n"""
    if l-1==k :
        return Individu[:k]+[Individu[k+1],Individu[k]]+Individu[k+2:]
    elif l-2==k :
        return Individu[:k]+[Individu[k+2],Individu[k+1],Individu[k]]+Individu[k+3:]
    
    else :
        return Individu[:k]+[Individu[l],Individu[l-1]]+Individu[k+2:l-1]+[Individu[k+1],Individu[k]]+Individu[l+1:]

Individu=list('abcdefg'+'124356')
#print(Individu)
#print(Mutation(Individu,1,12)) # tests OK

def Mutation_Alea(Individu) :
    """ modélise une mutation aléatoire """
    n=len(Individu)
    k=randint(1,n-2)
    l=randint(k+1,n-1)
    return Mutation(Individu,k,l)
    
#print(Individu)
#print(Mutation_Alea(Individu)) # test OK


 

### Sélection des individus ###

def Selection_Tournoi(Individu1,Individu2) :
    """ renvoie le vainqueur entre deux individus, en attribuant 85% de chance de viectoire pour le mieux adapté """
    if Adaptation_Individu(Individu1)<Adaptation_Individu(Individu2) :# individu 1 mieux adapté que 2
        Match=[Individu1.copy(),Individu2.copy()]
    else :
        Match=[Individu2.copy(),Individu1.copy()]
    #Match[0] mieux adapté que Match[1]
    x=uniform(0,1) # modélise la loi uniforme sur [0,1]
    if x<0.85 : #le mieux adapté gagne !!
        return Match[0]
    else :      #le moins adapté gagne !!!
        return Match[1]




#from common import * # sinon, randint(0,q-1) ne renvoie jamais q-1 ... bizarrement !



def Deux_Adversaires_Alea(Population) :
    """ renvoie un match entre deux adversaires d'une population """
    q=len(Population)
    Liste_Indices=list(range(q))
    k , l =randint(0 , q), randint(0,q-1) # k = numéro du premier candidat  ## en théorie randint(0,q-1) et randint(0,q-2)...
    Liste_Indices.remove(k) # pour ne pas choisir le même candidat
    m=Liste_Indices[l] # numéro du second candidat
    return [Population[k],Population[m]]

#Population = [0,1,2,3,4,5]
#for k in range(10) :
#    print(Deux_Adversaires_Alea(Population))  # tests OK

### Choix de la meilleur moitié d'une population et choix du meilleur 

def Meilleur_Moitie(Population) :
    """ ne retien que la moitié la plus adaptée à l'environnement """
    q=len(Population)
    Liste_Adaptation=[Adaptation_Individu(x) for x in Population]
    Liste_Adaptation.sort() # on classe dans l'ordre croissant
    Mediane=Liste_Adaptation[q//2]
    Liste_Meilleurs=[]
    for x in Population :
        if Adaptation_Individu(x)<Mediane :
            Liste_Meilleurs.append(x) # les meilleurs stricts sont placés à droite
        if Adaptation_Individu(x)==Mediane : 
            Liste_Meilleurs=[x]+Liste_Meilleurs # les ex-aequo de la médiane sont placés à gauche
    # on a peut-être compabilisé trop d'ex-aequo
    while len(Liste_Meilleurs)!=q//2 :
        Liste_Meilleurs.remove(Liste_Meilleurs[0]) # on élimine un individu de la médiane
    return Liste_Meilleurs
       
def Meilleur_Individu(Population) :
    " renvoie l'individu le mieux adapté dans une population """
    Min_Adaptation=min([Adaptation_Individu(x) for x in Population])
    for x in Population :
        if Adaptation_Individu(x)==Min_Adaptation :
            Meilleur=x
            break
    return Meilleur
        
### Construction de la génération suivante ###

def Generation_Suivante(Population) :
    """ génère la population à la génération suivante """
    q=len(Population)
    Population_Temp=[]
    for k in range(q) :
        Advers=Deux_Adversaires_Alea(Population)
        Population_Temp.append(Selection_Tournoi(Advers[0],Advers[1]))
    # Population_Temp = population des gagnants des matchs
    
    ## modélisation des hybridations sur cette Population_Temp
    # proba qu'une hypridation ait lieu entre deux chromosomes: 1/5
    
    for k in range(q-1) :
        for l in range(q-1-k) :
            x=uniform(0,1)
            if x<1/5 : #l'hybridation a lieu !!
                Individus_Hybr=Hybridation_Alea(Population_Temp[k],Population_Temp[k+l+1])
                Population_Temp[k],Population_Temp[k+l+1]=Individus_Hybr[0],Individus_Hybr[1]
                
                
    ## modélisation des mutations sur 
    # proba qu'une mutation ait lieu : 1/20
      
    for Individu in Population_Temp :
          x=uniform(0,1)
          if x<1/20 : # une mutation a lieu !!
                Individu=Mutation_Alea(Individu)
    
    ## choix des meilleurs individus de Population (génération g) (on en prend p//2) et des meilleurs individus de Population_Temp (génération g+1)(on en prend p//2)
    return Meilleur_Moitie(Population)+Meilleur_Moitie(Population_Temp)

Population=Generation_Pop_Alea([[1,2],[5,4],[6,2],[3,2],[5,3],[1,6]],4)
#print(Generation_Suivante(Population)) # pas d'erreur de syntaxe ...


### Choix des villes  et dessin - dimensions du canevas

largeur=1000
hauteur=500
n=30  # choix du nombre de villes

## Sommets en cercle
Liste_Sommets=[[largeur/2+200*cos(2*k*pi/n),hauteur/2+200*sin(2*k*pi/n)] for k in range(n)]
## Sommets en couronne
#Liste_Sommets=[[largeur/2+150*cos(2*k*pi/n),hauteur/2+150*sin(2*k*pi/n)] for k in range(n)]+[[largeur/2+230*cos(2*k*pi/n),hauteur/2+230*sin(2*k*pi/n)] for k in range(n)]
## Sommets sur trois cercles
#Liste_Sommets=[[largeur/2+150*cos(2*k*pi/n),hauteur/2+150*sin(2*k*pi/n)] for k in range(n)]+[[largeur/2+230*cos(2*k*pi/n),hauteur/2+230*sin(2*k*pi/n)] for k in range(n)]+[[largeur/2+50*cos(2*k*pi/n),hauteur/2+50*sin(2*k*pi/n)] for k in range(n)]
## Sommets sur trois cercles et une ellipse
#Liste_Sommets=[[largeur/2+150*cos(2*k*pi/n),hauteur/2+150*sin(2*k*pi/n)] for k in range(n)]+[[largeur/2+230*cos(2*k*pi/n),hauteur/2+230*sin(2*k*pi/n)] for k in range(n)]+[[largeur/2+50*cos(2*k*pi/n),hauteur/2+50*sin(2*k*pi/n)] for k in range(n)]+[[largeur/2+400*cos(2*k*pi/n),hauteur/2+75*sin(2*k*pi/n)] for k in range(n)]
Nbre_Gen=20 # nombre de générations à envisager lors du système dynamique

def Sommets_Graphe_Alea(n):
    global hauteur,largeur
    """ détermine les sommets aléatoires par la loi uniforme sur le canevas """
    return [[uniform(20,largeur-20),uniform(20,hauteur-20)] for k in range(n)]
    
## Sommets Aléatoires
#Liste_Sommets=Sommets_Graphe_Alea(n)
def Dessiner_Villes(Liste_Sommets):
    """ dessine les villes ponctuelles dans le canevas """
    for Ville in Liste_Sommets :
        canevas.create_rectangle(Ville[0]-2,Ville[1]-2,Ville[0]+2,Ville[1]+2,fill="black")
        
def Tracer_Chemins(Individu) :
    """ trace le cycle hamiltonien """
    canevas.delete(ALL)
    Dessiner_Villes(Liste_Sommets)
    for k in range(len(Individu)-1) :
        canevas.create_line(Individu[k][0],Individu[k][1],Individu[k+1][0],Individu[k+1][1],fill="red")
    canevas.create_line(Individu[-1][0],Individu[-1][1],Individu[0][0],Individu[0][1],fill="red")   # pour boucler la boucle
      
def Dynamique_Population(Nbre_Gen) :
    """ trace les meilleurs chemins sur Nbre_Gen générations """
    global Liste_Sommets
    
    p=30 # on raisonne sur des populations de p individus
    
    ## Choixi du type de population initiale
    Population=Generation_Pop_Alea(Liste_Sommets,p) # population de départ totalement aléatoire
    #Population=Generation_Pop_Semi_Alea(Liste_Sommets,p) # population de départ semi-aléatoire
    ##
    
    for k in range(Nbre_Gen)  :
        Tracer_Chemins(Meilleur_Individu(Population))
        Population=Generation_Suivante(Population)
        fenetre.after(200)
        fenetre.update()
        
        
### Interface Tkinter pour la visualisation du système dynamique ###

def go():
    global Nbre_Gen

    Dynamique_Population(Nbre_Gen)

from tkinter import * # pour l'interface graphique

fenetre = Tk()


#titre=Label(fenetre,text="Le Sudoku")
#titre.pack(side=TOP)

canevas = Canvas(fenetre, width =largeur, height =hauteur, bg ="#F5DA81")
canevas.pack( padx =5, pady =5)




bouton_quitter = Button(fenetre, text="Quitter", command=fenetre.quit)
bouton_quitter.pack(side=RIGHT)


#b2 = Button(fenetre, text ='Recommencer', command =recommencer)
#b2.pack(side=RIGHT, padx =5, pady =5)


b1 = Button(fenetre, text ='Go!', command =go)
b1.pack(side=RIGHT, padx =5, pady =5)


fenetre.mainloop()
fenetre.destroy()

