The-Wired is an online world where you get assigned a small community, a district, neighbors, a mayor, and actually get to know them. Built for people who find the internet too big and too loud.

hey guys and girls, I am in nano right now so please forgive any spelling mistakes you see lol

now, the wired, a few questions you may be asking

1. what is the wired?
   Ans; The wired is my first git project, born to help people be assigned a community online, to boil the project down.. I am building an online space, much like the systems of the real world, where you have small communities and houses with big cities across the horizon.

2. why?
   Ans; this is mainly for fun, but does hold some real world value, for example people who find it hard to make friends or to socialize online with random people, this project, the wired, is here to help by bringing small communities together, essentially think of it like your house in real life but online with different neighbors and mayors, it's a way to bring new people together and build friendships.

3. what do you mean by house? do you plan on recreating the entire world as a game?
   Ans; no no no... no.. not at all, I plan to make this like a top down game on the web, where you can move around communities via real time, travel to cities, and write local files to your district within a library, like your own mini history, and while it is a game I would still consider a large part of it as a messaging service. the way the world is going to work is a tree, where the core hub acts as the big connector and then sub cities, eventually down to districts, now upon making an account and verifying your email you will be randomly assigned a house in a random district, from here you will be met with others in your local community, where the small district will have a message board, (just for that district) and a library where you can write anything and save it in that district, then if you want to explore or meet someone you need to move down the tree, (which takes real time, idk how much yet lol~) before visiting their district, in addition I plan to do much more like mayors, politics, real message delays depending on your location, so much more, but that is the core of the wired.

4. that was a long answer.. okay last question, why the wired for a name?
   Ans; aha, that is a great question, it's called the wired for three reasons, 1 the entire layout is built like a wired system, information up, information down. 2 we tend to not realize it but we are really all connected, and I feel this project will help wire everyone into that fact. 3 because Serial Experiments Lain taught me something that I will never let go of...

if you have any questions feel free to ask! Yippee!

discord link; 
https://discord.gg/fZykRfdf99



INSTALLATION (<- that was 100% spelt wrong)

v0.3 
1. be a very cool linux,
2. clone the repo, 
2. run;   git clone https://github.com/rafdog1222/the-wired.git 
3. cd in there
3. run;    cd the-wired
4. make a venv, since we are linux, we carry the kernal, we will fight for the freedom, and honner his name
4. run;    python -m venv venv
5. install stuff with pip, 
5. run;    pip install -r requirements.txt
6. datbase set up time, this will take a second... 
6. run;    sudo -u postgres psql
7. if 6 dinn't work install postgresql on your system, if it did work you should be in 
7. run;    CREATE DATABASE thewired; 
8. we need to make some more stuff in here, so the user is next, you need to make the user and password here
8. run;    CREATE USER youruser  WITH PASSWORD 'yourpassword';
9. we are almost done in here, we just need perms, 
9. run;    GRANT ALL PRIVILEGES ON DATABASE thewired TO youruser;
10. we are done in here, i shall let you free, 
10. run;    \q 
11. you should be in your normal terminal now, so let's make the .env stuff ick 
11. run;    cp .env.example .env 
12. edit the .env file, this can be with nano or nvim or even vim i am going to assume nano
12. run;    nano .env
13. add in whatever you want in the .env, if you chage the wiredpass you may need to go back to the datbase and chage the password there, 
14. now we run everything! Yippee! 
14. run     app.py 
15. you will be given a link in the terminal, click it, or if you want to do it the other way the 
open your browser and go to  http://localhost:5000 <- if you chaged the port you need to chage it here.......


v0.2 
1. be cool linux guy, 
2. run ' git clone https://github.com/rafdog1222/the-wired.git ' 
2. cd in there 
3. make a venv, with ' python -m venv venv ' 
4. activate the venv!! ' source venv/bin/activate '
5. installing time~ 
5. run ' pip install -r requirements.txt '
6. run ' python app.py ' 
7. your done, either click the link in the terminal from app.py or head over to ' http://localhost:5000 ' and you're in the wired.
8. join the discord for more updates, (please it's only me and my thoughts there..)


v0.1 
1. pull me repo, (make sure it's v0.1 there may be more at the time of writing this)
2. if cool linux person make a venv, if not linux person do the first half of step 2
3. make a sqlite database, and point database.py to the .db to whatever you named it, (it's default is "wired" since that's what i use,)
4. run app.py via python, so python app.py
5. this will open up port 5000 on your localhost, it will also feed you a link to the page anyway, but if for some very weird and weird reason you don't get that link then http://<your_ip>:5000 
6. rejoice,
7. cry because i haven't made nat so you can't forward it to anyone else, or host it, but that is for v0.2 lol
8. join my discord and beg me to make v0.2 sooner, because you love the wired so very much 
9. ignore 8. if your cool, and just join anyway, it's just me at the time of writting this... 



v0.0 

1. pull my repo, (make sure it's v0.0 there might be more at the time of writing and reading this) 
2. cry, 
3. if cool linux, then make a venv
4. then make a sqlite3 database, and set the path in database.py (mine is set to wired.db, so that's the default when i commit)
5. make sure sqlite3 has all the right things, if so; 
6. run database.py (this set's up the .db)
7. ahha, 6 then 7, haha 67................ Oh, yeah, then run base.py and your done 
8. .PS. when it asks for your email you do not need to give it, type anything, hopefully in the next commit i fix this and set up auto database.py from base.py, but just write your name or whatever..

oh, and, i am really shy, but i am making a discord so people can talk to eachother or even talk to me dircely since i am online most of the time, so just ping me, it's nothing big (to be honest there is 0 people in here right now..) but give a litle look, you might like it..

discord link; 
https://discord.gg/fZykRfdf99

