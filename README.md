T33D
================================

Tools and knowledge for 3D/2D Computer Graphics, Game Dev, Animation, and VFX.


About
==========

The T33D repository is a library of knowledge and code, primarily aimed at digital artists, game developers, animators, and VFX artists. (We often abbreviate this grouping by writing 3D/2DArt/GameDev, which is a quick way of covering it all.)

Mostly the T33D repo consists of notes and code. (In many cases, notes about code, or code containing notes.) There are also a lot of notes simply about art, and other topics related to art and technology.

Other forms on information, images, videos, etc, are also included or linked to by the notes. (The repository itself is not meant to include large digital files, only references to them, since they are hosted separately from the main version control repository.) Notes are not necessarily in text either. They be be in many forms T33D is originally aimed at artists, but should also be useful for industry professionals.


Founding
-------------

T33D was founded by Joe Crawford, and in the early stages of development, T33D was primarily authored by Joe. It is closely related to Teaching3D, Joe's organization focused on teaching. The name itself actually translated to "Teaching 3 3D" where the separated 3 in the name is a recursive abbreviation which has multiple meanings.


Name
--------------

The project's name "t33d" is normally pronounced teed and usually more affectionately pronounced as "tweed". The double three digits in the title are often interpreted like the word "1337", as hacker "leet-speak", as in "elite". (Using 3's instead of E's is common in leet-speak.)

More Will Be Explained About The Meaning of the letters in the name, T33D, later.



---



### Capitalization of the name T33D

"T33D" is usually used in text and branding, but "t33d" is usually used in code, for example the Python Package name. Other variations like T33d may by used in situations where certain conventions often exist for capitalization exists (for example, class names in Python code).




The License
--------------------------

Any code not explicitly noted otherwise will be licensed under LGPL version 3, or if it's being quoted from elsewhere, licensed under it's original license. Please contact us if you have any license questions. We aim to be pretty liberal about this and are not looking to be strict about licensing, especially for anything we'd consider free use, which we'd paint with a broad brush.

Any art will be similarly licensed as either Public Domain, CC0 ( "creative commons zero license" ), or as some other creative commons or similar license in the creative commons spirit.





Where to Start?
===================

If you are unsure as to where you should start, we would suggest either of the following options


- Browse The Notes   ...or...
- Browse The Tools

In many cases, users looking for apps/scripts/plugins/tools can simple download the entire t33d repo, unzip it, and find the tools inside where they want them. Users wanting to copy our notes into their own can do the same, copy our notes folder into some subfolder of their own.

In some cases we uses the *releases* page to release specific important landmark versions of the tools, so in the future, expect content to via available under this repo's associated releases page as well.





The Code
=========

The code is intended to include useful tools, but also, to function as examples and learning material, helpful for anyone learning to code, especially people learnin to code for 3D, animation, vfx, or game development.



Programming Languages Used In Our Code
---------------------------------------
Most of our code and tools are coded in Python, but in the long run, our codebase will likely include many different languages. For example, a log of game logic code for game engines like Godot and Unity are written in C#, so C# is expected to be in our codebase longterm. Some are command line tools only, but some have graphical user interfaces as well, or in some cases TUI, terminal user interfaces, which are sort of like GUI's but work in text mode, and draw the interface as text characters.



Tools Included in our Codebase
-------------------------------

As of Feb 28 2006, the primary tools included in the T33D code base are Maya scripts, and other scripts related to programming with Python, one of the two main scripting languages used by Maya.



### General Use Tools and System Utilities

T33D includes certain tools that are more generally useful, such as tools for backing up work, organizing, and even for using artificial intelligence.



### Maya Scripts

As of Feb 28 2006, several Maya scripts exist, but it's only the standalone scripts that are worth using at this point.  The main T33D package isn't far along enough to be useful yet.


#### Recreation of Features from MmmmTools

Many years ago, Joe Crawford, the founder of T33D, had a very popular Maya script package called MmmmTools. It had a high 4.x rating, very close to a perfect 5 out of 5 stars, and it had tens of thousands of downloads. MmmmTools was used by manny thousands of artists all around the world, and in many studios. Unfortunately, when Maya transitions to Python 3 (from Python 2), MmmmTools it was too much work to port MmmmTools to the new version at that time. So, MmmmTools became unusable. (MmmmTools also had a number of tech debt issues anyway, because it was started when Joe was quite new to Python scripting Maya. Thus, it was decided to deprecate the project, and aim new development towards T33D, where hopefully we can recreate tools that we had in MmmmTools before.)

In the long run, we are planning to have most of the still useful features from MmmmTools added into T33D, and working on modern versions of Maya. Thankfully, many of MmmmTools' older features are no longer necessary in T33D, because Maya has improved since, and has introduced features which accomplish the same things, making some of the old MmmmTools features redundant.





Contact
=======

Joe Crawford is currently the main contact for this project, though the GitHub communication systems can also be used while our project remains on GitHub.
