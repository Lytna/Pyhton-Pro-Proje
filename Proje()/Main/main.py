# İçe aktar
# Veri tabanı kitaplığını bağlama
from flask import Flask, logging, render_template,request, redirect, session, flash, send_file, url_for
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import speech, ozet, os, uuid, remove1, password_gen
from detection import detect_objects


app = Flask(__name__)
# SQLite'ı bağlama
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary_yeni.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Veri tabanı oluşturma
db = SQLAlchemy(app)
# Tablo oluşturma


app.secret_key = "DENEME"
#Kullanıcı Giriş Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu sayfaya erişmek için giriş yapmalısınız")
            return redirect("/")
    return decorated_function



class Card(db.Model):
    # Sütun oluşturma
    # id
    id = db.Column(db.Integer, primary_key=True)
    # Başlık
    title = db.Column(db.String(100), nullable=False)
    # Tanım
    subtitle = db.Column(db.String(300), nullable=False)
    # Metin
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    # Nesnenin ve kimliğin çıktısı
    def __repr__(self):
        return f'<Card {self.id}>'
    

#Ödev #2. Kullanıcı tablosunu oluşturun
class User(db.Model):
	# Sütunlar oluşturuluyor
	#id
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	# Giriş
	email = db.Column(db.String(100), nullable=False)
	# Şifre
	password = db.Column(db.String(30), nullable=False)




# İçerik sayfasını çalıştırma 
@app.route('/', methods=['GET','POST'])
def login():
        error = ''
        if request.method == 'POST':
            form_login = request.form['email']
            form_password = request.form['password']
            
            #Ödev #4. yetkilendirmeyi uygulamak
            users_db = User.query.all()
            for user in users_db:
                if form_login == user.email and form_password == user.password:
                    session["logged_in"] = True #session başlat
                    session["email"] = user.email
                    session["id"] = user.id
                    return redirect('/main')
            else:
                error = 'Hatalı giriş veya şifre'
                return render_template('login.html', error=error)


            
        else:
            return render_template('login.html')



@app.route('/reg', methods=['GET','POST'])
def reg():
    if request.method == 'POST':
        email= request.form['email']
        password = request.form['password']
        
        #Ödev #3 Kullanıcı verilerinin veri tabanına kaydedilmesini sağlayın
        kullanıcı = User(email=email, password=password)
        db.session.add(kullanıcı)
        db.session.commit()

        
        return redirect('/')
    
    else:    
        return render_template('registration.html')

#ana menü
@app.route('/main')
@login_required
def main():
    return render_template('main.html')

#özet 
@app.route('/summary', methods=['GET', 'POST'])
@login_required
def summary():
    summary = ''
    if request.method == 'POST':
        text = request.form['text']
        sayı = request.form.get('b')
        summary = ozet.fonksiyon(text,int(sayı))
    return render_template('summary.html', summary=summary)

#arkaplan kaldırma 
@app.route('/background', methods=['GET', 'POST'])
@login_required
def background():
    if request.method == 'POST':
        img = request.files["a"]
        img_filename = str(uuid.uuid4()) + "_" + img.filename
        img_path = os.path.join('static/resimler', img_filename)

        try:
            os.makedirs(os.path.dirname(img_path), exist_ok=True)
            img.save(img_path)
            flash(f"Image saved to {img_path}")
        except Exception as e:
            flash(f"Error saving image: {e}")
            return render_template('img.html', file=None)

        try:
            output_path = os.path.join('static/resimler', 'output.png')
            remove1.fonksiyon(img_path, output_path)
            flash(f"Image processed and saved to {output_path}")
        except Exception as e:
            flash(f"Error processing image: {e}")
            return render_template('img.html', file=None)
        
        # Sadece dosya adını geçin
        return render_template('img.html', file='output.png')
    else:
        return render_template('img.html', file=None)


@app.route('/detection', methods=['GET', 'POST'])
@login_required
def detection():
    if request.method == 'POST':
        img = request.files.get("image")
        if not img:
            flash("No image file provided")
            return render_template('detection.html', result=None)

        img_filename = str(uuid.uuid4()) + "_" + img.filename
        img_path = os.path.join('static/resimler', img_filename)
        
        try:
            os.makedirs(os.path.dirname(img_path), exist_ok=True)
            img.save(img_path)
            flash(f"Image saved to {img_path}")
        except Exception as e:
            logging.error(f"Error saving image: {e}")
            flash(f"Error saving image: {e}")
            return render_template('detection.html', result=None)
        
        try:
            result = detect_objects(img_path)
            flash("Image processed successfully")
        except Exception as e:
            logging.error(f"Error processing image: {e}")
            flash(f"Error processing image: {e}")
            return render_template('detection.html', result=None)
        
        return render_template('detection.html', result=result)
    else:
        return render_template('detection.html', result=None)

@app.route('/password', methods=['GET'])
@login_required
def password():
    a = password_gen.randompassword()
    return render_template('password.html', a = a)

@app.route('/generate_password', methods=['GET'])
@login_required
def generate_password():
    a = password_gen.randompassword()
    return {'password': a}


# İçerik sayfasını çalıştırma
@app.route('/index')
@login_required
def index():
    # Veri tabanı girişlerini görüntüleme
    cards = Card.query.filter_by(user_id=session["id"]).order_by(Card.id).all()
    return render_template('index.html', cards=cards)

# Kayıt sayfasını çalıştırma
@app.route('/card/<int:id>')
@login_required
def card(id):
    card = Card.query.get(id)
    return render_template('card.html', card=card)

# Giriş oluşturma sayfasını çalıştırma
@app.route('/create')
@login_required
def create():
    print(session)
    print(session["id"])
    return render_template('create_card.html')

# Giriş formu
@app.route('/form_create', methods=['GET','POST'])
@login_required
def form_create():
    if request.method == 'POST':
        title =  request.form['title']
        subtitle =  request.form['subtitle']
        text =  request.form['text']
        user_id = session["id"]
        # Veri tabanına gönderilecek bir nesne oluşturma
        card = Card(title=title, subtitle=subtitle, text=text, user_id=user_id)
        
        db.session.add(card)
        db.session.commit()
        return redirect('/index')
    else:
        return render_template('create_card.html')

#Çıkış
@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("Başarıyla çıkış yaptınız")
    return redirect("/")

#inirme
@app.route('/download/<filename>')
@login_required
def download_file(filename):
    file_path = os.path.join('static/resimler', filename)
    try:
        return send_file(file_path, as_attachment=True)
    except FileNotFoundError:
        flash("File not found.")
        return redirect(url_for('background'))



#Kart silme 
@app.route("/card_delete/<int:id>")
def card_delete(id):
    card = Card.query.filter_by(id=id).first()
    db.session.delete(card)
    db.session.commit()
    flash("Kart başarıyla silindi")
    return redirect("/index")

#ses
@app.route("/ses")
def ses():
    a = speech.speech_tr()
    return render_template("create_card.html",a = a)

if __name__ == "__main__":
    with app.app_context():
         db.create_all()
    app.run(debug=True)