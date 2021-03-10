import os
import tkinter as tk
from tkinter import *
import threading
from tkinter import *
from tkhtmlview import HTMLLabel

from PIL import Image, ImageTk

import chess
import chess.engine
global squareSize
squareSize = 50

global canvasSize
global my_html_label
global movestack
global movestackend
global lastvalidhtml
global movesstring
global fullmovelist
global fullmovelist_index
fullmovelist_index = 0
lastvalidhtml = ""
movestack = []
fullmovelist = []

movestackend = 0
movesstring = ""
canvasSize = 1

class TkFrame(Frame):
    # main Tk frame

    def __init__(self, parent):
        Frame.__init__(self, parent, relief=RAISED)
        self.parent = parent
        self.img = {}
        self.initUI()

    def initUI(self):
        self.parent.title("Raven Openings Explorer 1.0")
        self.parent.minsize(687,505)
        self.pack(fill=BOTH, expand=YES)



def updatehtml():
    global movestack
    global lastvalidhtml
    global movestackend
    global movelist_index
    global my_html_label
    global movesstring
    filedir = "chessopeningtheory"
    newboard = chess.Board()
    ply = 1
    i = 0
    for move in movestack:
        i+=1
        if i > movestackend: break
        ply += 1
        movesan = newboard.san(move)
        newboard.push(move)
        if (ply % 2 == 0):
            filedir += "/" + str(int(ply / 2)) + "._" + movesan
        else:
            filedir += "/" + str(int(ply / 2)) + "..." + movesan
    filedir += "/index.html"
    if (movestackend == 0):
        filedir = "chessopeningtheory/index.html"
    html = ""
    newhtml = ""
    #filedir = "chessopeningtheory/"
    if (os.path.exists(filedir)):
        f = open(filedir, "r", encoding="utf-8")
        html = f.read()
        f.close()
        html = html.replace("<a href=\"/wiki/", "<a href=\"https://en.wikibooks.org/wiki/")
        newhtml = ""
        allowwrite = 0
        headerstring = "<div id=\"mw-content-text\" lang=\"en\" dir=\"ltr\" class=\"mw-content-ltr\"><div class=\"mw-parser-output\"><div class=\"tright\" style=\"clear: right; width: 260px; text-align:center\">"
        headerstring2 = "<div id=\"contentSub\"><span class=\"subpages\">"
        for line in html.splitlines():
            ignoreline = False
            """
            if movestackend == 0: allowwrite = 1
            if ("Moves" in line): allowwrite = 1
            elif (headerstring in line): allowwrite = 1
            elif (headerstring2 in line): allowwrite = 1
            #if "<meta property=\"og:title\"" in line:
            #   allowwrite = 1
            if "<img" in line: ignoreline = True
            if "<td style=\"padding:0px 0.5em; border-right:1px solid #aaa;\">" in line: ignoreline = True
            if "<td style=\"border-bottom:1px solid #aaa;\">" in line: ignoreline = True
            if "<td style=\"padding:0px 0.5em; border-left:1px solid #aaa;\">" in line: ignoreline = True
            if "<td style=\"border-top:1px solid #aaa;\">" in line: ignoreline = True
            if "<td style=\"background-color:white\">" in line and line[-1] >= 'a' and line[-1] <= 'h': ignoreline = True
            if "<td style=\"background-color:white\">" in line and line[-1] >= '1' and line[-1] <= '8': ignoreline = True
            if "<td>" in line and "</td>" in line and line[4] >= 'a' and line[4] <= 'h': ignoreline = True
            if "<td>" in line and "</td>" in line and line[4] >= '1' and line[4] <= '8': ignoreline = True
            if "id=\"References\">References<" in line: allowwrite = 0
            """
            ignoreline = False
            if ("document.documentElement" in line): allowwrite = 0
            if (movestackend >= 0 and "<meta property=\"og:title\"" in line) or (movestackend == 0 and "chess opening theory" in line):
                allowwrite = 1
            #if movestackend == 0: allowwrite = 1
            if ("Moves" in line): allowwrite = 1
            elif (headerstring in line): allowwrite = 1
            elif (headerstring2 in line): allowwrite = 1
            #if "<meta property=\"og:title\"" in line:
            #   allowwrite = 1
            if "<img" in line: ignoreline = True
            if "<td style=\"padding:0px 0.5em; border-right:1px solid #aaa;\">" in line: ignoreline = True
            if "<td style=\"border-bottom:1px solid #aaa;\">" in line: ignoreline = True
            if "<td style=\"padding:0px 0.5em; border-left:1px solid #aaa;\">" in line: ignoreline = True
            if "<td style=\"border-top:1px solid #aaa;\">" in line: ignoreline = True
            if "<td style=\"background-color:white\">" in line and line[-1] >= 'a' and line[-1] <= 'h': ignoreline = True
            if "<td style=\"background-color:white\">" in line and line[-1] >= '1' and line[-1] <= '8': ignoreline = True
            if "<td>" in line and "</td>" in line and line[4] >= 'a' and line[4] <= 'h': ignoreline = True
            if "<td>" in line and "</td>" in line and line[4] >= '1' and line[4] <= '8': ignoreline = True
            if "id=\"References\">References<" in line: allowwrite = 0
            if "<img" in line: ignoreline = True
            if "<td style=\"padding:0px 0.5em; border-right:1px solid #aaa;\">" in line: ignoreline = True
            if "<td style=\"border-bottom:1px solid #aaa;\">" in line: ignoreline = True
            if "<td style=\"padding:0px 0.5em; border-left:1px solid #aaa;\">" in line: ignoreline = True
            if "<td style=\"border-top:1px solid #aaa;\">" in line: ignoreline = True
            if "<td style=\"background-color:white\">" in line and line[-1] >= 'a' and line[-1] <= 'h': ignoreline = True
            if "<td style=\"background-color:white\">" in line and line[-1] >= '1' and line[-1] <= '8': ignoreline = True
            if "<td>" in line and "</td>" in line and line[4] >= 'a' and line[4] <= 'h': ignoreline = True
            if "<td>" in line and "</td>" in line and line[4] >= '1' and line[4] <= '8': ignoreline = True
            if "id=\"References\">References<" in line: allowwrite = 0
            if allowwrite and not ignoreline: newhtml += line + "\n"
    else:
        pass
    if (os.path.exists(filedir) and newhtml != ""):
        lastvalidhtml = newhtml
    if (os.path.exists(filedir)):
        if (movestackend > 0 and "<td><b>Moves:</b> 1." not in html and "<b>Moves: " not in html):
            ply = 0
            movesstring = ""
            newboard = chess.Board()
            for i in range(0, movestackend, 2):
                ply += 2
                if (ply % 2 == 0):
                    movesstring += str(int(ply / 2)) + ". "
                movesstring += str(newboard.san(movestack[i])) + " "
                newboard.push(movestack[i])
                if (i+1 < movestackend):
                    movesstring += str(newboard.san(movestack[i+1])) + " "
                    newboard.push(movestack[i+1])
            newhtml = "<b>Moves: " + movesstring + "</b>" + newhtml
    if (os.path.exists(filedir)):
        my_html_label.set_html(newhtml)
    elif (movestackend > 0 and lastvalidhtml != "" and "<b>Moves: " not in lastvalidhtml):
        newboard = chess.Board()
        movesstring = ""
        ply = 0
        for i in range(0, movestackend, 2):
            ply += 2
            if (ply % 2 == 0):
                movesstring += str(int(ply / 2)) + ". "
            movesstring += str(newboard.san(movestack[i])) + " "
            newboard.push(movestack[i]) 
            if (i+1 < movestackend):
                movesstring += str(newboard.san(movestack[i+1])) + " "
                newboard.push(movestack[i+1])
        my_html_label.set_html("<b>Moves: " + movesstring + "</b>" + lastvalidhtml)

