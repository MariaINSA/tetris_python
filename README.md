# Tetris en Python
Ce projet contiendra une version de Tetris utilisant la bibliothèque Tkinter en Python.

Ce Tetris suivra le système de rotation SRS. Pour le comprendre, cette [vidéo](https://www.youtube.com/watch?v=dgt1kWq2_7c) l’explique assez bien.

De plus, les timings et les directives générales seront basés sur le [Tetris Design Guideline](https://dn720004.ca.archive.org/0/items/2009-tetris-variant-concepts_202201/2009%20Tetris%20Design%20Guideline.pdf).


## Comment jouer
Débloquer Majus pour jouer, sinon il ne reconnaîtra pas les entrées.
- **Flèche gauche** : déplacer la pièce vers la gauche  
- **Flèche droite** : déplacer la pièce vers la droite  
- **Flèche vers le bas** : accélérer la chute de la pièce  
- **Espace** : faire tomber la pièce
- **Touche c** : mettre une pièce de côté pour l’utiliser plus tard
- **Touche z** : faire tourner la pièce dans le sens inverse des aiguilles d’une montre  
- **Touche x** : faire tourner la pièce dans le sens des aiguilles d’une montre  
- **Touche d'entrée** : mettre le jeu en pause  
- **Objectif** : compléter des lignes horizontales sans laisser d’espace vide. Chaque ligne complétée disparaît et rapporte des points.


## Cahier de charges

| Tâche          | Responsable      | Début       | Fin         |
|------------------------|----------------|------------|-----------|
| Analyse du projet       | Fatma et Maria | 09-10-2025 | 23-10-2025 |
| Conception fonctionnelle| Fatma       | 23-10-2025 | 30-11-2025 |
| Partie Graphique  | Fatma         | 30-10-2025 | 20-11-2025 |
| Partie Logique  | Maria          | 30-11-2025 | 20-11-2025 |
| Integration     | Fatma et Maria        | 20-11-2025 | 4-12-2025 |
| Documentation     | Maria | 4-12-2025 | 18-12-2025 |

## Classes
### 1. Logique:
#### **__1.1. Game Logic:__**
La classe Game_logic gère toutes les règles et le fonctionnement interne du jeu Tetris : déplacements des pièces, gestion du temps, score, niveaux, hold, pause et fin de partie.

**__Attributs:__**
- grid_logic : grille logique du jeu
- graphic / canvas : éléments graphiques
- block / current_block : pièce actuellement contrôlée
- block_list / next_block_list : sacs de pièces
- score, lines_cleared, level : progression du joueur
- falling_speed, timers : gestion du temps et de la gravité
- hold_block / hold_state : système de pièce en réserve

**__Méthodes:__**
- init_game() : réinitialise complètement la partie
- falling_mov() : fait tomber la pièce automatiquement
- update_game() : applique les déplacements, rotations et hard drop
- place_block() : verrouille la pièce et traite les lignes complètes
- hold() : gère la mécanique de hold
- pause_game() / game_over() : contrôle l’état du jeu
- update_image() : synchronise logique et affichage

#### **__1.2. Block:__**
La classe Block représente une pièce de Tetris en chute et gère toutes ses interactions avec la grille : déplacements, rotations, collisions et verrouillage.

**__Attributs:__**
- block_type : type de la pièce (I, J, L, O, S, T, Z)
- rotation : état de rotation actuel (0 à 3)
- block : matrice de la pièce selon son type et sa rotation
- position : position actuelle de la pièce dans la grille

**__Méthodes:__**
- update_block_position() : applique un déplacement, une rotation ou un hard drop
- hard_drop() : fait tomber instantanément la pièce jusqu’en bas
- move_validation() : vérifie les collisions et les limites de la grille
- check_block_under() : détecte si la pièce touche le sol ou un autre bloc
- check_game_over() : détermine si une nouvelle pièce provoque la fin de partie

#### **__1.3. Grid:__**
La classe Grid gère la grille logique du jeu Tetris : elle stocke les blocs placés, calcule la position de l’ombre (ghost piece), détecte les lignes complètes et les supprime.

**__Attributs:__**
- grid : matrice principale contenant les blocs fixés
- shadow_grid : matrice temporaire incluant la pièce active et son ombre
- cols / rows : dimensions internes de la grille (avec bordures)

**__Méthodes:__**
- update_shadow() : met à jour l’ombre et la pièce en cours
- update_grid() : valide l’état courant dans la grille principale
- check_full_lines() : détecte et supprime les lignes pleines
- clear_full_lines() : décale la grille vers le bas après suppression
- delete() : réinitialise complètement la grille



### 2. Graphique:
#### **__2.1. Screen Manager:__**
La classe ScreenManager est la fenêtre principale de l’application et gère la navigation entre tous les écrans du jeu (menus, jeu, pause, scores).

**__Attributs:__**
- frames : dictionnaire contenant tous les écrans de l’application
- title_font : police utilisée pour les titres
- container : frame parent dans laquelle les écrans sont empilés

**__Méthodes:__**
- show_frame() : affiche un écran donné et déclenche les actions associées (démarrer une partie, charger les scores)
- game_over() : relai pour déclencher la fin de partie depuis d’autres écrans

#### **__2.2. Keyboard:__**
La classe KeyBoard gère tous les événements clavier du jeu Tetris et transmet les actions à la logique du jeu.

**__Attributs:__**
- game : référence à l’objet Game_logic
- paused : indique si le jeu est en pause

**__Méthodes:__**
- move_left / move_right : déplacement horizontal de la pièce-
- rotate_left / rotate_right : rotation de la pièce
- hard_drop : fait tomber instantanément la pièce
- hold_block : met la pièce en réserve ou échange avec celle en hold
- start_soft_drop / stop_soft_drop : activation / désactivation de la descente rapide
- pause_game : met le jeu en pause ou le reprend

#### **__2.3. Block:__**
La classe Block affiche une pièce de Tetris centrée dans un canvas Tkinter, généralement utilisée pour montrer la pièce suivante ou la pièce en réserve (hold).

**__Attributs:__**
- cell_size : taille d’une case de la pièce en pixels
- padding : espace entre les cases pour un effet visuel
- colors : liste des couleurs des pièces
- canvas : zone graphique où la pièce est dessinée
- blocks : liste des rectangles actuellement affichés

**__Méthodes:__**
- clear() : efface la pièce actuellement affichée
- update(block_number) : dessine une nouvelle pièce à partir de son index, la centre dans le canvas et applique la bonne couleur

#### **__2.4. Grid:__**
La classe Grid représente la grille principale du jeu Tetris et affiche l’état du plateau à partir de la grille logique.

**__Attributs:__**
- colors : palette de couleurs des cellules
- rectangles : matrice contenant les identifiants des rectangles du canvas
- canvas : zone graphique où la grille est dessinée

**__Méthodes:__**
- init : crée la grille graphique en fonction de la grille logique et initialise toutes les cellules
- update(lgrid) : met à jour les couleurs des cellules selon l’état actuel du jeu


#### **__2.5. MainMenu:__**
La classe MainMenu représente l’écran principal du jeu Tetris, affichant le fond, le titre et les boutons de navigation.

**__Attributs:__**
- controller : référence au ScreenManager pour changer d’écran
- bg_label : label affichant l’image de fond
- title_label : label du titre du jeu
- btn_play / btn_scores / btn_quit : boutons pour jouer, voir les scores et quitter

**__Méthodes:__**
- start_game() : ouvre une boîte de dialogue pour entrer le nom du joueur et démarre le jeu
- open_options() : ouvre une fenêtre d’options (actuellement un placeholder)

#### **__2.6. HighScores:__**
La classe HighScores représente l’écran affichant les meilleurs scores du jeu Tetris. Elle lit, trie et affiche les scores, et permet de revenir au menu principal.

**__Attributs:__**
- controller : référence au ScreenManager pour changer d’écran
- csv_file : fichier texte où sont sauvegardés les scores
- scores_container : frame qui contient les widgets représentant les scores

**__Méthodes:__**
- load_and_display_scores() : lit, trie et affiche les 10 meilleurs scores
- display_scores(scores) : affiche les scores passés en paramètre dans la grille graphique
- read_scores() : lit le fichier de scores et retourne une liste de dictionnaires
- remove_duplicates(scores) : supprime les doublons dans la liste de scores
- save_scores(scores) : sauvegarde la liste de scores dans le fichier CSV


#### **__2.7. MiddleMenu:__**
La classe MiddleMenu affiche un menu intermédiaire lors de la pause ou après une partie terminée. Elle contient un titre et des boutons pour reprendre/rejouer ou revenir au menu principal.

**__Attributs:__**
- controller : référence au ScreenManager pour changer d’écran
- pause : booléen indiquant si le menu est une pause (True) ou une fin de partie (False)

**__Méthodes:__**
- init() : initialise le menu avec titre et boutons
- quit_to_menu() : retourne au menu principal et, si pause, déclenche game_over()


#### **__2.8. NameDialog:__**
La classe NameDialog est une boîte de dialogue modale qui permet au joueur de saisir son nom avant de commencer une partie.

**__Attributs:__**
- result : chaîne de caractères contenant le nom saisi, None si annulé
- entry : champ de saisie pour le nom

**__Méthodes:__**
- init() : initialise la fenêtre modale, les boutons et le champ de saisie
- center_window(parent) : centre la boîte de dialogue par rapport à la fenêtre parente
- validate() : vérifie que le nom est alphanumérique et de 1 à 7 caractères, puis ferme la fenêtre
- cancel() : ferme la boîte de dialogue sans enregistrer le nom

#### **__2.8. PlayScreen:__**
La classe PlayScreen représente l’écran principal du jeu Tetris. Elle affiche la grille de jeu, la pièce en hold, la file des prochaines pièces, et les statistiques du joueur (score, lignes, niveau, nom).

**__Attributs:__**
- controller : référence au ScreenManager pour changer d’écran
- lgrid : instance de la logique de la grille de jeu (Grid)
- grid_frame : interface graphique de la grille (ggrid.Grid)
- hold_canvas : affichage de la pièce en hold (block.Block)
- next_canvases : liste des affichages des prochaines pièces (block.Block)
- name_var, score_var, lines_var, level_var : variables pour les statistiques
- game : instance de la logique du jeu (Game_logic)
- k_events : gestionnaire clavier (KeyBoard)

**__Méthodes:__**

- update_hold(block) : met à jour l’affichage de la pièce en hold
- update_next(next_list1, next_list2, position) : met à jour la file des prochaines pièces
- update_text(lines, score, level, name) : met à jour les statistiques affichées
- open_new_screen(screen) : demande au contrôleur d’afficher un autre écran
- game_over_int() : déclenche la routine de fin de partie dans la logique du jeu