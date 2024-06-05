import sqlite3

def create_tables():
    # Veritabanı bağlantısı oluştur
    conn = sqlite3.connect('yoga_pose_verification.db')
    cursor = conn.cursor()

    # Kullanıcılar tablosunu oluştur
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL CHECK (role IN ('student', 'instructor'))
    )
    ''')

    # Fotoğraflar tablosunu oluştur
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS photos (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        photo_path TEXT NOT NULL,
        pose TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')

    # Değişiklikleri kaydet ve bağlantıyı kapat
    conn.commit()
    conn.close()
    print("Veritabanı ve tablolar başarıyla oluşturuldu.")

if __name__ == '__main__':
    create_tables()