def highlightPieces():
    global board
    global boardCanvas
    global canvasSize
    global app
    global squareSize
    n = 0
    i = 0
    for move in board.legal_moves:
        filedir = getfilename(move)
        inBook = os.path.exists(filedir)
        i+=1
        if inBook: n+=1
    if n == i: return
    for move in board.legal_moves:
        movestring = str(move)
        startfile = ord(movestring[0]) - 97
        startrank = ord(movestring[1]) - 49
        endfile = ord(movestring[2]) - 97
        endrank = ord(movestring[3]) - 49
        (startTileScrX, startTileScrY) = convertBoardIndextoXY(startfile, 7 - startrank)
        (endTileScrX, endTileScrY) = convertBoardIndextoXY(endfile, 7 - endrank)
        filedir = getfilename(move)
        inBook = os.path.exists(filedir)
        if inBook:
            boardCanvas.create_rectangle(startTileScrX +3, startTileScrY +3, (startTileScrX + squareSize - 2), (startTileScrY + squareSize - 2), outline="#3333FF",
                                     width=6)
            boardCanvas.create_rectangle(endTileScrX +3, endTileScrY +3, (endTileScrX + squareSize - 2), (endTileScrY + squareSize - 2), outline="#3333FF",
                                     width=6)
    root.update()
    
    
