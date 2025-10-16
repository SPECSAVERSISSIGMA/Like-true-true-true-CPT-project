My project is an anime review website. Im going to be developing a anime review website that will be be a interactive dynamic website for all users. It will be called OtakuZone and it will be a website for all, including for if your not english.Very inclusive.
 

figma designing
asthetically pleasing
colour

functional: 
should be able to give interactive buttons where u can press and it can bring u somewhere, eg, chat button or reply button or popular anime leaderboard and also linking the anime to website. 
login with stuff, eg two step verification
should be let u login and save progress with what u have watched
should give u free options and a help me guide.
homepage and regular page
language changer
Non-functional:
It should be able to run smoothly.
It should be able to perfectly interact with different people
The system must be user-friendly and easy to navigate
The system must be secure against unauthorized access
Performance testing, security testing, usability testing, and constant updates. 


I started working by Adding in the css and html outline. I had CHATGPT to help me with ideas with CSS like for example background ideas and styling. This was a long task to create the outline of what I was going to create. The html started with welcome, login and signup page. To link it up, I imported from  Flask, render_template, request, redirect, url_for, session, flash, sqlite3, random. These would be essential for the sqlite Database and etc. 

I started creating Database early on. I created a custom key that people cant access for a secure database. Then i started making my Database as seen below:

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    #what will it execute, id username and password
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

First i defined a database to make one. I connected it with 'users.db' which is what my database will be called. I used cursor and conn.cursor to all for commands to be executed in the project. These are to be linked to the database and yea. After that I got the cursor to execute what i wanted which was ID, Username and password. Then commit and closed for the database. 

I then created the database to take data from the app to the database by using the get and post method:
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            flash("Account created successfully! Please login.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username already exists!", "error")
        finally:
            conn.close()

    return render_template('signup.html')

My signup page used sqlite functions and get and post methods. By defining signup, i then had the different methods defined. Post meant interaction from the webapp to the database. This code meant that what ever added in for example username added on the website is then posted onto the database. I also used a if function to create a trial and error flow into my database. This for example was for unique username etc. 

After I linked that to login and signup with the use of jinja 2. That allowed for my database to work with login and signup. After adding in Styling into my login and signup. 

I then worked on adding in other pages and linking it with python. The code for them was almost the same:
@app.route('/shonen')
def shonen():
    if 'username' in session:
        return render_template('shonen.html', username=session['username'])
    return render_template('shonen.html')

Without doing this pages will not be able to load in. This also allows for render template. I did some css for the rest like shonen seinen isekai and welcome.

After that i added in a username changing functionality. I started by loading in profile and then I started creating my update profile:

