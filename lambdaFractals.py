import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from math import sqrt

def cantorLambda(expr, start=0, length=1, ax=None, height=None):
    if height is None:
        cantorLambda(expr, start=start, length=length, ax=ax, height=length/15)
    else:
        if isinstance(expr, list):
            if expr[0] == 'lambda':
                ax.add_patch(Polygon([(start+(length/3), 0), (start+(length/3), height), (start+(length*2/3), height), (start+(length*2/3), 0)], facecolor='k'))
                cantorLambda(expr[1], start=start, length=length/3, ax=ax, height=height)
                cantorLambda(expr[2], start=start+(length*2/3), length=length/3, ax=ax, height=height)
            elif expr[0] == 'apply':
                ax.add_patch(Polygon([(start+(length/3), 0), (start+(length/3), height), (start+(length*2/3), height), (start+(length*2/3), 0)], facecolor='tab:gray'))
                cantorLambda(expr[1], start=start, length=length/3, ax=ax, height=height)
                cantorLambda(expr[2], start=start+(length*2/3), length=length/3, ax=ax, height=height)
        elif isinstance(expr, str):
            ax.add_patch(Polygon([(start,0), (start,height), (start+length, height), (start+length, 0)], facecolor=expr))      

def sierpinskiLambda(expr, start=0, length=1, ax=None):
    if isinstance(expr, list):
        if expr[0] == 'lambda':
            ax.add_patch(Polygon([(start+(length/4),(length/4)*sqrt(3)), (start+(length/2),(length/2)*sqrt(3)), (start+(3*length/4),(length/4)*sqrt(3)),], facecolor='k'))
            sierpinskiLambda(expr[1], start=start, length=length/2, ax=ax)
            sierpinskiLambda(expr[2], start=start+(length/2), length=length/2, ax=ax)
        elif expr[0] == 'apply':
            ax.add_patch(Polygon([(start+(length/4),(length/4)*sqrt(3)), (start+(length/2),(length/2)*sqrt(3)), (start+(3*length/4),(length/4)*sqrt(3)),], facecolor='tab:gray'))
            sierpinskiLambda(expr[1], start=start, length=length/2, ax=ax)
            sierpinskiLambda(expr[2], start=start+(length/2), length=length/2, ax=ax)
    elif isinstance(expr, str):
        ax.add_patch(Polygon([(start,0), (start+(length/2),(length/2)*sqrt(3)), (start+length, 0),], facecolor=expr)) 

def fractalLambdaPlot(expr, start=0, length=1, plotFunc=sierpinskiLambda):
    _, ax=plt.subplots()
    plotFunc(expr=expr, start=start, length=length, ax=ax)
    plt.axis('equal')
    plt.show()

fractalLambdaPlot(['apply', 'b', ['lambda', 'g', 'y']])

#todo: beta reduction
#todo: legend
#todo: automatic colors