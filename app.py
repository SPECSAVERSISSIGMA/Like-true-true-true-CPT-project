from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import random

app = Flask(__name__)
app.secret_key = 'yAFGEJN47q8XCio97t775568ua78neia381uahwo2eiuOUGW7IAGEIUAGehut1234h83198235y01273t5198123yoiiUIOWGAEukehot7192835t198273yuHasegwufg2787383718234aksjlkhdifaSUIOGEEAasegasdSDFASEeasgasedgaeSUAIG891827348yhdskfasiofeasguoaiuaskjohueaUIOGEIGSEioHGIUEGHOh1iu2h31uihoHSEUILGO3ILUOIL3UKWHOIL1UGOI23UKWREALKSJHLKUHelskuhlkuhlkuHLKUEHukgwlIUKRHLI3U12IU3KJ4HL1K2J3H412K3H4L1K23JLKlkllk2j1h34kj12h3123412341234kjlhkhoiskIOAHEGIUAhiuosaeuhfoas123412341gheaskeghlakushdfiuasgelkuashegiuadshfouiaseo61782365871236498i7103298t6y9iwoeughfoiaukjsdbgajlkeghlkueshl'  # Use a strong secret key

# Create DB and user table if not exists
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

@app.route('/')
def home():
    return redirect(url_for('login'))

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        #query database, asking cursor to do smth in database, *=all 
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        #fetchone gets all details. 
        user = cursor.fetchone()
        #ggs closed 
        conn.close()

        if user:
            session['username'] = username
            return redirect(url_for('welcome'))
        else:
            flash("Invalid credentials!", "error")

    return render_template('login.html')

@app.route('/welcome')
def welcome():
    if 'username' in session:
        return render_template('welcome.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Logged out successfully!", "info")
    return redirect(url_for('login'))

@app.route('/isekai')
def isekai():
    if 'username' in session:
        return render_template('isekai.html', username=session['username'])
    return render_template('isekai.html')

@app.route('/Anime')
def Anime():
    if 'username' in session:
        return render_template('Anime.html', username=session['username'])
    return render_template('Anime.html')

@app.route('/shonen')
def shonen():
    if 'username' in session:
        return render_template('shonen.html', username=session['username'])
    return render_template('shonen.html')

@app.route('/seinen')
def seinen():
    if 'username' in session:
        return render_template('seinen.html', username=session['username'])
    return render_template('seinen.html')

@app.route('/profile')
def profile():
    if 'username' in session:
        return render_template('profile.html', username=session['username'])
    return render_template('profile.html')


#complete the username and password changing stuff tonight with good css.
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




if __name__ == '__main__':
    init_db()
    app.run(debug=True)
