WHAT ALL TO DO 
On pulling the repo, all these changes should already be there. (JUST MAKE SURE TO DOWNLOAD DOLOS (as given below))








>>>> Install dolos globally. I use wsl, so I installed, like outside any directory.

Install from here -> https://dolos.ugent.be/docs/installation.html

next up, I have all the website files in this folder named 'site'. Refer to
the repositories I sent you. Make changes to following files in your system.


I have a submissions directory globally made by the name of "submissions". This is where the submissions 
are stored.


 
 Further steps : 
 
 after changing the given files and changing respective addresses, start your virtual 
 environment. Go to /site directory where manage.py file is kept.
 
 /* CHECK manage.py AS A PRECAUTIONARY MEASURE FOR ANY CHANGES (like from my repo) */

 then, run :
python manage.py makemigrations (after doing changes to models)
python manage.py migrate (this too) 
then
python manage.py runserver 0.0.0.0:8000
 
 (this is given that you have python3 installed in the venv)
 
 


