import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import json
import os
import re
from datetime import datetime
from src.algorithms.stream_processor import StreamProcessor

class TrafficAnalyzerApp:
  def __init__(self, root):
    self.root = root # programının ana çerçevesi
    self.root.title("Siber Ağ Trafik Analizörü (Proje 9 - Final)") # Baslık
    self.root.geometry("1100x750") # Uygulama acılınca gösterilecek pencere boyutu (Genişlik x Yükseklik)
    
    # DEĞİŞKENLER
    self.processor = None # Arka planda çalışacak analiz algoritması (Henüz baslatmadık)
    self.is_running = False
    self.raw_data = []
    
    self.current_index = 0 # Kaldıgımız yeri hatırlamak için sayaç
    self.current_filename = None
    
    # Daha modern görünüm için ttk kullandım
    style = ttk.Style()
    style.theme_use('clam') 
    
    self.setup_ui() # : Ekranı çizecek fonksiyon
    
  def setup_ui(self):
    # SOL PANEL (Sabit Genişlik)
    sidebar_frame = tk.Frame(self.root, width=280, bg="#d9d9d9", padx=10, pady=10)
    sidebar_frame.pack(side="left", fill="y") # pack ekrana yerleştirme komutudur. (fill="y": Sol panel yukarıdan aşağıya tüm yüksekliği kaplasın.  expand=True: Sağ panel, pencere büyütülürse genişlesin.)
    sidebar_frame.pack_propagate(False) 
    
    # SAĞ PANEL (Esnek Alan)
    main_frame = tk.Frame(self.root, padx=10, pady=10, bg="white")
    main_frame.pack(side="left", fill="both", expand=True)

    # === SOL PANEL İÇERİĞİ ===
    
    tk.Label(sidebar_frame, text="KONTROL PANELİ", bg="#d9d9d9", font=("Arial", 11, "bold")).pack(pady=(0, 15))

    # 1. Kutu: Dosya
    box1 = ttk.LabelFrame(sidebar_frame, text="1. Dosya Yükleme")  # Ekrana yazar. ilk parametre hangi alana yazacagıdır text ile de içeriği yazıyoruz.
    box1.pack(fill="x", pady=5)
    
    self.btn_load = ttk.Button(box1, text="Dosya Seç", command=self.select_file) # Kullanıcı butona tıkladığında hangi fonksiyonun çalışacağını command= ile belirtiriz. Örneğin "Dosya Seç"e basınca select_file çalışır
    self.btn_load.pack(fill="x", padx=5, pady=5)

    self.btn_report = ttk.Button(box1, text="Rapor Al", command=self.save_report, state="disabled") # Başlangıçta bazı butonlar (Rapor Al, Durdur) tıklanamaz haldedir. Veri yüklenince açılacaklar (state="disabled")
    self.btn_report.pack(fill="x", padx=5, pady=5)

    # 2. Kutu: Analiz
    box2 = ttk.LabelFrame(sidebar_frame, text="2. Analiz İşlemleri")
    box2.pack(fill="x", pady=15)
    
    self.btn_start = ttk.Button(box2, text="BAŞLAT / DEVAM ET", command=self.start_analysis, state="disabled")
    self.btn_start.pack(fill="x", padx=5, pady=5)
    
    self.btn_stop = ttk.Button(box2, text="DURDUR", command=self.stop_analysis_click, state="disabled")
    self.btn_stop.pack(fill="x", padx=5, pady=5)

    # 3. Kutu: Arama
    box3 = ttk.LabelFrame(sidebar_frame, text="3. Arama Motoru")
    box3.pack(fill="x", pady=15)
    
    tk.Label(box3, text="IP Adresi:", bg="#d9d9d9").pack(anchor="w", padx=5)
    self.entry_search = ttk.Entry(box3)
    self.entry_search.pack(fill="x", padx=5, pady=5)
    
    self.btn_trie = ttk.Button(box3, text="Trie Ara (Prefix)", command=self.search_trie, state="disabled")
    self.btn_trie.pack(fill="x", padx=5, pady=2)
    
    self.btn_binary = ttk.Button(box3, text="Binary Ara (Tam)", command=self.search_binary, state="disabled")
    self.btn_binary.pack(fill="x", padx=5, pady=2)
    
    # Durum Bilgisi
    self.lbl_status = tk.Label(sidebar_frame, text="Hazır.", bg="#d9d9d9", fg="#333", wraplength=260, justify="left")
    self.lbl_status.pack(side="bottom", fill="x", pady=10)


    # === SAĞ PANEL İÇERİĞİ ===
    
    # Üst: Tablo
    top_frame = ttk.LabelFrame(main_frame, text="🏆 Lider Tablosu (Top-10 IP)") 
    top_frame.pack(side="top", fill="both", expand=True, pady=(0, 10))
    
    cols = ("sira", "frekans", "ip")
    self.tree = ttk.Treeview(top_frame, columns=cols, show="headings") # Treeview: Tkinter'da Excel benzeri tablolar oluşturmak için kullanılır.columns: Sütun isimlerini tanımlar (Sıra, Frekans, IP).heading: Sütun başlıklarında ne yazacağını belirler.
    self.tree.heading("sira", text="Sıra")
    self.tree.heading("frekans", text="Frekans")
    self.tree.heading("ip", text="IP Adresi")
    self.tree.column("sira", width=50, anchor="center")
    self.tree.column("frekans", width=100, anchor="center")
    self.tree.column("ip", width=250, anchor="center")
    
    tree_scroll = ttk.Scrollbar(top_frame, orient="vertical", command=self.tree.yview)
    self.tree.configure(yscrollcommand=tree_scroll.set)
    tree_scroll.pack(side="right", fill="y")
    self.tree.pack(fill="both", expand=True)

    # Alt: Log Ekranı
    bot_frame = ttk.LabelFrame(main_frame, text="📡 Canlı Log Akışı")
    bot_frame.pack(side="bottom", fill="both", expand=True)
    
    self.log_text = tk.Text(bot_frame, height=12, state="disabled", font=("Consolas", 9)) # Çok satırlı yazı alanı. Canlı loglar buraya akacak. Kullanıcı burayı elle değiştiremesin diye state="disabled" 
    self.log_text.pack(side="left", fill="both", expand=True)

    log_scroll = ttk.Scrollbar(bot_frame, orient="vertical", command=self.log_text.yview)
    self.log_text.configure(yscrollcommand=log_scroll.set)
    log_scroll.pack(side="right", fill="y")
    

  # --- FONKSİYONLAR ---

  def select_file(self):
    path = filedialog.askopenfilename(filetypes=[("Log/Txt/Json", "*.log *.txt *.json"), ("All", "*.*")]) # dosya seçme penceresini açar.seçilen dosyanın yolunu döndürür.
    if not path: return
    
    # Dosya ismini (uzantısız) al ve kaydet
    filename_with_ext = os.path.basename(path) # örn: server_logs.txt
    self.current_filename = os.path.splitext(filename_with_ext)[0] # örn: server_logs

    self.lbl_status.config(text=f"Dosya işleniyor:\n{os.path.basename(path)}")
    self.root.update()

    if path.endswith(".json"):
      self.load_data(path)
    else:
      json_path = self.convert_log(path)
      if json_path: self.load_data(json_path)

  def convert_log(self, path): # Eğer dosya .log veya .txt ise, içindeki IP adreslerini Regex (Düzenli İfadeler) ile bulur (re.compile kısmı) ve JSON formatına çevirir. Bu, veriyi daha kolay işlememizi sağlar.
    try:
      self.log_msg(f"DÖNÜŞÜM: {path}")
      ptrn = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})') 
      data = []
      with open(path, 'r', encoding='latin-1') as f:
        for line in f:
          m = ptrn.search(line)
          if m: data.append({"ip": m.group(1)})
      
      base_name = os.path.basename(path) 
      name_only = os.path.splitext(base_name)[0]
      out = f"data/{name_only}_converted.json"
      if not os.path.exists("data"): os.makedirs("data")
      with open(out, 'w', encoding='utf-8') as f:
        json.dump(data, f)
      return out
    except Exception as e:
      messagebox.showerror("Hata", str(e))
      return None

  def load_data(self, path):
    try:
      with open(path, 'r', encoding='utf-8') as f:
        self.raw_data = json.load(f)
        
      # YENİ DOSYA YÜKLENDİĞİNDE HER ŞEYİ SIFIRLA
      self.processor = None 
      self.current_index = 0
      
      # Arama butonlarını tekrar kapat (Çünkü processor silindi)
      if hasattr(self, 'btn_trie'): # Hata almamak için kontrol
        self.btn_trie.config(state="disabled")   
        self.btn_binary.config(state="disabled") 

      self.lbl_status.config(text=f"YÜKLENDİ: {len(self.raw_data)} Kayıt.\nAnalizi başlatabilirsiniz.")
      self.btn_start.config(state="normal")
      self.log_msg(f"Veri Hazır: {len(self.raw_data)} satır.")
      
      # Ekranları temizle
      self.log_text.config(state="normal")
      self.log_text.delete(1.0, "end")
      self.log_text.config(state="disabled")
      for i in self.tree.get_children(): self.tree.delete(i)
      
    except Exception as e:
      messagebox.showerror("Hata", str(e))

  def log_msg(self, msg):
    self.log_text.config(state="normal")
    self.log_text.insert("end", msg + "\n")
    self.log_text.see("end")
    self.log_text.config(state="disabled")

  def start_analysis(self):
    # EĞER İŞLEMCİ YOKSA (İLK DEFA BAŞLIYORSA) OLUŞTUR
    if self.processor is None:
        self.processor = StreamProcessor(k_top=10) # Algoritmayı baslat
        self.current_index = 0
        
        # Ekranı sadece ilk başta temizle
        self.log_text.config(state="normal")
        self.log_text.delete(1.0, "end")
        self.log_text.config(state="disabled")
        for i in self.tree.get_children(): self.tree.delete(i)
    
    self.is_running = True
    self.btn_start.config(state="disabled")
    self.btn_load.config(state="disabled")
    self.btn_stop.config(state="normal")
    self.btn_report.config(state="disabled")
    self.btn_trie.config(state="disabled")   
    self.btn_binary.config(state="disabled") 
    
    self.thread = threading.Thread(target=self.run_stream)
    self.thread.daemon = True
    self.thread.start()

  def stop_analysis_click(self):
    self.is_running = False
    self.lbl_status.config(text=f"DURAKLATILDI. ({self.current_index}. veride)")
    self.reset_ui()

  def reset_ui(self):
    self.btn_start.config(state="normal")
    self.btn_load.config(state="normal")
    self.btn_stop.config(state="disabled")
    self.btn_report.config(state="normal")
    if self.processor is not None: # Sadece processor varsa
      self.btn_trie.config(state="normal")  
      self.btn_binary.config(state="normal")   

  def run_stream(self):
    total = len(self.raw_data)
    
    # DÖNGÜYÜ BAŞTAN DEĞİL, KALDIĞI YERDEN (current_index) BAŞLATIYORUZ
    # range(başlangıç, bitiş)
    for i in range(self.current_index, total):
      if not self.is_running: 
        return
      
      log = self.raw_data[i]
      self.processor.process_item(log["ip"])
      
      # Kaldığımız yeri güncelle
      self.current_index = i + 1
      
      if self.current_index % 10 == 0:
        time.sleep(0.005)
        self.root.after(0, self.update_gui, self.current_index, total, log["ip"])
        
    self.is_running = False
    self.root.after(0, lambda: self.finish())

  def finish(self):
    self.lbl_status.config(text="DURUM: Analiz Bitti.")
    self.reset_ui()
    # Bittiğinde sıfırlamıyoruz, belki adam arama yapacak.
    # Ama tekrar başlatırsa sıfırdan başlaması için processor'ü silmiyoruz,
    # Sadece dosya yeniden yüklenirse sıfırlanıyor.
    messagebox.showinfo("Bitti", "Analiz Tamamlandı.")

  def update_gui(self, cnt, total, ip):
    self.log_msg(f"[{cnt}] {ip}")
    self.lbl_status.config(text=f"İLERLEME: {cnt} / {total}\nSon IP: {ip}")
    
    if cnt % 50 == 0:
      top = self.processor.get_top_list()
      for i in self.tree.get_children(): self.tree.delete(i)
      for idx, (freq, val) in enumerate(top, 1):
        self.tree.insert("", "end", values=(idx, freq, val))

  def search_trie(self):
    if not self.processor: return
    query = self.entry_search.get()
    if not query: return
    
    results = self.processor.search_ip(query)
    
    if results:
      self.show_scrollable_popup(f"Trie Sonuçları ({len(results)})", 
                                 f"'{query}' ön ekiyle bulunanlar:", 
                                 results)
    else:
      messagebox.showinfo("Sonuç", "Eşleşen IP bulunamadı.")

  def show_scrollable_popup(self, title, header, content_list):
    popup = tk.Toplevel(self.root)
    popup.title(title)
    popup.geometry("400x500")
    
    tk.Label(popup, text=header, font=("Arial", 10, "bold"), pady=10).pack()
    
    frame = ttk.Frame(popup)
    frame.pack(fill="both", expand=True, padx=10, pady=(0,10))
    
    scrollbar = ttk.Scrollbar(frame, orient="vertical")
    scrollbar.pack(side="right", fill="y")
    
    text_area = tk.Text(frame, yscrollcommand=scrollbar.set, font=("Consolas", 10))
    text_area.pack(side="left", fill="both", expand=True)
    
    scrollbar.config(command=text_area.yview)
    
    text_area.insert("end", "\n".join(content_list))
    text_area.config(state="disabled")

  def search_binary(self):
    if not self.processor: return
    res = self.processor.find_ip_binary(self.entry_search.get())
    if res != -1: messagebox.showinfo("Bulundu", f"IP: {res[1][1]}\nFrekans: {res[1][0]}")
    else: messagebox.showerror("Yok", "Bulunamadı.")

  def save_report(self):
    if not self.processor: return
    if not os.path.exists("raporlar"): os.makedirs("raporlar")

    # Dinamik İsim Oluşturma (DosyaIsmi_Tarih_Saat.txt)
    date_str = datetime.now().strftime("%d-%m-%Y")
    safe_filename = f"{self.current_filename}_{date_str}.txt"
    full_path = os.path.join("raporlar", safe_filename)

    with open(full_path, "w", encoding="utf-8") as f:
      f.write(f"RAPOR DOSYASI: {self.current_filename}\n")
      f.write(f"OLUŞTURULMA TARİHİ: {time.ctime()}\n\n")
      f.write("=== TOP 10 IP LİSTESİ ===\n")
      for fr, ip in self.processor.get_top_list():
        f.write(f"{fr:<10} | {ip}\n")
    messagebox.showinfo("Tamam", "Rapor kaydedildi.")

if __name__ == "__main__":
  root = tk.Tk()
  app = TrafficAnalyzerApp(root)
  root.mainloop()