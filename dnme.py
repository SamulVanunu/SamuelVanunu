import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import yt_dlp
from PIL import Image, ImageTk
import requests
from io import BytesIO

class ModernVideoSesIndirici:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 Ultra Video & Ses İndirici")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.root.configure(bg='#2c3e50')
        
        # Modern stil
        self.setup_styles()
        
        # Ana container
        main_container = tk.Frame(root, bg='#2c3e50')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_container)
        
        # Content alanı
        self.create_content(main_container)
        
        # Footer
        self.create_footer(main_container)
        
        # Varsayılan indirme konumu
        self.location_entry.insert(0, os.path.expanduser("~/Downloads"))
    
    def setup_styles(self):
        """Modern stilleri ayarla"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Özel stiller
        style.configure('Modern.TFrame', background='#34495e')
        style.configure('Title.TLabel', background='#34495e', foreground='#ecf0f1', font=('Arial', 18, 'bold'))
        style.configure('Subtitle.TLabel', background='#34495e', foreground='#bdc3c7', font=('Arial', 10))
        style.configure('Modern.TButton', font=('Arial', 10, 'bold'), padding=10)
        style.configure('Accent.TButton', background='#e74c3c', foreground='white')
        style.configure('Success.TLabel', background='#34495e', foreground='#2ecc71', font=('Arial', 10))
        style.configure('Modern.TEntry', font=('Arial', 10), padding=8)
        style.configure('Modern.TRadiobutton', background='#34495e', foreground='#ecf0f1', font=('Arial', 9))
    
    def create_header(self, parent):
        """Header bölümünü oluştur"""
        header_frame = ttk.Frame(parent, style='Modern.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Başlık
        title_label = ttk.Label(header_frame, 
                               text="🎬 ULTRA VIDEO & SES İNDİRİCİ", 
                               style='Title.TLabel')
        title_label.pack(pady=(10, 5))
        
        # Alt başlık
        subtitle_label = ttk.Label(header_frame,
                                  text="YouTube'dan kaliteli video ve ses indirin • Hızlı ve Güvenli",
                                  style='Subtitle.TLabel')
        subtitle_label.pack(pady=(0, 10))
    
    def create_content(self, parent):
        """İçerik bölümünü oluştur"""
        content_frame = ttk.Frame(parent, style='Modern.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sol panel - Girişler
        left_panel = ttk.Frame(content_frame, style='Modern.TFrame')
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Sağ panel - Bilgi ve istatistikler
        right_panel = ttk.Frame(content_frame, style='Modern.TFrame')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.create_input_panel(left_panel)
        self.create_info_panel(right_panel)
    
    def create_input_panel(self, parent):
        """Giriş panelini oluştur"""
        # URL Girişi
        url_section = ttk.LabelFrame(parent, text="🔗 YouTube URL", style='Modern.TFrame')
        url_section.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(url_section, text="Video URL:", style='Modern.TLabel').pack(anchor=tk.W, pady=(10, 5))
        
        self.url_entry = ttk.Entry(url_section, width=50, style='Modern.TEntry', font=('Arial', 11))
        self.url_entry.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Hızlı test butonları
        test_frame = ttk.Frame(url_section, style='Modern.TFrame')
        test_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        test_urls = [
            ("🎥 Kısa Video", "https://www.youtube.com/watch?v=9HcOc7gL1E0"),
            ("🎵 Müzik", "https://www.youtube.com/watch?v=6T7pUEZfgdA"),
            ("📚 Eğitim", "https://www.youtube.com/watch?v=rfscVS0vtbw")
        ]
        
        for text, url in test_urls:
            btn = ttk.Button(test_frame, text=text, 
                           command=lambda u=url: self.set_test_url(u),
                           style='Modern.TButton')
            btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # İndirme Konumu
        location_section = ttk.LabelFrame(parent, text="📁 İndirme Konumu", style='Modern.TFrame')
        location_section.pack(fill=tk.X, pady=(0, 15))
        
        location_frame = ttk.Frame(location_section, style='Modern.TFrame')
        location_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.location_entry = ttk.Entry(location_frame, style='Modern.TEntry')
        self.location_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        ttk.Button(location_frame, text="Gözat", 
                  command=self.browse_location, style='Modern.TButton').pack(side=tk.RIGHT)
        
        # Format Seçimi
        format_section = ttk.LabelFrame(parent, text="⚙️ İndirme Ayarları", style='Modern.TFrame')
        format_section.pack(fill=tk.X, pady=(0, 15))
        
        # Format
        format_frame = ttk.Frame(format_section, style='Modern.TFrame')
        format_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(format_frame, text="Format:", style='Modern.TLabel').pack(side=tk.LEFT)
        
        self.format_var = tk.StringVar(value="video")
        ttk.Radiobutton(format_frame, text="🎥 Video (MP4)", 
                       variable=self.format_var, value="video", style='Modern.TRadiobutton').pack(side=tk.LEFT, padx=(20, 10))
        ttk.Radiobutton(format_frame, text="🎵 Ses (MP3)", 
                       variable=self.format_var, value="audio", style='Modern.TRadiobutton').pack(side=tk.LEFT)
        
        # Kalite
        quality_frame = ttk.Frame(format_section, style='Modern.TFrame')
        quality_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Label(quality_frame, text="Kalite:", style='Modern.TLabel').pack(side=tk.LEFT)
        
        self.quality_var = tk.StringVar(value="1080p")
        qualities = [("1080p Full HD", "1080p"), ("720p HD", "720p"), 
                    ("480p Standart", "480p"), ("360p Düşük", "360p")]
        
        for text, value in qualities:
            ttk.Radiobutton(quality_frame, text=text, 
                           variable=self.quality_var, value=value, style='Modern.TRadiobutton').pack(side=tk.LEFT, padx=(10, 5))
        
        # İndirme Butonu
        button_frame = ttk.Frame(parent, style='Modern.TFrame')
        button_frame.pack(fill=tk.X, pady=20)
        
        self.download_button = ttk.Button(button_frame, 
                                        text="🚀 İNDİRMEYİ BAŞLAT", 
                                        command=self.start_download,
                                        style='Accent.TButton')
        self.download_button.pack(fill=tk.X, pady=10)
        
        # İlerleme çubuğu
        self.progress = ttk.Progressbar(button_frame, mode='indeterminate', length=100)
        self.progress.pack(fill=tk.X, pady=5)
        
        # Durum etiketi
        self.status_label = ttk.Label(button_frame, 
                                     text="✅ Sistem hazır - Test butonlarından birini deneyin!", 
                                     style='Success.TLabel')
        self.status_label.pack(pady=5)
    
    def create_info_panel(self, parent):
        """Bilgi panelini oluştur"""
        info_frame = ttk.LabelFrame(parent, text="ℹ️ Sistem Bilgisi", style='Modern.TFrame')
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        # İstatistikler
        stats_text = """
