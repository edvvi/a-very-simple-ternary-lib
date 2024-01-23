import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrow
from numpy import linspace, array, dot, matmul, sqrt, random, floor
from scipy.integrate import odeint

class Solver:    
    def __init__(self):      
        self._x0, self._x1, self._x2 = [],[],[]

    def solve(self, A, total_time, X0):
        file = open("data.txt","w")
        e = array([[1,0,0],[0,1,0], [0,0,1]])

        def diffeqs(X, t):    
            #replicator equations
            dx0dt = X[0]*(dot(e[0], matmul(A,X))-dot(X,matmul(A,X)))
            dx1dt = X[1]*(dot(e[1], matmul(A,X))-dot(X,matmul(A,X)))
            dx2dt = X[2]*(dot(e[2], matmul(A,X))-dot(X,matmul(A,X)))
            return [dx0dt, dx1dt, dx2dt]
    
        t = linspace(0,total_time,total_time*100)

        #solving the diff eqs with scipy's odeint
        S = odeint(diffeqs, X0, t)                                           

        #extracting the solutions
        self._x0 = S[:,0]
        self._x1 = S[:,1]
        self._x2 = S[:,2]

        #write solution on a file
        for i in range(0, len(self._x0)):
            file.write("{:.6f} {:.6f} {:.6f}\n".format(self._x0[i], self._x1[i], self._x2[i]))
        file.close()

    #return results as a tuple
    def get_results(self):
        return (self._x0, self._x1, self._x2)

class Plotter:
    def __init__(self, gameTitle, strategies):
        self.strategies = strategies
        self.gameTitle = gameTitle
        self._fig, self._ax = plt.subplots()

    #vertices of the equilateral triangle
    _vertices = [[0,0], [1,0], [0.5, sqrt(3)/2], [0,0]]
    #creates a tuple of [0,0] -> (x, y)
    _vx, _vy = zip(*_vertices) 
 
    #just two different size fonts
    _font1 = {'family': 'serif',
                'color':  'black',
                'weight': 'normal',
                'size': 16,
            }
    _font2 = {'family': 'serif',
                'color':  'black',
                'weight': 'normal',
                'size': 13,
            }            
    
    #conversion to cartesian
    def __to_xy(self, a,b,c):
        return ((float(a)+1-float(b))/2, (sqrt(3)/2)*float(c))

    def dot(self, a, b, c, **kwargs):  
        defaultKwargs = {'dot_size': 5, 
                        'dot_color':  'black',
                        'dot_border_color': 'black'}  
                   
        kwargs = { **defaultKwargs, **kwargs }   
        x = self.__to_xy(a,b,c)[0]
        y = self.__to_xy(a,b,c)[1]

        self._ax.plot(x, y, marker="o", markersize=kwargs['dot_size'], 
                      markeredgecolor=kwargs['dot_border_color'], markerfacecolor=kwargs['dot_color'])


    def plot(self, *args, **kwargs):
        #placeholder code --------------------------------------------------------
        x = []
        y = [] 

        #transform from triangular to cartesian
        #read text file
        if len(args) == 1:
            for line in args[0].readlines():
                aux = line.split()                
                x.append(self.__to_xy(aux[0], aux[1], aux[2])[0])
                y.append(self.__to_xy(aux[0], aux[1], aux[2])[1])
            args[0].close()  
        #read lists
        elif len(args) > 1:
            for i in range(len(args[0])):
                x.append(self.__to_xy(args[0][i], args[1][i], args[2][i])[0])
                y.append(self.__to_xy(args[0][i], args[1][i], args[2][i])[1])   
        
        #if args is empty assums data.txt exist and open it
        elif len(args) == 0:
                file = open("data.txt", "r")
                for line in file.readlines():
                    aux = line.split()
                    x.append(self.__to_xy(aux[0], aux[1], aux[2])[0])
                    y.append(self.__to_xy(aux[0], aux[1], aux[2])[1])
                file.close()
        
        #kwargs definitions
        defaultKwargs = {'line_color': 'black', 
                        'line_width':  1.3,
                        'arrow_pos': int(len(x)/2)}  
                   
        kwargs = { **defaultKwargs, **kwargs }

        #plot the actual data
        self._ax.plot(x, y, color = kwargs['line_color'], linewidth = kwargs['line_width'])
        k = kwargs['arrow_pos']

        arrow = FancyArrow(x[k], y[k], x[k+1]-x[k], y[k+1]-y[k], 
                shape='full', lw=0, length_includes_head=True, head_length=None, width=0, 
                head_width=.025, head_starts_at_zero=True, facecolor=kwargs['line_color'])
        self._ax.add_patch(arrow)     
        #---------------------------------------------------------------------------------

    def set_triangular_axis(self, **kwargs):     

        #more kwargs definitions           
        defaultKwargs = {'triangle_color': 'black', 
                        'triangle_line_width': 2,
                        'show_title': False,
                        'left_label_xpos': 0,
                        'top_label_xpos': 0,
                        'right_label_xpos': 0}                
        kwargs = { **defaultKwargs, **kwargs } 

        plt.axis('off')
        
        #the title is turned off by default
        if kwargs['show_title']: self._ax.set_title(self.gameTitle, loc="center", **self._font1)

        #plot the triangular axis
        self._ax.plot(self._vx,self._vy, color = kwargs['triangle_color'], linewidth = kwargs['triangle_line_width']) 
    
        #draw the strategy labels
        self._ax.text(1.0+kwargs['right_label_xpos'], -0.05, self.strategies[0], 
                     horizontalalignment = 'center', **self._font2)
        self._ax.text(kwargs['left_label_xpos'],-0.05, self.strategies[1],
                     horizontalalignment = 'center', **self._font2)
        self._ax.text(0.5+kwargs['top_label_xpos'], sqrt(3)/2+0.02, self.strategies[2],
                     horizontalalignment = 'center', **self._font2)
       
    def show(self, *args):  
        if len(args) == 0:
            ndpi = 300
        else:
            ndpi=args[0]
        plt.savefig(self.gameTitle+".png", bbox_inches='tight', dpi=ndpi)
        plt.show()   


'''
REFERENCES

[1] Toshiaki Shimura, Anthony I.S. Kemp; 
Tetrahedral plot diagram: A geometrical solution for quaternary systems. 
American Mineralogist 2015;; 100 (11-12): 2545–2547. doi: https://doi.org/10.2138/am-2015-5371

[2] https://mathworld.wolfram.com/TernaryDiagram.html

[3] https://en.wikipedia.org/wiki/Ternary_plot

'''
