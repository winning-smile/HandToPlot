import numpy as np
def mathtext_update(graph, x, y, z):
    global pagesource
    xt = str(np.abs(x))
    yt = str(np.abs(y))
    zt = str(np.abs(z))
    if graph == "line":
        if x == 0 and y == 0 and z == 1:
            pagesource = """
                        <html><head>
                        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-AMS-MML_HTMLorMML">                     
                        </script></head>
                        <body>
                        <p><mathjax style="font-size:2em">$$ y = x $$</mathjax></p>
                        </body></html>
                        """
        if x > 0 and y == 0 and z == 1:
            pagesource = """
                         <html><head>
                         <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-AMS-MML_HTMLorMML">                     
                         </script></head>
                         <body>
                         <p><mathjax style="font-size:2em">$$ y = x + {x} $$</mathjax></p>
                         </body></html>
                         """
    elif graph == "cubic":
        if x == 0 and y == 0 and z == 1:
            pagesource = """
                        <html><head>
                        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-AMS-MML_HTMLorMML">                     
                        </script></head>
                        <body>
                        <p><mathjax style="font-size:2em">$$y = x^2$$</mathjax></p>
                        </body></html>
                        """
        if x > 0 and y == 0 and z == 1:
            pagesource = f"""
                         <html><head>
                         <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-AMS-MML_HTMLorMML">                     
                         </script></head>
                         <body>
                         <p><mathjax style="font-size:2em">$$ y = (x-{xt})^2 $$</mathjax></p>
                         </body></html>
                         """
        if x == 0 and y > 0 and z == 1:
            pagesource = f"""
                         <html><head>
                         <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-AMS-MML_HTMLorMML">                     
                         </script></head>
                         <body>
                         <p><mathjax style="font-size:2em">$$ y = x^2 + {yt} $$</mathjax></p>
                         </body></html>
                         """
        if x > 0 and y > 0 and z == 1:
            pagesource = f"""
                         <html><head>
                         <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-AMS-MML_HTMLorMML">                     
                         </script></head>
                         <body>
                         <p><mathjax style="font-size:2em">$$ y = (x-{xt})^2 + {yt} $$</mathjax></p>
                         </body></html>
                         """
        if x > 0 and y < 0 and z == 1:
            pagesource = f"""
                         <html><head>
                         <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-AMS-MML_HTMLorMML">                     
                         </script></head>
                         <body>
                         <p><mathjax style="font-size:2em">$$ y = (x-{xt})^2 - {yt} $$</mathjax></p>
                         </body></html>
                         """
        if x < 0 and y > 0 and z == 1:
            pagesource = f"""
                         <html><head>
                         <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-AMS-MML_HTMLorMML">                     
                         </script></head>
                         <body>
                         <p><mathjax style="font-size:2em">$$ y = (x + {xt})^2 + {yt} $$</mathjax></p>
                         </body></html>
                         """
        if x < 0 and y < 0 and z == 1:
            pagesource = f"""
                         <html><head>
                         <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-AMS-MML_HTMLorMML">                     
                         </script></head>
                         <body>
                         <p><mathjax style="font-size:2em">$$ y = (x + {xt})^2 - {yt} $$</mathjax></p>
                         </body></html>
                         """

    elif graph == "quadro":
        if x == 0 and y == 0 and z == 1:
            pagesource = """
                        <html><head>
                        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-AMS-MML_HTMLorMML">                     
                        </script></head>
                        <body>
                        <p><mathjax style="font-size:2em">$$ y = x^3 $$</mathjax></p>
                        </body></html>
                        """
    return pagesource