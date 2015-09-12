# Devlopment Environment Setup
Components:
----------------
- python (3.4.0)
- virtualenv (13.1.2)
- virtualenvwrapper (4.7.0)
- pygame (1.9.2a0)
- PyCharm Community Edition (4.5.4)

Code completion for pygame:
---------------------------
In order for code completion to work for pygame, in IDEs such as pycharm, a few changes need to be done in pygame's \__init__.py file. The way pygame's submodules are imported confuses the IDEs. So you need to change the imports from:

<pre>
try:
    import pygame.display
except (ImportError, IOError):
    display = MissingModule("display", geterror(), 1)
</pre>

to:
<pre>
from pygame import display
</pre>

The modified __init__.py for pygame (1.9.2a0) is present in this directory as pygame1.9.2a0__init__.py