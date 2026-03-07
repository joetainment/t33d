"""
HotstringsActions module, and easy to edit python file that allows
hotstring commands to be spefied, along with the desired MEL
commands that should be executed when the hotstring is entered.
"""







actions = {'default':"""   hotkeyEditor; print "Default Action is Hotkey Editor. """}









## n is for normals
actions['n'] = """
polySoftEdgeWin;
"""    
actions['ns'] = """
SoftPolyEdgeElements 1;
"""                    
actions['nh'] = """
SoftPolyEdgeElements 0;
"""            
actions['nr'] = """
ReversePolygonNormals;
"""        
actions['nu'] = """
polyNormalPerVertex -ufn true;
"""