def drawPieces():

    global board
    global boardCanvas
    global canvasSize
    global app
    global flipped
    global count
    count = 0
    app.img = {}
    #dspboard = list(board)
    #if flipped: dspboard = reversed(board)
    #if boardHistoryPos != (len(boardHistory) - 1) and boardHistory != []:
    #    dspboard = list(boardHistory[boardHistoryPos])
    #	if flipped: dspboard = reversed(dspboard)
    for i in range(0,64):
        c = 63 - i
        # xTile goes from 0 to 7 (files)
        # yTile goes from 0 to 7 (ranks)
        xTile = ((7 - c) % 8)  # every 8th byte is a new row
        yTile = int(c / 8)  # each column is the nth byte in a row
        squareSize = int(canvasSize / 8)
        if squareSize < 1: squareSize = 1
        xDrawPos = (xTile * squareSize) - 3
        yDrawPos = (yTile * squareSize) - 3
        if flipped: 
            xDrawPos = ((7 - xTile) * squareSize) - 3
            yDrawPos = ((7 - yTile) * squareSize) - 3
        
        mytext = str(i)
        piece = str(board.piece_at(i))
        
        pieceFile = ''

        if (piece == 'R'): pieceFile = 'pieces\WR.png'  #white rook
        if (piece == 'N'): pieceFile = 'pieces\WN.png'  #white knight
        if (piece == 'B'): pieceFile = 'pieces\WB.png'  #white bishop
        if (piece == 'Q'): pieceFile = 'pieces\WQ.png'  #white queen
        if (piece == 'K'): pieceFile = 'pieces\WK.png'  #white king
        if (piece == 'P'): pieceFile = 'pieces\WP.png'  #white pawn

        if (piece == 'r'): pieceFile = 'pieces\BR.png'  #black rook
        if (piece == 'n'): pieceFile = 'pieces\BN.png'  #black knight
        if (piece == 'b'): pieceFile = 'pieces\BB.png'  #black bishop
        if (piece == 'q'): pieceFile = 'pieces\BQ.png'  #black queen
        if (piece == 'k'): pieceFile = 'pieces\BK.png'  #black king
        if (piece == 'p'): pieceFile = 'pieces\BP.png'  #black pawn
        
        if (pieceFile != ''):
            img = Image.open(pieceFile)
            img = img.resize((squareSize - 0, squareSize - 0), Image.ANTIALIAS)
            app.img[count] = ImageTk.PhotoImage(img)
            boardCanvas.create_image(xDrawPos + 3, yDrawPos + 3, image=app.img[count], anchor=NW)
            
        count += 1


def appresize(event):
    global boardCanvas
    global canvasSize
    global squareSize
    global app
    global root
    global boardImg
    global my_html_label
    global button_startpos, button_back, button_forward, button_end

    boardCanvas.pack(expand=YES)
    #boardCanvas.config(width=30, height=30,bg="black")
    #boardCanvas.pack(expand=NO)
    #print app.winfo_height()
    appheight = app.winfo_height()
    appwidth = app.winfo_width()
    biggestDim = "height"
    canvasSize = appwidth - 202
    if appwidth > appheight:
        biggestDim = "width"
        canvasSize = appheight - 25
    if appwidth < (canvasSize + 202):
        canvasSize = appwidth - 202
    squareSize = canvasSize / 8

    canvasSize = (int(canvasSize / 8) * 8)
    h = canvasSize
    w = canvasSize
    #boardImg.zoom(scalew, scaleh)
    buttonspacewidth = appwidth - w
    buttonwidth = buttonspacewidth / 4
    boardCanvas.place(x=00,y=0,w=w,h=h)
    gameStateLabel.place(x=0, y=h+1,w=300,h=20)
    my_html_label.place(x=w+5,y=0,w=appwidth-w-5,h=appheight - 29)
    button_startpos.place(x=w,y=appheight - 30, w=buttonwidth,h=29)
    button_back.place(x=w+buttonwidth,y=appheight - 30, w=buttonwidth,h=29)
    button_forward.place(x=w+buttonwidth * 2, y = appheight - 30, w=buttonwidth, h=29)
    button_end.place(x=w+ buttonwidth * 3, y = appheight - 30, w = buttonwidth, h = 29)
    drawBoard()
    drawPieces()
    highlightPieces()
    root.update()
    
def drawBoard():
    global count
    global boardCanvas
    global canvasSize
    global colLight, colDark
    global app
    global boardImg
    global scalew, scaleh
    count = 0
    board = ''
    #img = Image.Open(file='board.PNG')
    img = Image.open("board.PNG")
    if (canvasSize > 0): img = img.resize((canvasSize, canvasSize),Image.ANTIALIAS)
    boardImg = ImageTk.PhotoImage(img)
    #boardImg.config(file='board.PNG')
    #boardImg = PhotoImage(file='board.PNG').zoom(320,320)
    #boardImg.width = scalew
    #boardImg.height = scaleh
    #print dir(boardImg)
    boardCanvas.delete("all")
    boardCanvas.create_image(3, 3, image=boardImg, anchor=NW)

