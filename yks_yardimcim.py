import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                             QWidget, QPushButton, QScrollArea, QFrame, QHBoxLayout, QStackedWidget)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve
from PyQt5.QtGui import QFont, QColor, QPalette, QLinearGradient, QBrush

class FizikApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # --- PENCERE AYARLARI ---
        self.setWindowTitle("YKS YARDIMCIM - Fizik")
        self.setGeometry(100, 100, 1000, 700)
        
        # --- MODERN MATEMATİKSEL ARKA PLAN (CSS ile) ---
        # Arka plana ızgara (grid) deseni ve koyu renk veriyoruz
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e2e;
            }
            QLabel {
                color: #cdd6f4;
            }
            QPushButton {
                background-color: #89b4fa;
                color: #1e1e2e;
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #b4befe;
            }
        """)

        # Ana Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # --- HEADER (BAŞLIK VE İMZA) ---
        self.header_frame = QFrame()
        self.header_layout = QVBoxLayout(self.header_frame)
        
        self.title_label = QLabel("YKS YARDIMCIM")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        self.title_label.setStyleSheet("color: #f38ba8;") # Pembe neon

        self.signature_label = QLabel("ALPEREN SÜNGÜ")
        self.signature_label.setAlignment(Qt.AlignCenter)
        self.signature_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.signature_label.setStyleSheet("color: #fab387; letter-spacing: 5px;") # Turuncu neon

        self.header_layout.addWidget(self.title_label)
        self.header_layout.addWidget(self.signature_label)
        self.main_layout.addWidget(self.header_frame)

        # --- İÇERİK ALANI (KARTLAR) ---
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        # Konu 1: Fizik Nedir?
        self.page1 = self.create_content_page(
            "1. BÖLÜM: FİZİK BİLİMİNE GİRİŞ",
            "Fizik; madde, enerji ve bunlar arasındaki etkileşimi inceleyen doğa bilimidir.\n\n"
            "🔍 Gözlem ve deneye dayanır.\n"
            "📏 Ölçülebilir büyüklüklerle ifade edilir.\n"
            "❌ Metafizik, Teoloji ve Astroloji fizik bilimi değildir!",
            "🌌" 
        )
        
        # Konu 2: Fiziğin Alt Dalları (KAMYONET)
        self.page2 = self.create_content_page(
            "2. BÖLÜM: FİZİĞİN ALT DALLARI (KAMYONET)",
            "Akılda kalıcı kodlama: K.A.M.Y.O.N.E.T\n\n"
            "🔸 K - Katıhal Fiziği: Kristal yapıları inceler (Leke tutmayan kumaş, şarjlı piller).\n"
            "🔸 A - Atom Fiziği: Atomun yapısını inceler (Nanoteknoloji).\n"
            "🔸 M - Mekanik: Hareket, kuvvet ve denge (Gezegenler, köprüler).\n"
            "🔸 Y - Yüksek Enerji ve Plazma: Atom altı parçacıklar (CERN).\n"
            "🔸 O - Optik: Işık olayları (Gözlük, teleskop).\n"
            "🔸 N - Nükleer Fizik: Çekirdek tepkimeleri (Atom bombası, MR cihazı).\n"
            "🔸 E - Elektromanyetizma: Yüklü parçacıklar (Mıknatıs, pusula).\n"
            "🔸 T - Termodinamik: Isı ve sıcaklık (Yalıtım, motorlar).",
            "🚛"
        )

        # Konu 3: Fiziksel Büyüklükler (KISA MUZ)
        self.page3 = self.create_content_page(
            "3. BÖLÜM: TEMEL BÜYÜKLÜKLER",
            "Tek başına anlam ifade eden büyüklüklerdir. Kodlama: K.I.S.A.M.U.Z\n\n"
            ⚖️ K - Kütle (kg) -> Terazi\n"
            "💡 I - Işık Şiddeti (cd) -> Fotometre\n"
            "🌡️ S - Sıcaklık (Kelvin) -> Termometre\n"
            "⚡ A - Akım Şiddeti (Amper) -> Ampermetre\n"
            "🧱 M - Madde Miktarı (mol) -> Ölçülemez, hesaplanır\n"
            "📏 U - Uzunluk (metre) -> Şerit metre\n"
            "⏱️ Z - Zaman (saniye) -> Kronometre",
            "🍌"
        )

        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)
        self.stacked_widget.addWidget(self.page3)

        # --- NAVİGASYON BUTONLARI ---
        self.nav_layout = QHBoxLayout()
        
        self.btn_prev = QPushButton("<< Önceki Konu")
        self.btn_prev.clicked.connect(self.prev_page)
        self.btn_next = QPushButton("Sonraki Konu >>")
        self.btn_next.clicked.connect(self.next_page)

        self.nav_layout.addWidget(self.btn_prev)
        self.nav_layout.addWidget(self.btn_next)
        
        self.main_layout.addLayout(self.nav_layout)

    def create_content_page(self, title, content, icon):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # İçerik Kartı (Card Design)
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #313244;
                border-radius: 20px;
                border: 2px solid #45475a;
            }
        """)
        card_layout = QVBoxLayout(card)

        # İkon/Resim Alanı (Emoji kullanıyoruz şimdilik, buraya resim yüklenebilir)
        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setFont(QFont("Segoe UI Emoji", 60))
        icon_label.setStyleSheet("border: none; background: transparent;")

        # Başlık
        lbl_title = QLabel(title)
        lbl_title.setAlignment(Qt.AlignCenter)
        lbl_title.setFont(QFont("Verdana", 18, QFont.Bold))
        lbl_title.setStyleSheet("color: #a6e3a1; border: none; margin-bottom: 10px;") # Yeşil

        # Metin İçeriği
        lbl_content = QLabel(content)
        lbl_content.setAlignment(Qt.AlignLeft)
        lbl_content.setFont(QFont("Calibri", 14))
        lbl_content.setWordWrap(True)
        lbl_content.setStyleSheet("color: #cdd6f4; border: none; padding: 10px;")

        card_layout.addWidget(icon_label)
        card_layout.addWidget(lbl_title)
        card_layout.addWidget(lbl_content)
        card_layout.addStretch()

        layout.addWidget(card)
        return page

    def next_page(self):
        curr = self.stacked_widget.currentIndex()
        if curr < self.stacked_widget.count() - 1:
            self.stacked_widget.setCurrentIndex(curr + 1)
            self.animate_transition(self.stacked_widget.currentWidget())

    def prev_page(self):
        curr = self.stacked_widget.currentIndex()
        if curr > 0:
            self.stacked_widget.setCurrentIndex(curr - 1)
            self.animate_transition(self.stacked_widget.currentWidget())

    def animate_transition(self, widget):
        # Basit bir animasyon efekti (Opaklık geçişi)
        anim = QPropertyAnimation(widget, b"windowOpacity")
        anim.setDuration(500)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FizikApp()
    window.show()
    sys.exit(app.exec_())