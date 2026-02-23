import ducky,time
from ducky import Tester
class IndependentTimer:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.perf_counter()

    def stop(self):
        self.end_time = time.perf_counter()

    def elapsed(self):
        if self.start_time is None:
            return 0
        if self.end_time is None:
            return time.perf_counter() - self.start_time
        return self.end_time - self.start_time


def print_average():
    avg = Tester.average()
    if avg == 100:
        color = "\033[92m"
    elif avg >= 90:
        color = "\033[32m"
    elif avg >= 80:
        color = "\033[33m"
    elif avg >= 70:
        color = "\033[38;5;208m"
    else:
        color = "\033[91m"
    print(f"{color}------------------------------------------------------------")
    print(f"{color}Average success across all Tester instances: {avg:.2f}%\033[0m")

def hide_turtle_window():
    screen = ducky.Screen()
    screen.tracer(0, 0)
    canvas = screen.getcanvas()
    root = canvas.winfo_toplevel()
    root.withdraw()

if __name__ == "__main__":
    full_timer = IndependentTimer()
    full_timer.start()
    #basic turtle and Turtle Manager test
    start = time.perf_counter()
    Test1 = Tester()

    Test1.test("import ducky","Import ducky")

    hide_turtle_window()
    t=ducky.Turtle()

    Test1.test("t.speed(0)","Set turtle speed")
    Test1.test("duck=ducky.TurtleManager(t)","Instantiate TurtleManager class")
    Test1.test("for i in duck.colours:\n\tduck.colour(i)\n\tt.penup()\n\tt.goto(0,0)\n\tt.pendown()\n\tt.forward(100)","Test pen and colours")
    Test1.test("t.home()\nduck.colour('black')\nt.pendown()","Reset the turtle")
    Test1.test("t.clear()","Clear the canvas")
    end = time.perf_counter()
    print(f"\033[35mCompleted in {end-start} seconds")
    Test1.results()


    ducky.wait(20)
    #turtle functions test
    start = time.perf_counter()
    Test2 = Tester()

    Test2.test("ducky.splat(t,3)","Run custom splat function")
    Test2.test("t.home()\nduck.colour('black')\nt.pendown()","Reset the turtle")
    Test2.test("t.clear()","Clear the canvas")
    Test2.test("ducky.pizza(t,size=10,x=0,y=0)","Run custom pizza function")
    ducky.wait(20)
    Test2.test("t.home()\nduck.colour('black')\nt.pendown()","Reset the turtle")
    Test2.test("t.clear()","Clear the canvas")
    Test2.test("ducky.star(t)","Run custom star function")
    ducky.wait(20)
    Test2.test("t.home()\nduck.colour('black')\nt.pendown()","Reset the turtle")
    Test2.test("t.clear()","Clear the canvas")
    Test2.test("ducky.dots(t,5)","Run custom star function")
    ducky.wait(20)
    Test2.test("t.home()\nduck.colour('black')\nt.pendown()","Reset the turtle")
    Test2.test("t.clear()","Clear the canvas")
    Test2.test("ducky.target_board(t)","Run custom star function")
    ducky.wait(20)
    Test2.test("ducky.bye()","Close turtle")
    end = time.perf_counter()
    print(f"\033[35mCompleted in {end-start} seconds")
    Test2.results()

    ducky.wait(20)
    #matrix manager test
    start = time.perf_counter()
    Test3 = Tester()

    Test3.test("background = ducky.matrix(3,3)","Make a 3 x 3 matrix")
    Test3.test("line = [[0,1,0],[0,1,0],[0,1,0]]","Make a 3 x 3 matrix with a line in the middle")
    Test3.test("Matrix = ducky.MatrixManager(background,1000,line)","Make an object of the Matrix Manager class")
    Test3.test("Matrix.loop_func()","Run the main loop function of the matrix")
    Test3.test("Matrix.x_pos+=1","Move the line horizontally in the matrix")
    Test3.test("Matrix.loop_func()","Run the main loop function of the matrix")
    Test3.test("Matrix.x_pos-=2","Move the line horizontally in the matrix")
    Test3.test("Matrix.loop_func()","Run the main loop function of the matrix")
    Test3.test("Matrix.x_pos+=1","Reset the line's position")
    Test3.test("Matrix.y_pos+=1","Move the line vertically in the matrix")
    Test3.test("Matrix.y_pos-=2","Move the line vertically in the matrix")
    end = time.perf_counter()
    print(f"\033[35mCompleted in {end-start} seconds")
    Test3.results()

    #chatbot test
    ducky.wait(20)
    start = time.perf_counter()
    Test4 = Tester()

    inputs = ["hello there","bye"]
    outputs = ["Hello","Bye then"]
    Test4.test("chat=ducky.Chatbot(inputs,outputs)","Initialise a chatbot object")
    Test4.test("5/(chat.reply_test())","Test outputs")
    end = time.perf_counter()
    print(f"\033[35mCompleted in {end-start} seconds")
    Test4.results()
    #TODO add more tests for all the classes
    full_timer.stop()
    print(f"\033[35mCompleted all tests in {full_timer.elapsed()} seconds")
    print_average()
    print("\033[0m")
    average = Tester.average()
    if average < 100:
        print("Tests failed - Check output above.")
        exit(1)
    else:
        exit(0)