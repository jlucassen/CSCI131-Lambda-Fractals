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

def oneBetaReduction(expr):
    if isinstance(expr, list):
        if expr[0] == 'apply' and expr[1][0] == 'lambda':
            return deepSubstitute(expr[1][1], expr[1][2], expr[2])
        betaReduceFirst = [expr[0], oneBetaReduction(expr[1]), expr[2]]
        if betaReduceFirst != expr:
            return betaReduceFirst
        betaReduceSecond = [expr[0], expr[1], oneBetaReduction(expr[2])]
        if betaReduceSecond != expr:
            return betaReduceSecond
    return expr

def deepSubstitute(old, expr, new):
    if isinstance(expr, str) and expr == old:
        return new
    elif isinstance(expr, list):
        out = expr.copy()
        for i in range(len(expr)):
            if isinstance(expr[i], str) and expr[i] == old:
                out[i] = new
            if isinstance(expr[i], list):
                out[i] = deepSubstitute(old, out[i], new)
        return out

def visualBetaReduction(expr, start=0, length=1, plotFunc=sierpinskiLambda, depthLimit = 10):
    current = expr.copy()
    depth = 0
    while depth < depthLimit:
        if current == oneBetaReduction(current):
            break
        print(current)
        fractalLambdaPlot(expr=current, start=start, length=length, plotFunc=plotFunc)
        current = oneBetaReduction(current)    
        depth += 1    

visualBetaReduction(['apply', ['lambda', 'b', ['apply', 'b', ['apply', 'b', 'b']]], ['lambda', 'b', ['apply', 'b', ['apply', 'b', 'b']]]], plotFunc=cantorLambda)

#todo: legend
#todo: automatic colors