def convertXYtoBoardIndex(x, y):
    global flipped
    global canvasSize

    squareSize = canvasSize / 8
    # Converts cursor X, Y position to board array X, Y position
    returnX = int(x / squareSize)
    returnY = int(y / squareSize)
    if flipped:
        returnX = int((canvasSize - x) / squareSize)
        returnY = int((canvasSize - y) / squareSize)
    return (returnX, returnY)


def convertBoardIndextoXY(x, y):
    global flipped
    global canvasSize

    squareSize = canvasSize / 8
    # Converts board index X, Y to tile draw position X, Y
    returnX = x * squareSize
    returnY = y * squareSize
    if flipped:
        returnX = int((7 - x) * squareSize)
        returnY = int((7 - y) * squareSize)
    return (returnX, returnY)

def islower(c):
    if c >= 'a' and c <= 'z': return True
    return False

def isupper(c):
    if c >= 'A' and c <= 'Z': return True
    return False

def canvasClick(event):
    global clickDragging
    global canvasSize

    global ClickStartScrPos
    global clickStartPiece
    global clickStartBoardIndex
    global lastTileXIndex, lastTileYIndex
    global clickStartSquare
    global clickEndSquare
    global board
    global startTileScrX, startTileScrY
    if ((board.turn and p1 == "Human") or (not board.turn and p2 == "Human")):
        # human to move
        
        squareSize = canvasSize / 8
        mouseX = event.x
        mouseY = event.y
        
        # convert mouseX, mouseY to board array indices
        (tileXIndex, tileYIndex) = convertXYtoBoardIndex(mouseX, mouseY)
        #convert board indices to screen X Y position of tiles
        (tileScrX, tileScrY) = convertBoardIndextoXY(tileXIndex, tileYIndex)
        
        boardIndex = tileYIndex * 8 + tileXIndex
        boardIndex = 63 - boardIndex
        boardIndexX = 7 - (boardIndex % 8)
        boardIndexY = int(boardIndex / 8)
        boardIndex = boardIndexY * 8 + boardIndexX
        piece = board.piece_at(boardIndex)
        
        if (piece == None): return
        if ((board.turn and islower(str(piece))) or (not board.turn and isupper(str(piece)))): return
        
        #draw green square over tile
        #boardCanvas.draw.rect(pygScreen, (0,255,0), (tileScrX + 2, tileScrY + 2, 57, 57), 4)
        boardCanvas.create_rectangle(tileScrX +3, tileScrY +3, (tileScrX + squareSize - 2), (tileScrY + squareSize - 2), outline="#000000",
                                     width=6)
        clickDragging = True
        clickStartScrPos = (tileScrX, tileScrY)  # store top left screen X, Y for tile position
        clickStartBoardIndex = (tileXIndex, tileYIndex)
        startTileScrX = tileScrX
        startTileScrY = tileScrY
        clickStartPiece = piece
        lastTileXIndex = tileXIndex
        lastTileYIndex = tileYIndex
        clickStartSquare = boardIndex
        clickEndSquare = boardIndex

def getfilename(move):
    filedir = "chessopeningtheory"
    newboard = chess.Board()
    ply = 1
    for origmove in movestack:
        ply += 1
        movesan = newboard.san(origmove)
        newboard.push(origmove)
        if (ply % 2 == 0):
            filedir += "/" + str(int(ply / 2)) + "._" + movesan
        else:
            filedir += "/" + str(int(ply / 2)) + "..." + movesan
    ply += 1
    if (ply % 2 == 0):
        filedir += "/" + str(int(ply / 2)) + "._" + board.san(move)
    else:
        filedir += "/" + str(int(ply / 2)) + "..." + board.san(move)
    filedir += "/index.html"
    return filedir
    
