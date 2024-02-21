import random
from tkinter import *

# Coded in Spanish

# Dimensión básica
N = 9


filaActiva = 0
columnaActiva = 0

enRevision = False

bitacora = []

solucionExiste = True

juego = [
       [0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0]]

botones = [
       [0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0]]

keypad = [
        [1,2,3],
        [4,5,6],
        [7,8,9]]

keypad2 = [
        [0,0,0],
        [0,0,0],
        [0,0,0]]



# Imprime la matriz en la terminal
def printing(juego):
    for i in range(N):
        for j in range(N):
            print(juego[i][j], end = " ")

# Lee un archivo
# E: string con su ruta y nombre
# S: string con el nombre del archivo 
def leer(nombreArchivo):
    fo  = open(nombreArchivo, 'r')
    res = fo.read()
    fo.close()
    return res

# Función para actualizar matriz juego con los contenidos del archivo partidas.txt
def subirSudoku():
    global juego
    juego = eval(leer('partidas.txt'))
    print(juego)
    print("Respaldo")

# Función para guardar los contendiso de la matriz juego en el archivo bitacora.txt
def guardar():
    global juego
    global bitacora
    
    bitacora.append(juego)

    file = open("bitacora.txt", "w")
    file.write(str(bitacora))
        
# Verifica que un valor puede ser asignado en una casilla.
# Números del 1 al 9:
# 1. Distintos en un espacio 3x3
# 2. Distintos en una fila completa
# 3. Distintos en una columna completa

# E: tres listas (matriz, columna, fila) y un número
# S: un booleano
def isSafe(juego, row, col, num):
    for i in range(9):
        if juego[row][i] == num:
            return False
 
    for i in range(9):
        if juego[i][col] == num:
            return False
 
    startRow = row - row % 3
    startCol = col - col % 3
    for i in range(3):
        for j in range(3):
            if juego[i + startRow][j + startCol] == num:
                return False
    return True

# Llena un sudoku con números aleatorios válidos.
# E: una lista (matriz) y dos números (índice columna y fila)
# S: un booleano
def solveSudoku(juego, row, col):
    if (row == N - 1 and col == N):
        return True
       
    if col == N:
        row += 1
        col = 0
 
    if juego[row][col] > 0:
        return solveSudoku(juego, row, col + 1)
    
    for num in range(1, N + 1, 1):
        if isSafe(juego, row, col, num):
           
            juego[row][col] = num
 
            if solveSudoku(juego, row, col + 1):
                return True
        juego[row][col] = 0
    return False

# Genera la parte gráfica del sudoku.
def generarMatriz():
    for i in range(0,9):
        for j in range(0,9):
            btn = Button(mainFrame, 
                         bg="white", 
                         width = 7, 
                         height = 3, 
                         fg="#00425A", 
                         borderwidth=1, relief="solid",
                         command = lambda row=i, col=j: getCords(row, col))
            
            btn.grid(row=i, column=j)
            botones[i][j] = btn
            botones[i][j].config(font = "Helvetica 10 bold")

# Genera el teclado de números.
def generarKeypad():
    for i in range(0,3):
        for j in range(0,3):
            btn = Button(secondFrame,
                         bg="white", 
                         width = 10, 
                         height = 3, 
                         fg="#00425A", 
                         borderwidth=0, relief="solid",
                         command = lambda row=i, col=j: asignar(row, col))
            
            btn.grid(row=i, column=j)
            keypad2[i][j] = btn
            keypad2[i][j].config(font = "Helvetica 10 bold")

            keypad2[i][j].config(text = str(keypad[i][j]))


# Asigna el valor de los números de la matriz en el sudoku.
def pintarMatriz(num):
    global juego
    for i in range(0,9):
        for j in range(0,9):
            if random.randint(1,100) <= num:
                botones[i][j].config(text = str(juego[i][j]))
            else:
                botones[i][j].config(text = "")

# Genera una lista con 9 números distintos en orden aleatorio.
# Esta lista se usa para generar el resto de la matriz del sudoku.
def newGridStart():
    global juego
    for i in range(0, len(juego)):
        newLine = random.sample(range(1,10), 9)
        juego[0] = newLine
        
# Algoritmo para resolver sudoku aleatorio
def solve():
    global solucionExiste
    newGridStart()
    if (solveSudoku(juego, 0, 0)):
        solucionExiste = True
    else:
        solucionExiste = False
        
# Algoritmo para resolver sudoku cargado.
def solve2():
    global solucionExiste
    if (solveSudoku(juego, 0, 0)):
        solucionExiste = True
    else:
        solucionExiste = False

# Establece las casillas que serán cambiadas por el teclado de números
# E: dos números (fila y columna)
def getCords(row, col):
    global filaActiva
    global columnaActiva
    filaActiva = row
    columnaActiva = col

# Asigna los valores activos a valores en el sudoku.
# E: dos números (fila y columna)
def asignar(row, col):
    botones[filaActiva][columnaActiva].config(text = str(keypad[row][col]))

# Reinicia las casillas del sudoku.
def resetMatriz():
    global juego
    juego = [
       [0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0]]

# Establece dificultad fácil (muestra 65% de casillas)
def dificultadFacil():
    resetMatriz()
    generarMatriz()
    solve()
    pintarMatriz(65)
    lblMensaje.set("")

