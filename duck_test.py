import ducky
class Tester:
    def __init__(self):
        self.errors = []
        self.success = []

    def test(self,code, name="Unnamed"):
        try:
            exec(code, globals())
            self.success.append(name)
            print(f"\033[32mCode:\n{code}\n({name}) executed successfully\n")

        except Exception as error:
            print(f"\033[31m{error}\n")
            self.errors.append(f"Line:  {len(self.errors)+len(self.success)+1}   {error}")

    def results(self):
        total = len(self.success) + len(self.errors)
        if total == 0:
            percent = 0
        else:
            percent = (len(self.success) / total) * 100

        if percent == 100:
            print("\033[92m------------------------------------------------------------")
            print("\033[92mCompleted 100% successfully:\n")

        elif percent >= 90:
            print("\033[32m------------------------------------------------------------")
            print("\033[32mCompleted 90% or more successfully:\n")

        elif percent >= 80:
            print("\033[33m------------------------------------------------------------")
            print("\033[33mCompleted 80% or more successfully:\n")
        elif percent >= 70:
            print("\033[38;5;208m------------------------------------------------------------")
            print("\033[38;5;208mCompleted 70% or more successfully:\n")
        else:
            print("\033[91m------------------------------------------------------------")
            print("\033[91mCompleted less than 60% successfully:\n")

        for s in self.success:
            print(f"\033[32m{s}")
        if len(self.errors) > 0:
            print(f"\n\033[31mFailed tests:\n")
        for e in self.errors:
            print(f"\033[31m{e}")


#basic turtle and Turtle Manager
Test1 = Tester()
Test1.test("t=ducky.Turtle()","Create turtle")
Test1.test("t.speed(0)","Set turtle speed")
Test1.test("duck=ducky.TurtleManager(t)","Instantiate TurtleManager class")
Test1.test("for i in duck.colours:\n\tduck.colour(i)\n\tt.penup()\n\tt.goto(0,0)\n\tt.pendown()\n\tt.forward(100)","Test pen and colours")
Test1.test("t.clear()","Clear the canvas")
Test1.test("t.penup()\nt.goto(0,0)\nduck.colour('black')\nt.pendown()","Reset the turtle")
Test1.test("ducky.done()","Finish")
Test1.results()
input() #pause
#matrix manager test
Test2 = Tester()
Test2.test("background = ducky.matrix(3,3)","Make a 3 x 3 matrix")
Test2.test("line = [[0,1,0][0,1,0][0,1,0]]","Make a 3 x 3 matrix with a line in the middle")
Test2.test("Matrix = MatrixManager(background,2,line)","Make an object of the Matrix Manager class")
Test2.test("Matrix.loop_func()","Run the main loop function of the matrix")
Test2.test("Matrix.x+=1","Move the line horizontally in the matrix")
Test2.test("Matrix.loop_func()","Run the main loop function of the matrix")
Test2.test("Matrix.x-=2","Move the line horizontally in the matrix")
Test2.test("Matrix.loop_func","Run the main loop function of the matrix")
Test2.test("Matrix.x+=1","Reset the line's position")
Test2.test("Matrix.y+=1","Move the line vertically in the matrix")
Test2.results()