def canvasMotion(event):

    global lastTileScrX
    global lastTileScrY
    global lastTileXIndex
    global lastTileYIndex
    global canvasSize
    global clickStartBoardIndex
    global clickStartSquare
    global clickEndSquare
    global movestack
    global startTileScrX, startTileScrY

    if not clickDragging: return
    squareSize = canvasSize / 8
    mouseX = event.x
    mouseY = event.y
    if (mouseX > canvasSize or mouseX < 0 or mouseY > canvasSize or mouseY < 0): return
    # convert mouseX, mouseY to board array indices
    (tileXIndex, tileYIndex) = convertXYtoBoardIndex(mouseX, mouseY)
    #convert board indices to screen X Y position of tiles
    (tileScrX, tileScrY) = convertBoardIndextoXY(tileXIndex, tileYIndex)

    #clickStartBoardIndex = (tileXIndex, tileYIndex)
    #calculate boardIndex = board[] square index
    boardIndex = tileYIndex * 8 + tileXIndex
    boardIndex = 63 - boardIndex
    boardIndexX = 7 - (boardIndex % 8)
    boardIndexY = int(boardIndex / 8)
    boardIndex = boardIndexY * 8 + boardIndexX
    clickEndSquare = boardIndex
    startSquare = clickStartSquare
    endSquare = boardIndex
    piece = str(board.piece_at(startSquare))
    move = chess.Move(from_square = clickStartSquare, to_square = boardIndex)
    if ((piece == 'P' and endSquare >= 56 and endSquare <= 63) or (piece == 'p' and endSquare >= 0 and endSquare <= 7)):
        move.promotion = chess.QUEEN
    #print(endSquare)
    #print(board.piece_at(startSquare))
    inbook = False
    filedir = getfilename(move)
    inBook = os.path.exists(filedir)
    islegal = False
    for legalmove in board.legal_moves:
        if str(move) == str(legalmove): islegal = True
    if islegal and not inBook:
        #draw green square over moused over square
        boardCanvas.create_rectangle(tileScrX +3, tileScrY +3, (tileScrX + (squareSize - 2)), (tileScrY + (squareSize - 2)),
                                     outline="#00FF00", width=6)
        if ((lastTileXIndex != tileXIndex) or (lastTileYIndex != tileYIndex)):  # user mouses to a new square
            if (clickStartBoardIndex != (lastTileXIndex, lastTileYIndex)):  # don't redraw if it's the start square
                redrawTile(lastTileXIndex, lastTileYIndex)  # redraw over last square (to remove green rect)
                drawPieces()
                #highlightPieces()
                root.update()
                lastTileXIndex = tileXIndex
        lastTileYIndex = tileYIndex
    if (islegal and inBook):
        boardIndex = lastTileYIndex * 8 + lastTileXIndex
        boardIndex = 63 - boardIndex
        boardIndexX = 7 - (boardIndex % 8)
        boardIndexY = int(boardIndex / 8)
        boardIndex = boardIndexY * 8 + boardIndexX
        # it's a book move
       #draw blue square over moused over square
        boardCanvas.create_rectangle(tileScrX +3, tileScrY +3, (tileScrX + (squareSize - 2)), (tileScrY + (squareSize - 2)),
                                     outline="#0000AA", width=6)
        if ((lastTileXIndex != tileXIndex) or (lastTileYIndex != tileYIndex)):  # user mouses to a new square
            if (clickStartBoardIndex != (lastTileXIndex, lastTileYIndex)):  # don't redraw if it's the start square
                redrawTile(lastTileXIndex, lastTileYIndex)  # redraw over last square (to remove green rect)
                drawPieces()
                #highlightPieces()
                root.update()
        #redrawTile(clickStartBoardIndex[0], clickStartBoardIndex[1])
        #draw original square outline
        (startTileScrX, startTileScrY) = convertBoardIndextoXY(int(clickStartBoardIndex[0]), int(clickStartBoardIndex[1]))
        boardCanvas.create_rectangle(startTileScrX +3, startTileScrY +3, (startTileScrX + squareSize - 2), (startTileScrY + squareSize - 2), outline="#000000",
                          width=6)
        lastTileXIndex = tileXIndex
        lastTileYIndex = tileYIndex
    
        
def canvasRelease(event):

    global clickDragging
    global board, root
    global clickStartSquare
    global p1, p2
    global gameStateVar
    global clickEndSquare
    global my_html_label
    global movestack, movestackend
    global lastvalidhtml
    global fullmovelist
    global fullmovelist_index
    
    if (clickDragging == False):
        return

    clickDragging = False
    mouseX = event.x
    mouseY = event.y

    # convert mouseX, mouseY to board array indices
    (tileXIndex, tileYIndex) = convertXYtoBoardIndex(mouseX, mouseY)
    #convert board indices to X Y position of tiles
    #(tileScrX, tileScrY) = convertBoardIndextoXY(tileXindex, tileYindex)
    #startSquare = (clickStartBoardIndex[0], clickStartBoardIndex[1])
    #endSquare = (tileXindex, tileYindex)

    endSquare = clickEndSquare
    #startSquare = clickStartSquare[1] * 8 + clickStartSquare[0]
    #startSquare = 63 - startSquare
    startSquare = clickStartSquare
    hasmoved = False
    move = chess.Move(from_square = startSquare, to_square = endSquare)
    #print(endSquare)
    #print(board.piece_at(startSquare))
    piece = str(board.piece_at(startSquare))
    if ((piece == 'P' and endSquare >= 56 and endSquare <= 63) or (piece == 'p' and endSquare >= 0 and endSquare <= 7)):
        move.promotion = chess.QUEEN
    agMove = board.san(move)
    islegal = False
    for legalmove in board.legal_moves:
        if str(move) == str(legalmove): islegal = True
    if startSquare == endSquare: islegal = False
    if islegal:
        movestack.append(move)
        movestackend += 1
        # pop every move after current index from fullmovelist
        i = len(fullmovelist)
        while i >= movestackend:
            #print(str(i) + " " + str(movestackend))
            fullmovelist.pop()
            i -= 1
            
        fullmovelist.append(move)
        fullmovelist_index += 1
        print(fullmovelist)
        board.push(move)
        if (board.turn): gameStateVar.set("White to move.")
        else: gameStateVar.set("Black to move.")
        hasmoved = True
    if hasmoved:
        updatehtml()
    drawBoard()
    drawPieces()
    highlightPieces()
    root.update()
    legalmoves = board.legal_moves
    count = 0
    for x in legalmoves:
        count += 1
    if (count == 0):
        gameStateVar.set("End of game.")
        root.update()
        return
    #if (board.turn and p1 != "Human"): newAIthread()
    #elif (not board.turn and p2 != "Human"): newAIthread()

