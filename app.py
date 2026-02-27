from flask import Flask, render_template, request, redirect, url_for, flash
from db import get_db_connection
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_flashcards' # Required for flash messages

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute('SELECT * FROM decks ORDER BY created_at DESC;')
    decks = cur.fetchall()
    
    # Get card count for each deck
    for deck in decks:
        cur.execute('SELECT COUNT(*) FROM cards WHERE deck_id = %s;', (deck['id'],))
        deck['card_count'] = cur.fetchone()['count']
        
    cur.close()
    conn.close()
    return render_template('index.html', decks=decks)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title or not content:
            flash('عنوان و محتوا الزامی است!')
            return redirect(url_for('create'))

        # Parse the content (word : meaning)
        lines = content.strip().split('\n')
        cards_data = []
        for line in lines:
            if ':' in line:
                parts = line.split(':', 1)
                word = parts[0].strip()
                meaning = parts[1].strip()
                if word and meaning:
                    cards_data.append((word, meaning))

        if not cards_data:
            flash('فرمت وارد شده صحیح نیست. لطفا از فرمت "کلمه : معنی" استفاده کنید.')
            return redirect(url_for('create'))

        # Save to database
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Insert deck
        cur.execute('INSERT INTO decks (title) VALUES (%s) RETURNING id;', (title,))
        deck_id = cur.fetchone()[0]

        # Insert cards
        for word, meaning in cards_data:
            cur.execute('INSERT INTO cards (deck_id, word, meaning) VALUES (%s, %s, %s);', 
                        (deck_id, word, meaning))

        conn.commit()
        cur.close()
        conn.close()
        
        return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/deck/<int:deck_id>')
def view_deck(deck_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    cur.execute('SELECT * FROM decks WHERE id = %s;', (deck_id,))
    deck = cur.fetchone()
    
    if deck is None:
        cur.close()
        conn.close()
        return 'Deck not found!', 404

    cur.execute('SELECT * FROM cards WHERE deck_id = %s;', (deck_id,))
    cards = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return render_template('deck.html', deck=deck, cards=cards)

@app.route('/deck/<int:deck_id>/delete', methods=('POST',))
def delete_deck(deck_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM decks WHERE id = %s;', (deck_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