@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    if 'username' not in session:
        return redirect(url_for('login'))

    current_username = session['username']

    if request.method == 'POST':
        new_username = request.form['new_username']
        new_password = request.form['new_password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND username != ?", (new_username, current_username))
        user_check = cursor.fetchone()
        if user_check:
            flash("Username already taken.", "error")
            conn.close()
            return redirect(url_for('updateprofile'))
        cursor.execute("UPDATE users SET username=?, password=? WHERE username=?",
                       (new_username, new_password, current_username))
        conn.commit()
        conn.close()
        session['username'] = new_username
        flash("Profile updated!", "success")
        return redirect(url_for('profile'))

    return render_template('updateprofile.html', username=current_username)

what this did was that it made sure that the username was in session first. After used the post method similar to the login and signup to allow for the post method. This made new usernames and passwords. After that it would redirect to profile.html. 

I also added in a random functionality. This was to get the random anime to be generate when the user wants. I had help from AI as i was having trouble. My original idea used an f string in python :

quotes=["an apple a day keeps the doctors away", "honesty is the best policy", "don't beat around the bush"]

@app.route("/random")
def quote():
    return f"the quote of the day is {random.choice(quotes)}"

This used a array and a f string to randomly generate a quote from the list. By adding in a list of anime instead and linking it to random.html i could pick a random anime when the user clicked on the button:

anime = [ "Naruto", "Attack on Titan",  "Fullmetal Alchemist", "Blade of the Immortal", "Cowboy Bebop", "Steins;Gate", "Rurouni Kenshin: Trust & Betrayal", "Berserk", "Mushishi", "Now and Then, Here and There", "Hunter × Hunter", "Rurouni Kenshin" "Monster", "Naruto", "Naruto: Shippuden", "Bleach", "One Piece", "Dragon Ball Z", "Dragon Ball", "Dragon Ball Super",
    "Attack on Titan", "Demon Slayer", "My Hero Academia", "Jujutsu Kaisen", "Fullmetal Alchemist",
    "Fullmetal Alchemist: Brotherhood", "Death Note", "Steins;Gate", "Cowboy Bebop", "Samurai Champloo",
    "Inuyasha", "Spy x Family", "Mushishi", "Fruits Basket", "Parasyte", "Tokyo Ghoul", "Sailor Moon",
    "Black Clover", "Puella Magi Madoka Magica", "Soul Eater", "Mob Psycho 100", "Hunter x Hunter",
    "Yu Yu Hakusho", "JoJo's Bizarre Adventure", "Gintama", "Code Geass", "D.Gray-man",
    "The Seven Deadly Sins", "Fairy Tail", "Blue Exorcist", "Violet Evergarden", "Anohana",
    "Your Lie in April", "Toradora!", "Neon Genesis Evangelion", "Devilman Crybaby",
    "The Promised Neverland", "Made in Abyss", "Noragami", "Clannad", "Clannad: After Story",
    "Angel Beats!", "Re:Zero", "No Game No Life", "KonoSuba", "Tengen Toppa Gurren Lagann", "Monster",
    "Great Teacher Onizuka", "Golden Kamuy", "Mobile Suit Gundam", "Detective Conan", "Case Closed",
    "Nana", "Erased", "Black Lagoon", "Akame Ga Kill!", "Sword Art Online", "Log Horizon",
    "Is It Wrong to Try to Pick Up Girls in a Dungeon?", "That Time I Got Reincarnated as a Slime",
    "Hellsing", "Hellsing Ultimate", "Trigun", "Ranma ½", "Kimi no Na wa", "Spirited Away",
    "Princess Mononoke", "Howl's Moving Castle", "Akira", "Wolf's Rain", "Serial Experiments Lain",
    "Planetes", "Natsume's Book of Friends", "Yuru Camp", "Nichijou", "The Melancholy of Haruhi Suzumiya",
    "Lucky Star", "K-On!", "Angel Sanctuary", "Bakuman", "March Comes in Like a Lion", "Barakamon",
    "Kaguya-sama: Love is War", "Rent-A-Girlfriend", "Horimiya", "The Quintessential Quintuplets",
    "Haikyuu!!", "Yuri on Ice", "Free!", "Chihayafuru", "Ace of Diamond", "Slam Dunk", "frieren", "Fragrant Flower Blooms With Dignity", "Rising Of The Sword Hero", "Air", "Arakawa Under the Bridge", "Ascendance of a Bookworm", "Assassination Classroom", "Astro Boy", "Azumanga Daioh", "Baccano!", "Bakemonogatari", "Banana Fish", "Beastars", "Beelzebub", "Beyond the Boundary", "Black Bullet", "Black Fox", "Black Rock Shooter", "Blame!", "Bleach: Thousand-Year Blood War", "BNA: Brand New Animal", "Blood+", "Blood Lad", "Blue Period", "Bombshells: Hell's Island", "Bunny Drop", "Bungo Stray Dogs", "C: The Money of Soul and Possibility Control", "Cardcaptor Sakura", "Carole & Tuesday", "Castlevania", "Cautious Hero", "Cells at Work!", "Charlotte", "Children of the Whales", "Citrus", "Claymore", "Cobra The Animation", "Corpse Party", "Cromartie High School", "Dagashi Kashi", "Dance Dance Danseur", "Danganronpa: The Animation", "Darling in the Franxx", "Date A Live", "Deadman Wonderland", "Death Parade", "Demon King Daimao", "Denki-Gai", "Digimon Adventure", "Dimension W", "Do You Love Your Mom and Her Two-Hit Multi-Target Attacks?", "Dog Days", "Dr. Stone", "Dragon Ball GT", "Durarara!!", "Eden of the East", "Elfen Lied", "El Hazard", "El Cazador de la Bruja", "Engaged to the Unidentified", "Eromanga Sensei", "Eureka Seven", "Even Though I’m the Villainess, I’ll Become the Heroine!", "Excel Saga", "Fafner in the Azure", "Fate/Apocrypha", "Fate/Extra Last Encore", "Fate/Grand Order: Absolute Demonic Front - Babylonia", "Fate/kaleid liner Prisma☆Illya", "Fate/stay night", "Fate/Zero", "Flip Flappers", "Flying Witch", "Food Wars! Shokugeki no Soma", "Freezing", "Fruits Basket (2019)", "Future Diary", "Gabriel DropOut", "Gate", "Gamers!", "Gatchaman Crowds", "Gleipnir", "Girl's Last Tour", "Given", "Goblin Slayer", "Golden Time", "Granblue Fantasy", "Grimgar: Ashes and Illusions", "Gunslinger Girl", "Haganai: I Don't Have Many Friends", "Haiyore! Nyaruko-san", "Hajime no Ippo", "Hamatora", "Hanebado!", "Hanasaku Iroha", "Handa-kun", "Hataraku Maou-sama! (The Devil is a Part-Timer!)", "Heaven's Memo Pad", "Hellsing: Dawn", "Hibike! Euphonium", "Highschool of the Dead", "High School DxD", "Hinamatsuri", "Hitoribocchi no Marumaru Seikatsu", "Oshi No Ko", 
]

@app.route("/random")
def randomanime():
    animeoftheday = random.choice(anime)
    username = session.get('username')
    message = f"The anime of the day is {animeoftheday}!"
    return render_template('random.html', message=message, username=username)


    The anime was a list/ array that had all the anime stored that i had chatgpt to generate. Then using something similar I created the random.html and the f strong from animeoftheday. Random.choice was a function from importing the random anime.

    In the end i had chatgpt to help me with css with login and signup and update profile. I got the background images from google and I randomly found it. 