"""
def getAIMove():
global board
global root
global canvasSize
global gameStateVar
global pvmove

lastpvmovestr = ""
if (p1 == "AI" and board.turn): engine = engine1
elif (p2 == "AI" and not board.turn): engine = engine2
lastStartScrX = None
lastStartScrY = None
lastEndScrX = None
lastEndScrY = None
with engine.analysis(board, chess.engine.Limit(time=(0.5))) as analysis:
    for info in analysis:
        if (info.get("pv") != None):
            pvmove = info.get("pv")[0]
            print(info.get("score"))
            pvmovestr = str(pvmove)
            if lastpvmovestr != pvmovestr:
                startfile = ord(pvmovestr[0]) - 97
                startrank = ord(pvmovestr[1]) - 49
                endfile = ord(pvmovestr[2]) - 97
                endrank = ord(pvmovestr[3]) - 49
                startrank = 7 - startrank
                endrank = 7 - endrank
                squareSize = canvasSize / 8
                (startScrX, startScrY) = convertBoardIndextoXY(startfile, startrank)
                (endScrX, endScrY) = convertBoardIndextoXY(endfile, endrank)
                #drawBoard()
                #drawPieces()
                if lastStartScrX != None:
                    colLight = (128, 128, 128)
                    colDark = (196, 196, 196)
                    colLight = '#%02x%02x%02x' % colLight
                    colDark = '#%02x%02x%02x' % colDark
                    startcol = colLight
                    endcol = colLight
                    if ((laststartrank + laststartfile) % 2 == 0): startcol = colDark
                    if ((lastendrank + lastendfile) % 2 == 0): endcol = colDark
                    boardCanvas.create_rectangle(lastStartScrX +3, lastStartScrY +3, (lastStartScrX + squareSize - 2), (lastStartScrY + squareSize - 2), outline=startcol,
                                 width=6)
                    boardCanvas.create_rectangle(lastEndScrX +3, lastEndScrY +3, (lastEndScrX + squareSize - 2), (lastEndScrY + squareSize - 2), outline=endcol,
                                 width=6)
                boardCanvas.create_rectangle(startScrX +3, startScrY +3, (startScrX + squareSize - 2), (startScrY + squareSize - 2), outline="#0000FF",
                                 width=6)
                boardCanvas.create_rectangle(endScrX +3, endScrY +3, (endScrX + squareSize - 2), (endScrY + squareSize - 2), outline="#0000FF",
                                 width=6)
                lastStartScrX = startScrX
                lastStartScrY = startScrY
                lastEndScrX = endScrX
                lastEndScrY = endScrY
                laststartfile = startfile
                laststartrank = startrank
                lastendfile = endfile
                lastendrank = endrank
            lastpvmovestr = pvmovestr
pvmove = analysis.info['pv'][0]
board.push_uci(str(pvmove))
root.after(1, drawBoard)
root.after(1, drawPieces)
legalmoves = board.legal_moves
count = 0
for x in legalmoves:
    count += 1
if (count == 0):
    gameStateVar.set("End of game.")
    root.update()
    gameinprogress = False
else:
    if (board.turn): gameStateVar.set("White to move.")
    else: gameStateVar.set("Black to move.")
    root.update()
    if (p1 == "AI" and board.turn):
        newAIthread()
    elif (p2 == "AI" and not board.turn):
        newAIthread()

def newAIthread():
global root
thread = threading.Thread(target=getAIMove)
thread.start()
"""
def redrawTile(x, y):
    global count
    global board
    global flipped
    global canvasSize
    count = 0
    colLight = (128, 128, 128)
    colDark = (196, 196, 196)
    colLight = '#%02x%02x%02x' % colLight
    colDark = '#%02x%02x%02x' % colDark

    squareSize = canvasSize / 8
    # redraws a tile with its piece
    boardIndex = y * 8 + x
    boardIndex = 63 - boardIndex
    boardIndexX = 7 - (boardIndex % 8)
    boardIndexY = int(boardIndex / 8)
    boardIndex = boardIndexY * 8 + boardIndexX
    i = x
    j = y
    xpos = (i * squareSize) - 3
    ypos = (j * squareSize) - 3 # each tile is 60x60 px
    if flipped:
        xpos = ((7 - i) * squareSize)
        ypos = ((7 - j) * squareSize)
    col = colLight
    if ( ( (i + j) % 2 ) == 0 ): col = colDark  # alternate tiles are dark
    # redraw tile
    drawEndX = (xpos + squareSize)
    drawEndY = (ypos + squareSize)
    if flipped:
        drawEndX = ((7 - xpos) + squareSize)
        drawEndY = ((7 - ypos) + squareSize)

    tempDrawDir = 1
    if (not board.turn) and (flipped == True): tempDrawDir = 0
    if (board.turn) and (flipped == True): tempDrawDir = 0
    boardCanvas.create_rectangle(xpos + 3 * tempDrawDir, ypos + 3 * tempDrawDir, (xpos + squareSize + 3 * tempDrawDir), (ypos + squareSize + 3 * tempDrawDir), fill=col, outline=col)
    #redraw piece
    piece = str(board.piece_at(boardIndex))
    pieceFile = ''
    if (piece == 'R'): pieceFile = 'pieces\WR.png'  #white rook
    if (piece == 'N'): pieceFile = 'pieces\WN.png'  #white knight
    if (piece == 'B'): pieceFile = 'pieces\WB.png'  #white bishop
    if (piece == 'Q'): pieceFile = 'pieces\WQ.png'  #white queen
    if (piece == 'K'): pieceFile = 'pieces\WK.png'  #white king
    if (piece == 'P'): pieceFile = 'pieces\WP.png'  #white pawn

    if (piece == 'r'): pieceFile = 'pieces\BR.png'  #black rook
    if (piece == 'n'): pieceFile = 'pieces\BN.png'  #black knight
    if (piece == 'b'): pieceFile = 'pieces\BB.png'  #black bishop
    if (piece == 'q'): pieceFile = 'pieces\BQ.png'  #black queen
    if (piece == 'k'): pieceFile = 'pieces\BK.png'  #black king
    if (piece == 'p'): pieceFile = 'pieces\BP.png'  #black pawn
    if (pieceFile != ''):
        #app.img[count] = ImageTk.PhotoImage(file=pieceFile)
        #boardCanvas.create_image((xpos), (ypos), image=app.img[count], anchor=NW)

        img = Image.open(pieceFile)
        if squareSize > 0: img = img.resize((int(squareSize) - 0, int(squareSize) - 0), Image.ANTIALIAS)
        app.img[boardIndex] = ImageTk.PhotoImage(img)
        boardCanvas.create_image(xpos+3*tempDrawDir, ypos+3*tempDrawDir, image=app.img[boardIndex], anchor=NW)
    count+= 1
    pass


