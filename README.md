# Forza 4 con PyGame

Forza 4 è una versione del celebre gioco da tavolo costruita utilizzando Python e la libreria PyGame. Questo progetto include diverse funzionalità, tra cui una modalità a giocatore singolo con livelli di difficoltà variabili e un'interfaccia utente grafica semplice e intuitiva.

## Caratteristiche principali

- **Livelli di difficoltà**: Seleziona tra 4 livelli di difficoltà per sfidare l'intelligenza artificiale:
  - Easy
  - Medium
  - Hard
  - Champion
- **Intelligenza Artificiale (IA)**: L'IA è costruita con tecniche come Minimax, valutazioni euristiche e simulazioni casuali per simulare il gioco di un avversario umano.
- **Grafica intuitiva**: Una griglia colorata che permette di visualizzare facilmente lo stato di gioco.
- **Istruzioni di gioco**: Mostrate nella schermata di selezione della difficoltà per aiutare i nuovi giocatori a iniziare rapidamente.
- **Feedback visivo**: Il cursore e la griglia facilitano il controllo e la visualizzazione della mossa corrente.
- **Effetto di attesa per il computer**: Durante il turno del computer, viene mostrato un messaggio per indicare che l'IA sta elaborando la mossa.

## Requisiti

Per eseguire il gioco, assicurati di avere installato Python 3.x e la libreria PyGame. Puoi installare PyGame con il seguente comando:

```
pip install pygame
```

## Come giocare

Avvio del gioco: Esegui il file principale (main.py o il file Python contenente il codice) per avviare il gioco.

```
python main.py
```

Selezione della difficoltà: All'avvio, potrai scegliere il livello di difficoltà tra:

Easy
Medium
Hard
Champion
Basta cliccare con il mouse su uno dei pulsanti per iniziare il gioco.

### Controlli di gioco

Usa le frecce destra e sinistra per muovere il cursore.
Premi la freccia giù per far cadere la pedina nella colonna selezionata.
Vittoria o sconfitta: Il gioco termina quando uno dei giocatori riesce a mettere in fila quattro pedine dello stesso colore in orizzontale, verticale o diagonale. Se non ci sono più mosse disponibili e nessuno ha vinto, la partita termina in pareggio.

### Logica dell'IA
Easy: L'IA seleziona casualmente una colonna disponibile.
Medium: L'IA cerca di bloccare le mosse vincenti dell'avversario, ma non usa una strategia avanzata.
Hard: L'IA utilizza l'algoritmo Minimax con una profondità limitata per prendere decisioni ottimali.
Champion: L'IA effettua simulazioni e analisi approfondite per trovare la mossa migliore in base alla situazione della partita.
Struttura del codice

### Funzioni principali
draw_grid(): Disegna la griglia di gioco.
draw_piece(row, col, color): Disegna una pedina nella posizione specificata.
drop_piece(grid, col, color): Fa cadere una pedina nella colonna selezionata, aggiornando la griglia.
check_win(grid, color): Verifica se un giocatore ha vinto controllando quattro pedine consecutive.
ai_move_easy(grid), ai_move_medium(grid), ai_move_hard(grid), ai_move_champion(grid): Funzioni che gestiscono le mosse dell'intelligenza artificiale a seconda del livello di difficoltà.
show_difficulty_screen(): Mostra la schermata iniziale per selezionare il livello di difficoltà.
Modalità IA

### Possibili miglioramenti futuri
Alcune idee per le future versioni:

Modalità multiplayer locale
Supporto per una modalità online
Aggiunta di effetti sonori e animazioni più complesse
Miglioramenti grafici e personalizzazioni delle pedine
Ringraziamenti
Questo progetto è stato sviluppato da Andrea Palladino. Un ringraziamento speciale va a ChatGPT-4 per l'aiuto nella scrittura del codice e la progettazione dell'intelligenza artificiale del gioco.

### Licenza
Questo progetto è open-source e disponibile sotto la licenza Creative Commons.