🎯 ÖZELLİKLER

✓ YouTube uyumlu
✓ HD kalite desteği
✓ Hızlı indirme
✓ MP3 dönüştürme
✓ Türkçe arayüz
✓ Güvenli kullanım

📊 SİSTEM

• yt-dlp motoru
• Güncel API
• Stabil bağlantı
• Hata yönetimi

⚠️ UYARILAR

• Kişisel kullanım
• Telif haklarına dikkat
• Yasal sınırlar içinde
        """
        
        info_label = ttk.Label(info_frame, text=stats_text, 
                              style='Modern.TLabel', justify=tk.LEFT)
        info_label.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Son indirmeler
        history_frame = ttk.LabelFrame(parent, text="📋 Son İndirmeler", style='Modern.TFrame')
        history_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.history_text = tk.Text(history_frame, height=6, bg='#2c3e50', fg='#ecf0f1', 
                                   font=('Arial', 8), wrap=tk.WORD)
        self.history_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.history_text.insert(tk.END, "Henüz indirme yapılmadı...\n")
        self.history_text.config(state=tk.DISABLED)
    
    def set_test_url(self, url):
        """Test URL'sini ayarla"""
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, url)
        self.status_label.config(text="✅ Test URL'si ayarlandı! İndirmek için butona tıkla.")
    
    def browse_location(self):
        """İndirme konumu seç"""
        directory = filedialog.askdirectory()
        if directory:
            self.location_entry.delete(0, tk.END)
            self.location_entry.insert(0, directory)
    
    def start_download(self):
        """İndirme işlemini başlat"""
        url = self.url_entry.get().strip()
        location = self.location_entry.get().strip()
        
        if not url:
            messagebox.showerror("Hata", "❌ Lütfen bir YouTube URL'si girin.")
            return
        
        if not location:
            messagebox.showerror("Hata", "❌ Lütfen bir indirme konumu seçin.")
            return
        
        # İndirme işlemini ayrı bir thread'de başlat
        thread = threading.Thread(target=self.download_with_yt_dlp, args=(url, location))
        thread.daemon = True
        thread.start()
        
        # İlerleme çubuğunu başlat
        self.progress.start(15)
        self.download_button.config(state="disabled")
        self.status_label.config(text="📥 İndiriliyor... Lütfen bekleyin!")
    
    def download_with_yt_dlp(self, url, location):
        """yt-dlp ile video/ses indirme"""
        try:
            self.root.after(0, lambda: self.status_label.config(text="🔗 YouTube'a bağlanıyor..."))
            
            # yt-dlp ayarları
            ydl_opts = {
                'outtmpl': os.path.join(location, '%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
            }
            
            if self.format_var.get() == "video":
                # VIDEO indirme ayarları
                ydl_opts['format'] = f'bestvideo[height<={self.quality_var.get().replace("p", "")}]+bestaudio/best'
            else:
                # SES indirme ayarları
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            
            # İndirme işlemi
            self.root.after(0, lambda: self.status_label.config(text="📥 Dosya indiriliyor..."))
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                # Ses indirildiyse uzantıyı düzelt
                if self.format_var.get() == "audio":
                    filename = filename.rsplit('.', 1)[0] + '.mp3'
                
                # Geçmişe ekle
                self.add_to_history(info.get('title', 'Bilinmeyen'), 
                                  'Video' if self.format_var.get() == 'video' else 'Ses',
                                  info.get('duration', 0))
                
                # Başarı mesajı
                file_size = os.path.getsize(filename) // (1024*1024) if os.path.exists(filename) else "Bilinmiyor"
                self.root.after(0, self.download_complete, 
                              f"✅ {'Video' if self.format_var.get() == 'video' else 'Ses'} başarıyla indirildi!\n\n"
                              f"📺 Başlık: {info.get('title', 'Bilinmiyor')}\n"
                              f"📂 Konum: {filename}\n"
                              f"📊 Boyut: {file_size} MB\n"
                              f"⏱️ Süre: {info.get('duration', 0) // 60}:{info.get('duration', 0) % 60:02d}")
                
        except Exception as e:
            self.root.after(0, self.download_error, f"❌ İndirme hatası: {str(e)}")
    
    def add_to_history(self, title, format_type, duration):
        """İndirme geçmişine ekle"""
        self.history_text.config(state=tk.NORMAL)
        if "Henüz indirme yapılmadı" in self.history_text.get("1.0", "end-1c"):
            self.history_text.delete("1.0", tk.END)
        
        duration_str = f"{duration // 60}:{duration % 60:02d}" if duration > 0 else "Bilinmiyor"
        history_entry = f"✓ {title[:40]}... [{format_type}] - {duration_str}\n"
        self.history_text.insert(tk.END, history_entry)
        self.history_text.see(tk.END)
        self.history_text.config(state=tk.DISABLED)
    
    def download_complete(self, message):
        """İndirme tamamlandığında"""
        self.progress.stop()
        self.download_button.config(state="normal")
        self.status_label.config(text="🎉 İndirme tamamlandı!")
        messagebox.showinfo("Başarılı", message)
    
    def download_error(self, error_message):
        """Hata durumunda"""
        self.progress.stop()
        self.download_button.config(state="normal")
        self.status_label.config(text="❌ İndirme başarısız!")
        messagebox.showerror("Hata", error_message)

if __name__ == "__main__":
    root = tk.Tk()
    
    # Pencereyi ekranın ortasına yerleştir
    window_width = 800
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    app = ModernVideoSesIndirici(root)
    root.mainloop()