import random, time, os, nltk, tkinter as TK, types, math, inspect, sys, requests, json, ast, logging, abc, gymnasium
from os.path import isfile, split, join
from copy import deepcopy
from tkinter import simpledialog
from turtle import Turtle
from nltk.tokenize import word_tokenize
from ducky.backend import backend
from nltk.stem import LancasterStemmer

#matrix functions

def matrix(x,y,fill=0):
    mat = [[fill for _ in range(x)] for _ in range(y)]
    return mat

def draw(mat,x,y,val=1,errors=True):
    """draws a certain value to all specified positions"""
    if len(x) == len(y):
        try:
            for i,x_pos in enumerate(x):
                mat[y[i]][x_pos] = val
        except (ValueError,IndexError) as e:
            if errors:
                print(e)
    else:
        print(f"Lengths aren't equal: Mat Rows: {len(mat)}, X: {len(x)}, Y: {len(y)}")
    return mat

def scan(mat,condition=1):
    """returns all locations that meet a certain condition"""
    x = []
    y = []
    for y_index,Y in enumerate(mat):
        for x_index,X in enumerate(mat[y_index]):
            if X == condition:
                x.append(x_index)
                y.append(y_index)
    return x,y

def shift(mat,x,y,x_shift,y_shift=0):
    """shifts a matrix by a certain x and y distance"""
    y_size = len(mat)
    x_size = len(mat[0])
    
    new_x = []
    new_y = []
    
    if len(x) == len(y):
        for i in range(len(x)):
            nx = x[i] + x_shift
            ny = y[i] + y_shift
            
            if 0 <= nx < x_size and 0 <= ny < y_size:
                new_x.append(nx)
                new_y.append(ny)
                
    return new_x, new_y

def move(mat,x_move,y_move=0,condition_scan=1,blank_clear=0):
    """uses shift function to move an image stored in a matrix"""
    x, y = scan(mat,condition=condition_scan)
    new_x, new_y = shift(mat, x, y, x_shift=x_move, y_shift=y_move)
    mat = clear_matrix(mat,blank=blank_clear)
    mat = draw(mat, new_x, new_y,val=condition_scan)
    return mat

def clear_matrix(mat,blank=0):
    """clears a matrix using a custom blank value"""
    for Y in range(len(mat)):
        for X in range(len(mat[Y])):
            mat[Y][X] = blank
    return mat

def render(mat):
    """renders a matrix to console"""
    for row in mat:
        print(" ".join(str(cell) for cell in row))
    print("------------------------------------------------------")
    
#my functions

def download_nltk():
    """downloads nltk resources"""
    nltk.download('punkt', quiet=True)

def download_to_path(url, path, file_name, quiet=False):
    """downloads a file"""
    try:
        r = requests.get(url)
        r.raise_for_status()
        with open(f"{path}/{file_name}", "wb") as f:
            f.write(r.content)
    except requests.exceptions.RequestException as e:
        if not quiet:
            print("Download failed:", e)

