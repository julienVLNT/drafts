import adelio            as io
import matplotlib.pyplot as plt
import numpy             as np
import os

class Simulation():
    """
    Simulation numérique réalisée à l'aide du logiciel ADELI.
    """

    def __init__(self, outfolder: str, infolder: str, coords: list, fields: list, bwork: bool) -> None:
        """
        Constructeur.
        
        Parametres
        ----------
        outfolder : str
                    Chemin absolu vers le dossier de sortie de la session d'analyse
        infolder  : str
                    Chemin absolu vers le dossier contenant les fichiers T et P de la simulation.
        coords    : list(str)
                    Noms des coordonnées des noeuds à lire, ["x", "z"] pour les facettes 1 ou 3 c.f 02_Pfile.ipynb.
        fields    : list(str)
                    Noms des champs à lire, par exemple ["d", "e", "s", "Peierls"]
        bwork     : bool
                    Interrupteur de calcul et de post-traitement du travail.
               
        Retour
        ------
        """
        # Gestion des chemins
        self.basepath = infolder
        self.ppath    = os.path.join(self.basepath, "".join([filename for filename in os.listdir(self.basepath) if filename.startswith("p")]))
        self.tpath    = os.path.join(self.basepath, "".join([filename for filename in os.listdir(self.basepath) if filename.startswith("t")]))

        # Préparation du dossier de sortie de l'analyse : "outfolder/simulations/singles/nom_de_la_simulation"
        self.__prepare_tree(outfolder)

        # Déclaration des objets T et P de la simulation
        self.tfile = io.Tfile(self.tpath)
        self.pfile = io.Pfile(self.ppath)

        # Lecture des dates de sortie de la simulation
        self.dates  = self.tfile.read()
        self.idates = list(range(len(self.dates)))

        # Lecture de tous les champs du fichier `p`
        self.fields = self.pfile.read_fields(self.idates, self.pfile.fields)

        return
    

    def __prepare_tree(self, outfolder: str) -> None:
        """
        Prépare le sous-dossier de l'analyse de la simulation
        
        Parametres
        ----------
        outfolder : str
                    Chemin de sortie de la session d'analyse
                    
        Retours
        -------
        """
        simpath = os.path.join(outfolder, "simulations", "singles", self.basepath.split("/")[-1])
        os.makedirs(simpath, exist_ok=True)
        return



class Group():
    """
    Groupe de simulation avec sa méthode d'analyse propre.
    """

    def __init__(self, outfolder: str, paths: list, coords: list, fields: list, work: bool) -> None:
        """
        Constructeur.
        
        Parametres
        ----------
        outfolder : str
                    Chemin du dossier de sortie de la session d'analyse
        paths     : list(str)
                    Chemins absolus vers les dossiers contenant les simulations (fichiers T et P).
        fields    : list(str)
                    Noms des champs à post-traiter
        coords    : list(str)
                    Noms des coordonnées à extraire, en général ['x', 'z']
        work      : bool
                    Activer le calcul et le post-traitement du travail.
        
        Retour
        ------
        """
        self.__prepare_tree(outfolder)

        self.coords = coords
        self.fields = fields
        self.bwork  = work

        self.simulations = []
        for path in paths:
            self.simulations.append(Simulation(path, outfolder, self.coords, self.fields, self.bwork))
        return
    

    def __prepare_tree(self, outfolder: str):
        """
        Prépare les sous-dossiers de l'analyse : outfolder/singles et outfolder/group

        Parametres
        ----------
        outfolder : str
                    Chemin racine de l'exécution de la session

        Retour
        ------
        """
        os.makedirs(os.path.join(outfolder, "simulations", "singles"), exist_ok=True)
        os.makedirs(os.path.join(outfolder, "simulations", "groups"), exist_ok=True)
        return
