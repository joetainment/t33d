Teaching 3D Python Exercises
===============================


Exercise 01
General Questions

1)  Are scripting languages considered high or low level languages?  (Another way of asking this would be, is Python considered a high or low level language.)
<br><br><br>


2)  Which language sees more widespread use, MEL or Python?
<br><br><br>


3)  Name at least one other popular programming language other than MEL or Python.
<br><br><br>


4)  Write a comment as it would appear in MEL code.
<br><br><br>

5)  Write a comment as it would appear in Python code
<br><br><br>

<br>
...onto the Maya specific questions...
<br><br>

6)  Write mel code to make a sphere with a radius of 6 units in Maya.
<br><br><br>


7)  It is common, when working with Python in Maya, to import Maya's commands as a python module.  This is generally done at the beginning of every script.  Write code to import the standard commands in the standard fashion shown in the Maya official documentation.
<br><br><br>

8)  Write Python code to create a sphere in Maya that has a radius of 4 units.
<br><br><br>

9)  Translate this example MEL code into Python code:
	polyCube -sx 4 -sy 8 -sz 2;
<br><br><br>

10)  Translate this example Python code into MEL code:

	cmds.ls( selection=True )
<br><br><br>



Exercise 02

For each expression below, give the value it evaluates to (expressed in the simplest form), and give the type of the value.  If it evaluates to no other particular value or type, the value is None and the type is NoneType.  If the value is a string or unicode string, make sure you write the value in quotes.

Assume that maya

examples:	question	y = len("55555")
		value		5
		type		int

		question	cmds.select( clear=True )
		value		None
		type		NoneType		

question	x = cmds.polySphere
		value		cmds.polySphere
		type		function
('builtin_function_or_method' would be fine instead of function, but function is close enough)

Questions:
				Value				Type

example           "Happy Birthday!"                                             "Happy Birthday!"                             str

example          "Happy" + " " + "Birthday" + "!"                          "Happy Birthday!"                            str

example            4                                                                             4                                            int   

example            1 + 2                                                                       3                                            int   

example            1.0 + 3.1                                                                 4.1                                          float    

example             round                                                                     round                               function

example             round(4)					4.0				float

example              int(4.0)                                                                 4				int


    len("dog")						


    "dog"			
									
   len				


    47 + 0.328						


    0.25 + 0.25 + 0.25 + 0.25				


    dog_sound = "bark! bark!"				


   ( 6, 4+1 )							

    ( 7, 3 )						

    [ 7, 3 ]						


    [ 7, 3 ][1]						

cont. next page...



Questions (... continued)						Value				Type


    len( [ 7, 3 ] )						

    ( 8, )							


    8,							


    -8							


    (-8,)[0]					 	

    { 'website': 'Teaching3D', 'url':'http://teaching3d.com' }	

    { 'website': 'Teaching3D', 'url':'http://teaching3d.com' }['url']	

    9/2							

    9/2.0						







Exercise 03

Write Python code to create a variable called width and assign it a value of 8.009




What would be the type and value of the variable created by your answer to the last question? (provide 2 answers, the type, and the value)




Write Python code to create a variable called name, and make it equal to "Carl".




What would be the type of addNumbers in the following code:
(The type of addNumbers itself, not the return value it would give.)

def addNumbers( a, b ):
	return float( a + b )




Assume the code in the last question had already been run, what would the type and value resulting from the following code:
addNumbers( 8.45, 1.33 )




After the following code executes, what will the type of x be"
x = [ "pens", "pencils", "papers", "erasers", "staples" ]




What would be the length of the resulting variable x, in the above code example?




If the following code was executed, what would the resulting value of n be:
n=5
if n >=4:
    n = 11
else:
    n = 2





What would be printed when running the following code example?
i = 0
for number in [0,5,2]:
    i = i + 1
print( i )


What would be printed when running the following code example?
i = 0
for number in [5,1,2]:
    i = i + number
print( i )


# Bonus question:   what would be printed if the last line said the following?"
print( number)



What would be the printed result of the following program?

def changeNumber(  numGiven  ):
    r = 3.000 * numGiven
    return r + 2.0

print(  changeNumber( 2 )  ) 



In the above code example, what is the type of changeNumber itself?




What is the purpose of the keyword def, as in, what does it do?



What type would be returned by changeNumber?







Exercise 4

Write Python code to create a variable called width and assign it a value of 6




Write a line of code that creates a variable called position that is a tuple containing 3 coordinates, so that it could act like a Vector3 storing x, y, and z coordinates. each of which is a floating point number.  Make it have a value of 3.4 in x, 8.0 in y, and -1.54 in z.



Write a line of code that creates a variable called scale, that is a list which uses floats for storing x, y, and z values to represent scale.  Make it represent a scaling of 1.21, -2.42, 3.63.
(The is just like the answer to the last question, but now called scale, and using a list instead of a tuple.)



Write a line of code that creates a dictionary called books, with keys that are titles of books and values that are the author. Add one title called “Calvin and Hobbes” by author “Bill Waterson”, and another title called “Life In Hell”, by “Matt Groening”