def low_ram_download(url,path,file_name,quiet=False):
    """downloads a file using less ram"""
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(f"{path}/{file_name}", "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
    except requests.exceptions.RequestException as e:
        if not quiet:
            print("Download failed:", e)

def rand_int(minimum,maximum):
    """returns a random integer within certain bounds"""
    return random.randint(minimum,maximum)

def choose(list_input):
    """chooses a random item from a list"""
    return random.choice(list_input)

def wait(ms):
    """waits a certain amount of time in milliseconds"""
    time.sleep(ms/1000)
    
def current_hour():
    """returns the current hour"""
    return time.localtime()[3]

def current_minute():
    """returns the current minute"""
    return time.localtime()[4]

def current_second():
    """returns the current second"""
    return time.localtime()[5]
    
def tokenise(string):
    """tokenises a word"""
    tokens = word_tokenize(string)
    return tokens

def stem(string):
    """returns the stem of a word"""
    lancaster = LancasterStemmer()
    return lancaster.stem(string)
    
def array(lst):
    """returns an array of a list"""
    return backend().array(lst)

def dot_product(mat1,mat2):
    """returns the dot product of two values"""
    return backend().dot(mat1,mat2)

def scale_matrix(mat,val):
    """scales a matrix by a certain value"""
    return mat*val

def average_matrix(mat):
    """averages a matrix"""
    return backend().average(mat)

def calc(param):
    """calculates a mathematical expression"""
    try:
        return ast.literal_eval(param)
    except (ValueError,SyntaxError) as e:
        logging.error(f"Error evaluating expression: {e}")
        return e

def find_total(number,condition=None):
    """adds all numbers below it that meet a certain condition"""
    if number < 1:
        return 0
    total = 0
    for n in range(1, number + 1):
        if condition is None or condition(n):
            total += n
    return total
    
def ask_url(url):
    """sends a get request to a url"""
    return requests.get(url)

def ask_json(url):
    """sends a get request to a url and returns it in json format"""
    return requests.get(url).json()

def get_coords():
    """gets the coordinates of the user using ip"""
    response = requests.get("https://ipinfo.io/json", timeout=5)
    response.raise_for_status()
    data = response.json()
    loc = data.get("loc")  # "lat,lon"
    if loc:
        lat, lon = map(float, loc.split(","))
        return lat, lon
    return None

def get_time():
    """returns a time.perf_counter object"""
    return time.perf_counter()

#my decorators

def time_function(func):
    """times the execution time of a function"""
    def wrapper(*args, **kwargs):
        start = get_time()
        result = func(*args, **kwargs)
        end = get_time()
        execution_time = end - start
        return result, execution_time
    return wrapper

def repeat(times):
    """repeats a function a certain number of times"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(times):
                result = func(*args, **kwargs)
                results.append(result)
            return results
        return wrapper
    return decorator

def modify(func,modifier):
    """modifies a function"""
    return modifier(func())

#classes

class Tester:
    _instances = []
    @classmethod
    def average(cls):
        total_success = 0
        total_errors = 0
        for instance in cls._instances:
            total_success += len(instance.success)
            total_errors += len(instance.errors)
        total_tests = total_success + total_errors
        if total_tests == 0:
            return 0
        return (total_success / total_tests) * 100

    @classmethod
    def fails(cls):
        errors = []
        for instance in cls._instances:
            errors.append(instance.errors)
            return errors if len(errors) > 0 else None

    def __init__(self):
        self.instance_val = len(self._instances) + 1
        self.errors = []
        self.success = []
        Tester._instances.append(self)
        print("\033[0m")

    def test(self,code, name="Unnamed"):
        try:
            exec(code, globals())
            self.success.append(name)
            print(f"\033[32mCode:\n{code}\n({name}) executed successfully\n")

        except Exception as error:
            print(f"\033[31m{error}")
            print(f"\033[31m{code}\n")
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
            print(f"\033[91mCompleted {percent}% successfully:\n")
        if self.success:
            print(f"\033[32mSuccessful tests:")
        for s in self.success:
            print(f"\033[32m{s}")
        if len(self.errors) > 0:
            print(f"\n\033[31mFailed tests:")
        for e in self.errors:
            print(f"\033[31m{e}")


class MatrixManager:
    def __init__(self,background,fps,mat=None,wrapping=False,sprite_condition=1):
        self.mat = mat
        self.fps = fps
        self.x = None
        self.y = None
        self.sprite_condition = sprite_condition
        self.wrapping = wrapping
        self.background = background
        self.scan_mat()
        self.x_pos = 0
        self.y_pos = 0
    def make_matrix(self,x,y,value=0):
        self.mat = matrix(x,y,value)
        
    def scan_mat(self):
        if self.mat:
            self.x,self.y = scan(self.mat,self.sprite_condition)
            
    def modify_matrix(self,x,y,val):
        self.mat[y][x] = val
        
    def self_render(self,t_x,t_y,printing=True,sprite_cond=1):
        draw(self.background,t_x,t_y,val=sprite_cond)
        if printing:
            render(self.background)
            
    def loop_func(self,rendering=True,clearing=True):
        temp_x = [x for x in self.x]
        temp_y = [y for y in self.y]
        if clearing:
            clear_matrix(self.background)
        for i in range(len(temp_x)):
            temp_x[i] += self.x_pos
        for i in range(len(temp_y)):
            temp_y[i] -= self.y_pos
        if self.wrapping:
            for i in range(len(temp_x)):
                temp_x[i] = temp_x[i] % len(self.background[0]) #wrap horizontally
            for i in range(len(temp_y)):
                temp_y[i] = temp_y[i] % len(self.background) #wrap vertically
        self.self_render(temp_x,temp_y,printing=rendering,sprite_cond=self.sprite_condition)
        wait(1000/self.fps)


class Manage:
    def __init__(self, file, action):
        self.file = file
        self.action = action
        self.text = None
        if self.action.lower() == "write":
            self.write_to_file()
        elif self.action.lower() == "read":
            self.text = self.read_from_file()
        elif self.action.lower() == "append":
            self.append_to_file()
        elif self.action.lower() == "delete":
            self.delete_a_file()
        else:
            print("Error, invalid choice:\n")
    def write_to_file(self):
        try:
            with open(self.file,"w") as file:
                file.write(input(f"What do you want to write to the file?\n"))
        except Exception as e:
            logging.error(f"Failed to write to {self.file}: {e}")

    def append_to_file(self):
        try:
            with open(self.file,"a") as file:
                file.write(input(f"What do you want to append to the file?\n"))
        except Exception as e:
            logging.error(f"Failed to append to {self.file}: {e}")
            return None

    def delete_a_file(self):
        if input("Are you sure ('y') ?:\n") == "y":
            os.remove(self.file)
    def read_from_file(self):
        try:
            with open(self.file,"r") as file:
                return file.read()
        except Exception as e:
            logging.error(f"Failed to read from {self.file}: {e}")
            return None


class TurtleManager:
    def __init__(self,turtle,colours=None):
        self.turtle = turtle
        self.x = self.turtle.xcor()
        self.y = self.turtle.xcor()
        self.width = self.turtle.width()
        self.pen_down = self.turtle.isdown()
        self.rotation = self.turtle.heading()
        self.colours = colours
        if not self.colours:
            self.colours = ["red","green","blue","yellow","white","black","green","purple"]

    def colour(self,name=None,index=None):
        if index:
            self.turtle.pencolor(self.colours[index])
        else:
            self.turtle.pencolor(name)

    def update(self):
        self.width = self.turtle.width()
        self.rotation = self.turtle.heading()
        self.x = self.turtle.xcor()
        self.y = self.turtle.xcor()
        self.pen_down = self.turtle.isdown()

    def change(self,x=False,y=False,rotation=False,rotation_val=None,width=False,width_val=None,pen_state=False):
        if x and y:
            if self.pen_down:
                self.turtle.penup()
                self.turtle.goto(self.x, self.y)
                self.turtle.pendown()
            else:
                self.turtle.goto(self.x, self.y)

        if rotation and rotation_val is not None:
            self.turtle.setheading(rotation_val)

        if pen_state:
            if self.pen_down:
                self.turtle.penup()
            else:
                self.turtle.pendown()
        if width and width_val is not None:
            self.turtle.width(width_val)

#unfinished chatbot
            
class Chatbot:
    def __init__(self,testing_input=None,testing_output=None):
        self.greetings = None
        self.farewells = None
        self.time = None
        self.help = None
        self.location = None
        self.user_input = None
        self.testing_input = testing_input
        self.testing_output = testing_output
        self.build()

    def build(self):
        self.greetings = ["hi","hello","meet","morn","afternoon","hey"]
        self.farewells = ["bye","see","lat","goodby"]
        self.time = ["tim","now","clock"]
        self.help = ["assist","help","nee"]
        self.location = ["wher","loc"]

    def run(self):
        self.user_input = ""
        score = [0,0,0,0,0]
        while self.user_input != "exit":
            self.user_input = input("You:\t")
            print(self.reply(self.user_input))

    def reply(self,reply_input):
        score = [0, 0, 0, 0, 0]
        tokens = tokenise(reply_input)
        stemmed_words = []
        for token in tokens:
            stemmed_words.append((stem(token)))
        for word in stemmed_words:
            if word in self.greetings:
                score[0] += 1
            elif word in self.farewells:
                score[1] += 1
            elif word in self.time:
                score[2] += 3
            elif word in self.help:
                score[3] += 2
            elif word in self.location:
                score[4] += 3
        if score[0] > score[1] and score[0] > score[2] and score[0] > score[3] and score[0] > score[4]:
            return "Hello"
        elif score[1] > score[0] and score[1] > score[2] and score[1] > score[3] and score[1] > score[4]:
            return "Bye then"
        elif score[2] > score[0] and score[2] > score[1] and score[2] > score[3] and score[2] > score[4]:
            return f"{current_hour()}:{current_minute()}:{current_second()}"
        elif score[3] > score[0] and score[3] > score[1] and score[3] > score[2] and score[3] > score[4]:
            return "How may I assist you?"
        elif score[4] > score[0] and score[4] > score[1] and score[4] > score[2] and score[4] > score[3]:
            return f"Your current coordinates are:\n{get_coords()}"
        return None

    def reply_test(self):
        if self.testing_input and self.testing_output and len(self.testing_input) == len(self.testing_output):
            for test in range(len(self.testing_input)):
                if self.reply(self.testing_input[test]) != self.testing_output[test]:
                    return 0
            return 1
        return None


#AI class templates

import abc
import random

import ducky
import numpy
import numpy


class ActivationFunctions:
    TANH = 0

    @staticmethod
    def __tanh(x: numpy.ndarray):
        return numpy.tanh(x)

    @staticmethod
    def __tanh_derived(x: numpy.ndarray):
        return 1 - (numpy.tanh(x) ** 2)

    @staticmethod
    def use_tanh():
        return ActivationFunctions.TANH, ActivationFunctions.__tanh, ActivationFunctions.__tanh_derived


class CostFunctions:
    MSE = 0

    @staticmethod
    def __mse(actual: numpy.ndarray, prediction: numpy.ndarray):
        return numpy.mean(numpy.power(actual - prediction, 2))

    @staticmethod
    def __mse_derived(actual: numpy.ndarray, prediction: numpy.ndarray):
        return (2 * (prediction - actual)) / actual.size

    @staticmethod
    def use_mse():
        return CostFunctions.MSE, CostFunctions.__mse, CostFunctions.__mse_derived


class Layer(abc.ABC):
    def __init__(self):
        self.input = None
        self.output = None

    @abc.abstractmethod
    def feed_forward(self, input_values: numpy.ndarray):
        pass

    @abc.abstractmethod
    def back_propagate(self, output_error: numpy.ndarray, learning_rate: float):
        pass

    @abc.abstractmethod
    def copy(self):
        pass


class FullyConnectedLayer(Layer):
    def __init__(self, input_size: int, output_size: int):
        Layer.__init__(self)
        random_bound = 1.0 / numpy.sqrt(input_size)
        self.weights = numpy.random.uniform(-random_bound, random_bound, (input_size, output_size))
        self.bias = numpy.zeros((1, output_size))
        self.input_size = input_size
        self.output_size = output_size

    def feed_forward(self, input_values):
        self.input = input_values
        self.output = numpy.dot(self.input, self.weights) + self.bias
        return self.output

    def back_propagate(self, output_error, learning_rate):
        input_error = numpy.dot(output_error, self.weights.T)
        weights_error = numpy.dot(self.input.T, output_error)
        self.weights -= (learning_rate * weights_error)
        self.bias -= (learning_rate * numpy.mean(output_error, axis=0, keepdims=True))
        return input_error

    def copy(self):
        copied_layer = FullyConnectedLayer(self.input_size, self.output_size)
        weights = self.weights.copy()
        bias = self.bias.copy()
        copied_layer.weights = weights
        copied_layer.bias = bias
        return copied_layer


class ActivationLayer(Layer):
    def __init__(self, activation_id, activation, activation_derived):
        Layer.__init__(self)
        self.activation_id = activation_id
        self.activation = activation
        self.activation_derived = activation_derived

    def feed_forward(self, input_values):
        self.input = input_values
        self.output = self.activation(self.input)
        return self.output

    def back_propagate(self, output_error, learning_rate):
        return self.activation_derived(self.input) * output_error

    def copy(self):
        copied_layer = ActivationLayer(self.activation_id, self.activation, self.activation_derived)
        return copied_layer


class NeuralNetwork:
    def __init__(self, cost_function_id, cost_function, cost_function_derived):
        self.layers = []
        self.cost_function_id = cost_function_id
        self.cost_function = cost_function
        self.cost_function_derived = cost_function_derived

    def add_layer(self, layer):
        self.layers.append(layer)

    def predict(self, input_data):
        output = input_data
        for layer in self.layers:
            output = layer.feed_forward(output)
        return output

    def train(self, train_input, train_output, n_epochs, batch_size, learning_rate):
        for epoch in range(n_epochs):
            batch_index = 0
            while batch_index < train_input.shape[0]:
                if batch_index + batch_size < train_input.shape[0]:
                    output = train_input[batch_index:batch_index + batch_size, ]
                    actual = train_output[batch_index:batch_index + batch_size, ]
                else:
                    output = train_input[batch_index:, ]
                    actual = train_output[batch_index:, ]
                for layer in self.layers:
                    output = layer.feed_forward(output)
                cost = self.cost_function(actual, output)
                error = self.cost_function_derived(actual, output)
                for layer in reversed(self.layers):
                    error = layer.back_propagate(error, learning_rate)
                print(f"Epoch {epoch + 1}/{n_epochs} | Batch = {(batch_index + 1) * batch_size} | Cost = {cost}")
                batch_index += batch_size

    def save(self, file_path):
        with open(f"{file_path}.nn", "w") as save_file:
            save_file.write(f"{self.cost_function_id}\n")
            for index, layer in enumerate(self.layers):
                if isinstance(layer, FullyConnectedLayer):
                    save_file.write(f"{index}|F|{layer.weights.shape}|{layer.bias.shape}\n")
                    numpy.save(f"{file_path}_{index}_w", layer.weights)
                    numpy.save(f"{file_path}_{index}_b", layer.bias)
                elif isinstance(layer, ActivationLayer):
                    save_file.write(f"{index}|A|{layer.activation_id}\n")

    @staticmethod
    def load_from_file(file_path):
        with open(f"{file_path}.nn", "r") as load_file:
            lines = load_file.readlines()
        cost_function_id = int(lines[0])
        if cost_function_id == CostFunctions.MSE:
            neural_network = NeuralNetwork(*CostFunctions.use_mse())
        else:
            neural_network = NeuralNetwork(*CostFunctions.use_mse())
        for line in lines[1:]:
            if line != "":
                parts = line.split("|")
                if parts[1] == "F":
                    weights = numpy.load(f"{file_path}_{int(parts[0])}_w.npy")
                    bias = numpy.load(f"{file_path}_{int(parts[0])}_b.npy")
                    layer = FullyConnectedLayer(weights.shape[0], weights.shape[1])
                    layer.weights = weights
                    layer.bias = bias
                    neural_network.add_layer(layer)
                elif parts[1] == "A":
                    activation_id = int(parts[2])
                    if activation_id == ActivationFunctions.TANH:
                        neural_network.add_layer(ActivationLayer(*ActivationFunctions.use_tanh()))
                    else:
                        neural_network.add_layer(ActivationLayer(*ActivationFunctions.use_tanh()))
        return neural_network

    def copy_network(self):
        copied_network = NeuralNetwork(self.cost_function_id, self.cost_function, self.cost_function_derived)
        for layer in self.layers:
            copied_network.add_layer(layer.copy())
        return copied_network


class Agent:
    def __init__(self, gamma=0.99):
        self.gamma = gamma


class QTable:
    def __init__(self, state, actions):
        self.table = numpy.zeros((state,actions))
        self.actions = actions
        self.state = state

    def update_table(self, state_row, action, value):
        self.table[state_row, action] += value

    def get_action(self, state_row):
        return numpy.argmax(self.table[state_row])


class QTableAgent(Agent):
    def __init__(self, table, num_possible_values):
        Agent.__init__(self)
        self.table = table
        self.num_possible_values = num_possible_values
        self.epsilon = 1

    def state_to_row(self,state):
        return int("".join([str(s) for s in state.astype(int)]), self.num_possible_values)

    def predict(self, state):
        self.epsilon *= self.gamma
        if random.random() > self.epsilon:
            return self.table.get_action(self.state_to_row(state))
        else:
            return rand_int(0,self.table.actions-1)

    def train(self, state, action, reward):
        self.table.update_table(self.state_to_row(state), action, reward)


class DeepQAgent(Agent):
    def __init__(self, layer_sizes):
        Agent.__init__(self)
        self.memory = Memory()
        self.counter = 0
        try:
            self.neural_network = NeuralNetwork.load_from_file("deepq-nn")
        except FileNotFoundError:
            self.neural_network = NeuralNetwork(*CostFunctions.use_mse())
            for i, size in enumerate(layer_sizes[:-1]):
                self.neural_network.add_layer(FullyConnectedLayer(size, layer_sizes[i+1]))
                self.neural_network.add_layer(ActivationLayer(*ActivationFunctions.use_tanh()))

    def predict(self, state):
        return int(self.neural_network.predict(state)[0].argmax())

    def train(self, discount_rate):
        training_input_data = []
        training_output_data = []
        for i in range(len(self.memory.states)): #loops through a range the len of all states stored in Memory
            prediction = self.neural_network.predict(self.memory.states[i]) #makes a prediction on the current memory state being iterated over with the current neural network
            prediction[0] += self.memory.rewards[i - 1] #prediction is edited based on the reward from what the agent did in that state
            if i > 0:
                prediction[0] += self.memory.rewards[i-1] * discount_rate #updates prediction based on previous rewards
        training_input_data = numpy.array(training_input_data)
        training_output_data = numpy.array(training_output_data)
        self.neural_network.train(training_input_data, training_output_data, n_epochs=500, batch_size=10, learning_rate=0.1) #trains the neural network
        if self.counter >= 10:
            self.neural_network.save("deepq-nn") #saves neural network as deepq-nn
            self.counter = 0
        else:
            self.counter += 1

    def update_memory(self, state, action, reward):
        self.memory.update(state, action, reward) #appends a state, action and reward to the Memory instance variable's instance variables


class Memory:
    def __init__(self):
        """initialises a Memory object"""
        self.states = []
        self.actions = []
        self.rewards = []

    def update(self, state, action, reward):
        """appends a state, action and reward to instance variables"""
        self.states.append(state)
        self.actions.append(action)
        self.rewards.append(reward)

    def clear(self):
        """clears the instance variable lists of states, actions and rewards."""
        self.states = []
        self.actions = []
        self.rewards = []


#Customisable gymnasium env
class DuckEnv(gymnasium.Env, abc.ABC):
    def __init__(self, state_shape, num_actions):
        """initialises a gymnasium environment"""
        super().__init__() #gymnasium init
        self.action_space = spaces.Discrete(num_actions) #num of actions
        self.observation_space = spaces.Box(low=-numpy.inf, high=numpy.inf, shape=state_shape, dtype=numpy.float32) #state space

    def step(self, action):
        """gymnasium step function that uses user-defined functions"""
        next_state = self.on_action(action) #gets next state
        self.state = numpy.array(next_state, dtype=numpy.float32) #converts it into numpy arrray
        reward = self.get_reward() #gets user function for get_reward
        terminated = self.is_game_over() #checks for game_over
        truncated = False #to stop infinite loop in training by truncating training
        return self.state, reward, terminated, truncated, {} #returns gymnasium compatible format

    def reset(self, seed=None, options=None):
        """reset function"""
        super().reset(seed=seed)
        return self.on_reset(), {}

    @abc.abstractmethod
    def on_action(self, action):
        """user-defined function"""
        return self.state

    @abc.abstractmethod
    def get_reward(self):
        """user-defined function"""
        return 0

    @abc.abstractmethod
    def on_reset(self):
        """user-defined function"""
        return self.state

    @abc.abstractmethod
    def is_game_over(self):
        """user-defined function"""
        return False

#turtlel functions moved out of this module
#turtle also removed since it wasn't really doing much