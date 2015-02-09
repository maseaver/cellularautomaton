import sys

class State(object):
    def __init__(self):
        self.maxX = 76
        self.maxY = 25

        self.x = self.sanitizedDimension("width", self.maxX)
        self.y = self.sanitizedDimension("height", self.maxY)
        
        self.rows = [[]] * self.y
        for row in range(self.y):
            cells = [[]] * self.x
            for col in range(self.x):
                cells[col] = 0
            self.rows[row] = cells

    def sanitizedDimension(self, name, maximum):
        notAnIntError = "That doesn't look like an integer to me.\n"
        noInput = "    I'll just assume 10.\n"
        
        prompt = "    Enter the " + name + " as an integer from 1 to "
        prompt = prompt + str(maximum) + " inclusive: "

        valueGotten = False

        while valueGotten == False:
            userInput = raw_input(prompt)
            print
            inputList = userInput.split()

            if len(inputList) != 0:
                firstInput = inputList[0]
                if len(firstInput) == 1:
                    try:
                        value = int(firstInput)
                        valueGotten = True
                    except ValueError:
                        print notAnIntError
                else:
                    try:
                        value = int(firstInput[:2])
                        valueGotten = True
                    except ValueError:
                        print notAnIntError
            else:
                print noInput
                value = 10
                valueGotten = True
        
        if value <= 0:
            value = 1
        elif value > maximum:
            value = maximum

        return value

    def color(self, value):
        colorDict = {
            0 : "30",
            1 : "30",
            2 : "34",
            3 : "34",
            4 : "32",
            5 : "32",
            6 : "33",
            7 : "33",
            8 : "31",
            9 : "31",
            }
        formattingString = "\033[" + colorDict[value] + "m"

        return formattingString

    def drawBoard(self, line = ""):
        for i in range(self.y):
            thisLine = line[:]
            for h in range(self.x):
                value = self.rows[i][h]
                thisLine = thisLine + self.color(value) + str(value)
            print thisLine
        print "\033[0m"

    def bound(self, value, maxValue):
        if value not in range(maxValue) and value != None:
            value = value % maxValue
        return value
            
    def calculateCell(self, row, col):
        value = self.rows[row][col]
        neighbors = {
"north" : self.rows[self.bound(row - 1, self.y)][self.bound(col, self.x)],
"nWest" : self.rows[self.bound(row - 1, self.y)][self.bound(col - 1, self.x)],
"west" : self.rows[self.bound(row, self.y)][self.bound(col - 1, self.x)],
"sWest" : self.rows[self.bound(row + 1, self.y)][self.bound(col - 1, self.x)],
"south" : self.rows[self.bound(row + 1, self.y)][self.bound(col, self.x)],
"sEast" : self.rows[self.bound(row + 1, self.y)][self.bound(col + 1, self.x)],
"east" : self.rows[self.bound(row, self.y)][self.bound(col + 1, self.x)],
"nEast" : self.rows[self.bound(row - 1, self.y)][self.bound(col + 1, self.x)],
            }
            
        if value > 0:
            value = value - 1
        if neighbors["north"] > 0:
            value = value + 1
        if neighbors["east"] > 0:
            value = value + 1
        if neighbors["south"] > 0:
            value = value + 1
        if neighbors["west"] > 0:
            value = value + 1
        value = value % 10
        return value

    def calculateBoard(self):
        newRows = [[]] * self.y
        for row in range(self.y):
            newRows[row] = [[]] * self.x
            for col in range(self.x):
                newRows[row][col] = self.calculateCell(row, col)
        return newRows

    def setPoint(self, num, col, row):
        self.rows[row][col] = num

    def setPoints(self, num, col1, row1, col2, row2):
        arguments = [num, col1, row1, col2, row2]

        if row2 == None:
            row2 = row1
        if col2 == None:
            col2 = col1

        num = num % 10
        rowMin = self.bound(min(row1, row2), self.y)
        rowMax = self.bound(max(row1, row2) + 1, self.y + 1)
        colMin = self.bound(min(col1, col2), self.x)
        colMax = self.bound(max(col1, col2) + 1, self.x + 1)
        
        if rowMin == rowMax and colMin == colMax:
            self.setPoint(num, rowMin, rowMax)
        else:

            rectangleMembers = []

            for i in range(rowMin, rowMax):
                for h in range(colMin, colMax):
                    rectangleMembers.append((h, i))

            for point in rectangleMembers:
                row = point[1]
                col = point[0]
                self.setPoint(num, col, row)

        return self.rows

def introduction():
    introMessage = """\
    Hello, and welcome to my cellular automaton program.

    The first thing it'll ask you to do is enter the width and then the height
as separate integer values. It will then draw a blank board and solicit your
input, at which point you have five options:
  1. you may input a value and a point, expressed as <value x y> with each
     item an integer, to set the point (x, y) to value;
  2. you may enter a value followed by two points, expressed as <value x1 y1 
     x2> with each item an integer, to set the rectangle defined by (x, y1, x2,
     y2) to value;
  3. you may hit enter to advance the automaton;
  4. you may enter a lowercase h to reprint this message;
  5. or you may enter a lowercase q to quit.

    Remember GIGO: if you give the program unexpected input, expect unexpected
output.
    
    After you give it input, it should show the old board with the
modifications just made (indented), then calculate the new state of the board,
display it, and solicit input again."""
    print introMessage
    print

def sanitizedMidRunCommand():
    intentGotten = False

    commandStrings = ["",
                      "h",
                      "q",]
    
    
    while intentGotten == False:
        command = raw_input("""\
    Value and point or points, press enter to advance, the lowercase letter h to
print the introductory message, or the lowercase letter q to end.

> """)
        print
        
        commandList = command.split()

        if len(commandList) == 0:
            commandList.append("")
        
        if commandList[0] in commandStrings:
            userInput = commandList[0]
            intentGotten = True
        else:
            trimmedCommandListCopy = commandList[:5]
            for i in range(len(trimmedCommandListCopy)):
                try:
                    int(commandList[i])
                except ValueError:
                    print """\
    At least one of those doesn't look like an integer to me."""
                    break
                else:
                    trimmedCommandListCopy[i] = int(commandList[i])
            else:
                userInput = trimmedCommandListCopy
                if len(userInput) < 5:
                    for i in range(5 - len(userInput)):
                        userInput.append(None)
                intentGotten = True
    else:
        return userInput

def main():
    state = State()
    print
    state.drawBoard()
    
    while True:
        userInput = sanitizedMidRunCommand()

        #print userInput

        if userInput != "":
            if userInput == "q":
                break
            elif userInput[0] == "h":
                introduction()
                state.drawBoard()
                continue
            else:
                num = userInput[0]
                col1 = userInput[1]
                row1 = userInput[2]
                col2 = userInput[3]
                row2 = userInput[4]
                state.rows = state.setPoints(num, col1, row1, col2, row2)
                state.drawBoard("    ")
                
        state.rows = state.calculateBoard()
        state.drawBoard()        
    
if __name__ == "__main__":
    introduction()
    main()