def movelistBack(event):
    global movelist_index
    global root
    global board
    global movestackend
    global fullmovelist_index
    global fullmovelist
    if movestackend == 0: return
    fullmovelist_index -= 1
    movestackend -= 1
    movestack.pop()
    board.pop()
    drawBoard()
    drawPieces()
    highlightPieces()
    updatehtml()
    root.update()
    
def movelistStartpos(event):
    global board
    global movestackend
    global movestack
    global fullmovelist
    global fullmovelist_index
    movestack = []
    board = chess.Board()
    movestackend = 0
    fullmovelist_index = 0
    drawBoard()
    drawPieces()
    highlightPieces()
    updatehtml()
    root.update()
    
def movelistForward(event):
    global board
    global movestackend
    global movestack
    global fullmovelist
    global fullmovelist_index
    if len(fullmovelist) <= movestackend: return
    move = fullmovelist[movestackend]
    board.push(move)
    movestackend += 1
    fullmovelist_index += 1
    movestack.append(move)
    drawBoard()
    drawPieces()
    highlightPieces()
    updatehtml()
    root.update()

def movelistEnd(event):
    global board
    global movestack
    global fullmovelist
    global fullmovelist_index
    global movestackend
    newboard = chess.Board()
    movestackend = 0
    fullstack_index = 0
    for move in movestack:
        board.pop()
        
    movestack = []
    for move in fullmovelist:
        board.push(move)
        movestack.append(move)
        movestackend+=1
        fullmovelist_index+=1
    drawBoard()
    drawPieces()
    highlightPieces()
    updatehtml()
    root.update()
    pass
    
