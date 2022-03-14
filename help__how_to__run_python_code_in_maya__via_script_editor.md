Running Python Code In Maya's Built In Script Editor
==================================

Do the following to run code in the Maya script editor, and safeguard against Maya deleting the code from the editor.

<pre>

Press:
Ctrl A			(select all)
Ctrl C			(copy text to clipboard)
Ctrl Enter		(actually run the code)

</pre>

In the event that Maya deletes your code, you'll be able to press Ctrl V to paste it back again!


Example
================
In the script editor, in a new "Python" tab, type:

<pre>
import maya.cmds as cmds
cmds.polyCube()
</pre>


Then press     Ctrl A  Ctrl C  Ctrl Enter
<br>

Your code should run and a new polyCube should be created!

