def mathtext_update(graph, x, y, z):
    global pagesource
    if graph == "line" and x == 0 and y == 0 and z == 1:
        pagesource = """
                    <html><head>
                    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-AMS-MML_HTMLorMML">                     
                    </script></head>
                    <body>
                    <p><mathjax style="font-size:2em">$$ y = x $$</mathjax></p>
                    </body></html>
                    """
    elif graph == "cubic" and x == 0 and y == 0 and z == 1:
        pagesource = """
                    <html><head>
                    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-AMS-MML_HTMLorMML">                     
                    </script></head>
                    <body>
                    <p><mathjax style="font-size:2em">$$ y = x^2 $$</mathjax></p>
                    </body></html>
                    """
    elif graph == "quadro" and x == 0 and y == 0 and z == 1:
        pagesource = """
                    <html><head>
                    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-AMS-MML_HTMLorMML">                     
                    </script></head>
                    <body>
                    <p><mathjax style="font-size:2em">$$ y = x^3 $$</mathjax></p>
                    </body></html>
                    """
    return pagesource