What is the primary difference between a tuple and a list? (not just the syntax)




Are items in a python dictionary in any particular order?
(hint, see:   https://docs.python.org/2/tutorial/datastructures.html#dictionaries)


---------------------------------------------
For the next questions, assume the following code:

import pymel.all as pm
import maya.cmds as cmds
objs = cmds.ls( )
for i, obj in enumerate(objs):
    timesPassed = i
    theObject = obj
---------------------------------------------



What is the type of objs?





What type is the type of obj inside the for loop?





What is the type of i inside the loop?





What is the value of i during the second time that the contents of the for loop run (the second iteration)?




Given the list:  [ apples, pears, bananas ]  Write a line of code  to insert an item “grapes” between pears and bananas.  (You may have to research to find this answer.  As a hint, look for python documentation about inserting into a list.)





Write a line of code to combine the lists fruits and vegetables into a list called food. (Again, you may need to research this.)




Write a line of code to create a dictionary called stats, which remembers that wins is 4 and losses is 2.




Given a dictionary stats in which the keys were the names of sports teams, as strings, and the values were the number of wins the team had in the season, write a short python program which would print the name of each team along with how many wins the team had. (do not simply print the dictionary itself, print individual items from it)







Exercise 5 - Problem Solving

Read the directions and follow the instructions.  Generally, for this assignment you are just finding solution to problems in the shown code, and/or adding some additional code to accomplish the requested tasks.

There are a lot of *intentional* typos.  Part of this exercise is to find and fix those typos.

When finished, each question's code should run as a Maya python script, and produce the requested result.


Note, please scroll down,  I had to fit them on pages nicely, so it doesn't start until the next page!



##############  Question 1 Code  ############################
Import  maya.commands as cmds 	## Has 2 typo's .   Fix them
originalSelection = cmds.ls( ) 	## Doesn't properly get the selection.  Fix it
print( originalSelection )          	## This should print the selection
                           	## It will work once you fix the lines above
##############  End of Question One Code  ############################
##Write the fixed program below as your answer.




##############  Question 2 Code  ############################
#### This program should make a cube 8 units wide 4 units tall and 2 units deep, and with no face on top

Import maya.cmds as cmds
#### Make a new cube!
####     This is missing something right before the "polyCube"
####     in polyCube   it's also missing the options
newCubeAsList = polyCube()   
#### Get the cube's transform code
####     Remember, we got a list containing the cube's name,
####     not the cube's name itself, so we need to get
####     the cube's name.)
newCubeXform = newCubeList[999999]   ## Wrong number for index.  Fix this!

#### This deletes a face on the cube, but it's the wrong one.
####    Fix it so the right face is deleted
cmds.delete( newCubeXform+".f[4]" )

##############  End of Question 2 Code  ############################
##Write the fixed program below as your answer.



##############  Question 3 Code  ############################
###
####  This next function should work to unparent any maya object
####	when the function is given the objects name as a string
###
####	in the docs and figure out what the right answer is.
####	"something" is not correct.  Look in the official
####	docs for a solution.
####	Hint: even one letter substituted for "something" is enough!
####    Note that you'll have to create an scene with some parented
####    objects if you want to test this.

import maya.cmds as cmds

def unparent(obj):
    cmds.parent( obj, something=True )

for obj in cmds.ls():
    try:
        unparent(obj)
    except:
        print( "Could not unparent object "+obj)

## At this point, all objects in the scene should be unparented

##############  End of Question 3 Code  ############################
##Write the fixed program below as your answer.



##############  Question 4 Code  ############################
####     Fix the call to the function, without changing the function itself

def doSomething( actuallyDoIt=False ):
    if actuallyDoIt==True:
        print( "This actually did something!" )

## The next line isn't working!  Fix the call to the function so
## it passes the correct argument and calls the function in
## a way that makes it print
doSomething( )  	

##############  End of Question 4 Code  ############################
## Write the fixed line below as your answer
## (no need to write the whole program)




##############  Question 5  Code ############################
####       Make a 5x5x5 cube of cubes!
Import pymel.all as pm
## Here's a little bit to get you started
for x in xrange(5): ## Look at this code and what it does
    for y in xrange(5):  ## You can figure it out....
        ## you'll have to add another loop, using another axis variable
        print( "This is a hint! x is now " + x + " and y is now " + y )
        pcube = pm.polyCube()
        pm.move( pcube, to,where,itGoes )

##############  End of Question 5  Code ############################












Exercise 6  - Custom Script

Write your own short python program, that is useful to you working on your projects. It could be a Maya Python script, but doesn't have to be. Also write a couple paragraphs of english explaining how it works.

Ideally you should write something that automates or accelerates some part of the workflow.  If you make a tool based on something we did in class, you should add some kind of significant improvement to it.

This part of the assignment is pretty flexible and I don't expect all that much.  Even just a few lines of code that does something useful for you, would be good enough.  Please feel free to ask me for help, and to review your ideas or suggest some.

