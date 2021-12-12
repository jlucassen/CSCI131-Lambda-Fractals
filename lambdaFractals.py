import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from math import sqrt
import random

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

def rulerLambda(expr, start=0, length=1, ax=None):
    if isinstance(expr, list):
        if expr[0] == 'lambda':
            ax.add_patch(Polygon([(start+(length*7/15),length/4), (start+(length*7/15),-length/4), (start+(length*8/15),-length/4), (start+(length*8/15),length/4),], facecolor='k'))
            rulerLambda(expr[1], start=start, length=length*7/15, ax=ax)
            rulerLambda(expr[2], start=start+length*8/15, length=length*7/15, ax=ax)
        elif expr[0] == 'apply':
            ax.add_patch(Polygon([(start+(length*7/15),length/4), (start+(length*7/15),-length/4), (start+(length*8/15),-length/4), (start+(length*8/15),length/4),], facecolor='tab:gray'))
            rulerLambda(expr[1], start=start, length=length*7/15, ax=ax)
            rulerLambda(expr[2], start=start+length*8/15, length=length*7/15, ax=ax)
    elif isinstance(expr, str):
        ax.add_patch(Polygon([(start,length/9), (start,-length/9), (start+length, -length/9), (start+length, length/9)], facecolor=expr))   

def oneBetaReduction(expr):
    if isinstance(expr, list):
        if expr[0] == 'apply' and isinstance(expr[1], list) and expr[1][0] == 'lambda':
            return deepSubstitute(expr[1][1], expr[1][2], expr[2], uniform=False)
        betaReduceFirst = [expr[0], oneBetaReduction(expr[1]), expr[2]]
        if betaReduceFirst != expr:
            return betaReduceFirst
        betaReduceSecond = [expr[0], expr[1], oneBetaReduction(expr[2])]
        if betaReduceSecond != expr:
            return betaReduceSecond
    return expr

def deepSubstitute(old, expr, new, uniform=True):
    if isinstance(expr, str) and expr == old:
        return new
    elif isinstance(expr, list):
        out = expr.copy()
        for i in range(len(expr)):
            if isinstance(expr[i], str) and expr[i] == old:
                if uniform:
                    out[i] = new
                else:
                    out[i] = alphafy(new)
            if isinstance(expr[i], list):
                out[i] = deepSubstitute(old, out[i], new)
        return out

def alphafy(expr):
    if isinstance(expr, list):
        out = expr.copy()
        if out[0] == 'lambda':
            out = deepSubstitute(out[1], out, "#%06x" % random.randint(0, 0xFFFFFF))
        out[1] = alphafy(out[1])
        out[2] = alphafy(out[2])
        return out
    return expr

def fractalLambdaPlot(expr, plotFunc=sierpinskiLambda):
    _, ax=plt.subplots()
    plotFunc(expr=alphafy(expr), ax=ax)
    plt.axis('equal')
    plt.show()

def visualBetaReduction(expr, plotFunc=sierpinskiLambda, depthLimit = 5):
    current = alphafy(expr.copy())
    depth = 0
    while depth < depthLimit:
        print(current)
        _, ax=plt.subplots()
        plotFunc(expr=current, ax=ax)
        plt.axis('equal')
        plt.show()
        if current == oneBetaReduction(current):
            break
        current = oneBetaReduction(current)    
        depth += 1    

fractalLambdaPlot(['lambda', 'x', 'x'], plotFunc=cantorLambda) # \x.x
fractalLambdaPlot(['lambda', 'x', ['lambda', 'y', 'x']], plotFunc=sierpinskiLambda) # \x.\y.x
fractalLambdaPlot(['lambda', 'x', ['lambda', 'y', 'y']], plotFunc=rulerLambda) # \x.\y.y
#fractalLambdaPlot(['lambda', 'x', ['lambda', 'y', ['lambda', 'w', ['apply', ['apply', 'x', 'w'], 'y']]]], plotFunc=cantorLambda) # \x.\y.\z.((xz)y)
#fractalLambdaPlot(['lambda', 'x', ['lambda', 'x', 'x']], plotFunc=sierpinskiLambda) # \x.\x.x
#fractalLambdaPlot(['lambda', 'x', ['apply', ['lambda', 'y', ['apply', 'x', ['apply', 'y', 'y']]], ['lambda', 'y', ['apply', 'x', ['apply', 'y', 'y']]]]], plotFunc=rulerLambda) # Y combinator

#visualBetaReduction(['apply', ['lambda', 'x', ['lambda', 'y', 'x']], ['lambda', 'x', 'x']], plotFunc=cantorLambda) # evaluate (\x.\y.x)(\x.x)
#visualBetaReduction(['apply', ['lambda', 'x', ['apply', 'x', 'x']], ['lambda', 'x', ['apply', 'x', 'x']]], plotFunc=sierpinskiLambda) # evaluate (\x.xx)(\x.xx) 

lambdaTrue = ['lambda', 'x', ['lambda', 'y', 'x']]
lambdaFalse = ['lambda', 'x', ['lambda', 'y', 'y']]
lambdaNot = ['lambda', 'w', ['apply', ['apply', 'w', lambdaFalse], lambdaTrue]]
lambdaAnd = ['lambda', 'w', ['lambda', 'z', ['apply', ['apply', 'w', 'z'], lambdaFalse]]]
lambdaOr = ['lambda', 'w', ['lambda', 'z', ['apply', ['apply', 'w', lambdaTrue], 'z']]]
booleanExpr = ['apply', ['apply', lambdaOr, lambdaFalse], ['apply', ['apply', lambdaAnd, lambdaTrue], ['apply', lambdaNot, lambdaFalse]]] # translate ((Or False) ((And True) (Not False)))
visualBetaReduction(booleanExpr, plotFunc=rulerLambda, depthLimit=20) # evaluate

visualBetaReduction(['apply', ['lambda', 'y', ['apply', 'y', ['apply', 'y', 'y']]], ['lambda', 'y', ['apply', 'y', ['apply', 'y', 'y']]]], plotFunc=cantorLambda)
visualBetaReduction(['apply', ['lambda', 'y', ['apply', 'y', ['apply', 'y', 'y']]], ['lambda', 'y', ['apply', 'y', ['apply', 'y', 'y']]]], plotFunc=sierpinskiLambda)
visualBetaReduction(['apply', ['lambda', 'y', ['apply', 'y', ['apply', 'y', 'y']]], ['lambda', 'y', ['apply', 'y', ['apply', 'y', 'y']]]], plotFunc=rulerLambda)