# Establece dificultad media (muestra 55% de casillas)
def dificultadMedia():
    resetMatriz()
    generarMatriz()
    solve()
    pintarMatriz(55)
    lblMensaje.set("")

# Establece dificultad difícil (muestra 45% de casillas)
def dificultadDificil():
    resetMatriz()
    generarMatriz()
    solve()
    pintarMatriz(45)
    lblMensaje.set("")

# Revela las casillas restantes o soluciona el sudoku.
def solucionarJuego():
    global juego
    for i in range(0,9):
        for j in range(0,9):
            botones[i][j].config(text = str(juego[i][j]))
    lblMensaje.set("")
    lblMensaje.set("Sudoku solucionado.")

    
# Borra el valor de una casilla en el sudoku.
def borrar():
    botones[filaActiva][columnaActiva].config(text = "")
    lblMensaje.set("")

# Función que carga una matriz del archivo partidas.txt
def cargar():
    resetMatriz()
    subirSudoku()
    solve2()
    generarMatriz()

    if solucionExiste == False:
        lblMensaje.set("¡El Sudoku no tiene solución!")
    else:
        pintarMatriz(55)
        lblMensaje.set("Sudoku cargado :)")

# Revisa que los valores de las casillas del sudoku coinciden con los valores de la matriz.
def revisarRespuestas():
    global enRevision
        
    if enRevision == False:    
        for i in range(0,9):
            for j in range(0,9):
                if botones[i][j].cget("text") != str(juego[i][j]):
                    botones[i][j].config(bg = "#FA9494") # Malo - Rojo
                else:
                    botones[i][j].config(bg = "#ADE792") # Bueno - Verde
        enRevision = True
    else:
        for i in range(0,9):
            for j in range(0,9):
                botones[i][j].config(bg = "white")
        enRevision = False
        



main = Tk()
main.title("Proyecto Programado II - Sudoku - Víctor Fung")
main.geometry("1000x820")

# Frames
mainFrame = Frame(main, bg = "#1C6758", highlightbackground = "#003865", highlightthickness=3)
secondFrame = Frame(main, bg = "#1C6758", highlightbackground = "#003865", highlightthickness=3)
thirdFrame = Frame(main, bg = "#9BABB8", highlightbackground = "#003865", highlightthickness=3, width = 300, height = 150)

mainFrame.place(x = 20, y = 40)
secondFrame.place(x=670, y= 100)
thirdFrame.place(x=20, y=740)


# Mensaje 
lblMensaje = StringVar()

# Labels
Label(main, text="Sudoku TEC",fg = "#3C486B", font=("Helvetica 18 bold")).place(x=670, y= 20)
Label(main, text="Víctor Andrés Fung Chiong - Proyecto Programado II",fg = "#3C486B", font=("Helvetica 9 bold")).place(x=670, y= 55)
Label(main, text="Nuevo Sudoku ",fg = "#3C486B", font=("Helvetica 15 bold")).place(x=20, y= 570)
Label(main, text="Opciones ",fg = "#3C486B", font=("Helvetica 15 bold")).place(x=20, y= 650)
Label(main, text= "", textvariable = lblMensaje, font = ("Helvetica 12 bold"), fg = "#CD1818").place(x = 20, y = 10)
Label(thirdFrame, text="Las partidas se guardan en el archivo bitacora.txt.\n Para cargar una partida, inserte una matriz en el \n archivo partidas.txt, la cual se subirá con dificultad media.", 
      font = ("Helvetica 11 bold"), bg = "#9BABB8", fg = "#003865").pack()

# Botones Dificultad
Button(main, text = "Fácil", command = dificultadFacil, fg = "#3C486B", font=("Helvetica 16 bold"), borderwidth=2, relief="solid", width = 10, height= 1).place(x=20, y= 600)
Button(main, text = "Medio", command = dificultadMedia, fg = "#3C486B", font=("Helvetica 16 bold"), borderwidth=2, relief="solid", width = 10, height= 1).place(x=170, y= 600)
Button(main, text = "Difícil", command = dificultadDificil, fg = "#3C486B", font=("Helvetica 16 bold"), borderwidth=2, relief="solid", width = 10, height= 1).place(x=320, y= 600)

# Botones Opciones
Button(main, text = "Solucionar", command = solucionarJuego,fg = "#5D9C59", font=("Helvetica 16 bold"), borderwidth=2, relief="solid", width = 10, height= 1).place(x=810, y= 506)
Button(main, text = "Revisar", command = revisarRespuestas,fg = "#5D9C59", font=("Helvetica 16 bold"), borderwidth=2, relief="solid", width = 10, height= 1).place(x=650, y= 506)
Button(main, text = "Borrar", command = borrar, fg = "#3C486B", font=("Helvetica 12 bold"), borderwidth=3, relief="solid", width = 10, height= 1).place(x=670, y= 280)

Button(main, text = "Cargar", command = cargar,fg = "#3C486B", font=("Helvetica 16 bold"), borderwidth=2, relief="solid", width = 10, height= 1).place(x= 20, y= 680)
Button(main, text = "Guardar", command = guardar,fg = "#3C486B", font=("Helvetica 16 bold"), borderwidth=2, relief="solid", width = 10, height= 1).place(x= 170, y= 680)

generarKeypad()

main.mainloop()