def main():
    global p1
    global p2
    global p1engine, p2engine
    global boardCanvas
    global canvasSize
    global app
    global root
    global board
    global clickDragging
    global flipped
    global gameStateVar, gameStateLabel
    global engine1
    global engine2
    global keeprunning
    global gameinprogerss
    global my_html_label
    global button_startpos, button_back, button_forward, button_end
    global movestack, movestackend

    gameinprogress = False

    flipped = False
    clickDragging = False

    root = tk.Tk()

    # position/dimensions for main tk frame
    x = 100
    y = 100
    w = 887
    h = 505
    oldappheight = h
    oldappwidth = w
    geostring = "%dx%d+%d+%d" % (w, h, x, y)

    root.geometry(geostring)
    app = TkFrame(root)
    app.bind("<Configure>", appresize)

    boardCanvas = Canvas(app, width=480, height=480)

    boardCanvas.bind("<Button-1>", canvasClick)
    boardCanvas.bind("<ButtonRelease-1>", canvasRelease)
    boardCanvas.bind("<B1-Motion>", canvasMotion)

    boardCanvas.pack(expand=YES)
    boardCanvas.place(x=0, y=0)

    gameStateVar = StringVar()

    gameStateLabel = Label(root, font=('calibri', 15), justify=LEFT, anchor="w", textvariable=gameStateVar)
    gameStateLabel.pack()
    gameStateLabel.place(x=0, y=480)

    my_html_label = HTMLLabel(root, html="opening text appears here")
    my_html_label.pack(pady=20, padx=20, fill="both", expand=True)
    
    button_startpos = Button(root, width=100, height=48, text="<<")
    button_startpos.pack()
    button_back = Button(root, text="<")
    button_back.pack()
    button_forward = Button(root, text=">")
    button_forward.pack()
    button_end = Button(root, text=">>")
    button_end.pack()
    button_back.bind("<ButtonRelease-1>", movelistBack)
    button_startpos.bind("<ButtonRelease-1>", movelistStartpos)
    button_forward.bind("<ButtonRelease-1>", movelistForward)
    button_end.bind("<ButtonRelease-1>", movelistEnd)
    f = open("chessopeningtheory/index.html", "r", encoding="utf-8")
    html = f.read()
    f.close()
    newhtml = ""
    allowwrite = 0
    for line in html.splitlines():
        ignoreline = False
        if "<meta property=\"og:title\"" in line:
            allowwrite = 1
        if "<img" in line: ignoreline = True
        if "<td style=\"padding:0px 0.5em; border-right:1px solid #aaa;\">" in line: ignoreline = True
        if "<td style=\"border-bottom:1px solid #aaa;\">" in line: ignoreline = True
        if "<td style=\"padding:0px 0.5em; border-left:1px solid #aaa;\">" in line: ignoreline = True
        if "<td style=\"border-top:1px solid #aaa;\">" in line: ignoreline = True
        if "<td style=\"background-color:white\">" in line and line[-1] >= 'a' and line[-1] <= 'h': ignoreline = True
        if "<td style=\"background-color:white\">" in line and line[-1] >= '1' and line[-1] <= '8': ignoreline = True
        if "<td>" in line and "</td>" in line and line[4] >= 'a' and line[4] <= 'h': ignoreline = True
        if "<td>" in line and "</td>" in line and line[4] >= '1' and line[4] <= '8': ignoreline = True
        if "id=\"References\">References<" in line: allowwrite = 0
        if allowwrite and not ignoreline: newhtml += line + "\n"
    my_html_label.set_html(newhtml)
    p1 = "Human"
    p2 = "Human"
    """
    if (p1 == "AI"):
        engine1 = chess.engine.SimpleEngine.popen_uci("c:\\engines\\stockfish11.exe")

    if (p2 == "AI"):
        engine2 = chess.engine.SimpleEngine.popen_uci("c:\\c\\raven-weak\\raven-weak.exe")
    """
    initGame(p1, p2)
    #root.update()

    drawBoard()
    drawPieces()
    highlightPieces()
    #root.after(1, mainloop())

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

def on_closing():
    global root
    global engine1
    global engine2
    if (p1 == "AI"): engine1.close()
    if (p2 == "AI"): engine2.close()
    root.destroy()

def initGame(player1, player2):
    global board
    global gameinprogress
    global gameStateVar
    board = chess.Board()
    gameinprogress = True
    gameStateVar.set("White to move.")
    #if (p1 == "AI" and board.turn): newAIthread()
    #elif (p2 == "AI" and not board.turn): newAIthread()

main()