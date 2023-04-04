import argparse

class Interface(argparse.ArgumentParser):
    """
    Reconnaissance et distribution des arguments passés en ligne de commande lors de l'appel du programme.
    """

    def __init__(self) -> None:
        """
        Constructeur de la classe.
        """

        super().__init__()

        self.add_argument( "--facet",
                           nargs="?",
                           default=1,
                           dest="facet",
                           required=False,
                           type=int,
                           help="Index of the facet, default : 1" )
        
        self.add_argument( "--coords",
                           nargs="?",
                           default="x z",
                           dest="coords",
                           required=False,
                           type=str,
                           help="Coordinate names, default : 'x z'." )
        
        self.add_argument( "--fields",
                           nargs="?",
                           default="d e j Peierls Work",
                           dest="fields",
                           required=False,
                           type=str,
                           help="Field names, default : 'd e s Peierls'." )
        
        self.add_argument( "-W", "--work",
                           nargs="?", 
                           default=False,
                           dest="bwork",
                           required=False,
                           type=bool,
                           help="Computes the absolute work if set to True (1), default : 0")
        
        self.add_argument( "--exp",
                           dest="expin",
                           required=True,
                           type=str,
                           help="List of absolute paths of the folders containing the .csv files of each experiment." )
        
        self.add_argument( "--sim",
                           dest="simin",
                           required=True,
                           type=str,
                           help="List of absolute paths of the folders of each simulation to analyse as a bulk." )
        
        self.add_argument( "-O", "--outfolder",
                           nargs="?",
                           default="out/",
                           dest="out",
                           required=False,
                           type=str,
                           help="Folder that should store the result of the session, default : './out/'")
        
        self.args = self.parse_args()

        self.coords    = self.args.coords.split(" ")    # Liste de str contenant les noms des coordonnées
        self.facet     = self.args.facet                # Entier naturel indexant la facette d'intérêt
        self.fields    = self.args.fields.split(" ")    # Liste de str contenant les noms des champs
        self.bwork     = self.args.bwork                # Booléen pour décider si le calcul du travail (produit e x s) doit être post-traité
        self.expin     = self.args.expin                # Liste de str contenant les chemins absolus de dossiers contenant des expériences (fichiers .csv)
        self.simin     = self.args.simin                # Liste de str contenant les chemins absolus de dossiers contenant des simulations (couple (Tfile, Pfile))
        self.outfolder = self.args.out                  # Chaîne de caractère vers un emplacement accessible en écriture pour l'utilisateur.

        return
