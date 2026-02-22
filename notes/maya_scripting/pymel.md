Pymel
========

Because Python in Maya is implemented in such a strange way, and doesn't feel very normal (or "pythonic") some kind volunteers put together a system called Pymel that makes it a lot easier to use many of Maya features from Python, especially some of the trickier more advanced features.


Pymel's main webpage - https://github.com/LumaPictures/pymel


Some studios and pipelines purposefully avoid using pymel, so you may have to avoid using it. However, my advice is to use pymel when it’s useful, as long as you aren’t working with someone else who says not to use it. If you aren't sure if you can use it on your project, ask your supervisor or whoever else is in charge!

Pymel only causes problems if it's used carelessly, but due to some of its perceived problems and bad publicity, some people now have an almost religious objection to using it. I continue using it because in many cases it saves me hours of time, and if I really need to write something without Pymel, I can always rewrite using maya.cmds and OpenMaya.



Understanding The Difference Between  maya.cmds  and  pymel
================================================================

Maya.cmds does most things with simple strings, where pymel does almost everything with python objects (instances of classes).  Pymel will often be much much easier and require you to write much less code, but it can potentially run slower than maya.cmds.  In some case much much slower.  There are also however some cases where pymel is actually faster due to it’s way of using Maya’s API.  My general advice is try with pymel and use maya.cmds for parts where pymel is too slow.

Pymel Compared to maya.cmds:
https://www.youtube.com/watch?v=MzyLhdY2PSc

I usually use
<pre>
import pymel.all as pm 
</pre>

for using pymel,  and I use
<pre>
import maya.cmds as cmds
</pre>

you can use both in the same script, but only if you are careful
and understand how they interact and potentially conflict

