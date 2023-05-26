import numpy as np
def mathtext_update(graph, x, y, z):
    global pagesource
    xt = str(np.abs(x))
    yt = str(np.abs(y))
    zt = str(np.abs(z))
    value = ""

    if graph == "line":
        if x == 0 and y == 0 and z == 1:
            value = "f(x) = x"
        if x == 0 and y > 0 and z == 1:
            value = f"f(x) = x + {yt}"
        if x == 0 and y < 0 and z == 1:
            value = f"f(x) = x - {yt}"
        if x > 0 and y == 0 and z == 1:
            value = f"f(x) = x - {xt}"
        if x < 0 and y == 0 and z == 1:
            value = f"f(x) = x + {xt}"
        if x < 0 and y > 0 and z == 1:
            value = f"f(x) = x + {str(np.abs(x) + y)}"
        if x > 0 and y < 0 and z == 1:
            value = f"f(x) = x - {str(np.abs(x) + np.abs(y))}"
        if (x < 0 and y < 0 and z == 1) or (x > 0 and y > 0 and z == 1):
            if x < y:
                value = f"f(x) = x - {str(np.abs(x + y))}"
            else:
                value = f"f(x) = x + {str(np.abs(x + y))}"

    elif graph == "cubic":
        if x == 0 and y == 0 and z == 1:
            value = "f(x) = x^2"
        if x == 0 and y > 0 and z == 1:
            value = f"f(x) = x^2 + {yt}"
        if x == 0 and y < 0 and z == 1:
            value = f"f(x) = x^2 - {yt}"
        if x > 0 and y == 0 and z == 1:
            value = f"f(x) = (x - {xt})^2"
        if x < 0 and y == 0 and z == 1:
            value = f"f(x) = (x + {xt})^2"
        if x > 0 and y > 0 and z == 1:
            value = f"f(x) = (x - {xt})^2 + {yt}"
        if x > 0 > y and z == 1:
            value = f"f(x) = (x - {xt})^2 - {yt}"
        if x < 0 < y and z == 1:
            value = f"f(x) = (x + {xt})^2 + {yt}"
        if x < 0 and y < 0 and z == 1:
            value = f"f(x) = (x + {xt})^2 - {yt}"

    elif graph == "quadro":
        if x == 0 and y == 0 and z == 1:
            value = "f(x) = x^3"
        if x == 0 and y > 0 and z == 1:
            value = f"f(x) = x^3 + {yt}"
        if x == 0 and y < 0 and z == 1:
            value = f"f(x) = x^3 - {yt}"
        if x > 0 and y == 0 and z == 1:
            value = f"f(x) = (x - {xt})^3"
        if x < 0 and y == 0 and z == 1:
            value = f"f(x) = (x + {xt})^3"
        if x > 0 and y > 0 and z == 1:
            value = f"f(x) = (x - {xt})^3 + {yt}"
        if x > 0 > y and z == 1:
            value = f"f(x) = (x - {xt})^3 - {yt}"
        if x < 0 < y and z == 1:
            value = f"f(x) = (x + {xt})^3 + {yt}"
        if x < 0 and y < 0 and z == 1:
            value = f"f(x) = (x + {xt})^3 - {yt}"

    pagesource = f"""
                <html><head>
                <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-AMS-MML_HTMLorMML">                     
                </script></head>
                <body>
                <p><mathjax style="font-size:2em">$${value}$$</mathjax></p>
                </body></html>
                """

    return pagesource