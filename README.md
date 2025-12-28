# 🛡️ Siber Güvenlik Ağ Trafik Analizörü

Bu proje, büyük ölçekli sunucu loglarını (erişim kayıtlarını) analiz ederek siber güvenlik tehdit istihbaratı sağlamak, ağ trafiğini izlemek ve en çok etkileşimde bulunan IP adreslerini tespit etmek amacıyla geliştirilmiş bir **Masaüstü Uygulamasıdır**.

Veri Yapıları ve Algoritmalar dersi kapsamında, Python'un hazır kütüphaneleri yerine **kendi yazdığımız özel veri yapıları** (Custom Data Structures) kullanılarak tasarlanmıştır.

---

## Projenin Genel Amacı ve Özellikleri

Bu yazılımın temel işlevleri ve akışı şöyledir:

* **1. Log Okuma ve İşleme:** `.log`, `.txt` veya `.json` formatındaki ham sunucu kayıtlarını okur. İçerisindeki IP adreslerini *Regex* (Düzenli İfadeler) ile ayıklar.
* **2. Canlı Trafik Simülasyonu:** Verileri anında belleğe yüklemek yerine, gerçek bir ağ trafiği akıyormuş gibi satır satır işler (Stream Processing).
* **3. Frekans Analizi (Hash Map):** Hangi IP adresinin ağa kaç kez bağlandığını hesaplar. Bunu yaparken çakışmaları (collision) önleyen özel bir *Hash Map* yapısı kullanır.
* **4. Lider Tablosu (Top-K Analizi):** Ağa en çok yük bindiren veya saldırı şüphesi taşıyan ilk 10 IP adresini anlık olarak tespit eder. Bunun için *Min-Heap* algoritması kullanılır.
* **5. Hızlı Arama Motoru (Trie):** Binlerce IP adresi arasında belirli bir başlangıç (örn: "192.168.") ile başlayanları milisaniyeler içinde bulur.
* **6. Raporlama:** Analiz sonuçlarını sıralı bir şekilde hem ekrana yansıtır hem de dosya olarak kaydeder.

---

## Kullanılan Teknolojiler ve Algoritmalar

Projede performans ve veri bütünlüğü için aşağıdaki yapılar manuel olarak kodlanmıştır:

| Bileşen | Kullanılan Yapı / Algoritma | Görevi |
|---|---|---|
| **Veri Sayma** | `Custom Hash Map` | IP adreslerinin tekrar sayılarını tutar. (Collision Handling: Chaining) |
| **Sıralama (Top 10)** | `Min-Heap` | En yüksek frekanslı 10 IP'yi hafızayı yormadan tutar. |
| **Arama (Search)** | `Trie (Prefix Tree)` | IP adreslerini basamaklarına göre ağaç yapısında saklar ve hızlı arama sağlar. |
| **Sıralama (Rapor)** | `Merge Sort` | Ana veriyi bozmadan (Stable) büyükten küçüğe sıralama yapar. |
| **Sıralama (Alfabetik)**| `Quick Sort` | IP adreslerini alfabetik dizmek için kullanılır. |
| **Arayüz** | `Tkinter` | Kullanıcı dostu ve donmayan (Multi-threaded) bir arayüz sağlar. |

---

## Proje Dosya Yapısı

Proje modüler bir mimariye sahiptir:

```text
PROJE9/
│
├── main.py                # Uygulamanın giriş noktası ve Arayüz (GUI) kodları
├── data/                  # İşlenecek log dosyaları (access.log vb.)
├── raporlar/              # Oluşturulan analiz raporları
│
└── src/                   # Kaynak kodlar
    ├── algorithms/        # Algoritma modülleri
    │   ├── heap_manager.py
    │   ├── sorting.py
    │   └── stream_processor.py
    │
    └── structures/        # Veri yapıları modülleri
        ├── custom_hash_map.py
        └── trie.py


## Kurulum ve Çalıştırma

Projeyi bilgisayarınızda çalıştırmak için şu adımları izleyin:

1. **Projeyi İndirin:**
   Bu repoyu bilgisayarınıza klonlayın veya ZIP olarak indirin.
   ```bash
   git clone [https://github.com/KULLANICI_ADINIZ/Network-Traffic-Analyzer.git](https://github.com/KULLANICI_ADINIZ/Network-Traffic-Analyzer.git)

2. **Dizine Girin:**
   ```bash
   cd Network-Traffic-Analyzer

3. **Uygulamayı Başlatın:**
   Python yüklü olduğundan emin olun ve aşağıdaki komutu çalıştırın:
   ```bash
   python main.py

4. **Kullanım:**
   * Açılan ekranda **"Dosya Seç"** butonuna basarak `data` klasöründeki bir log dosyasını seçin.
   * **"BAŞLAT"** butonuna basarak analizi izleyin.
   * Analiz bittiğinde veya durdurduğunuzda **Trie Arama** özelliğini kullanabilir veya **Rapor Al** diyerek sonuçları kaydedebilirsiniz.

---

### Geliştirici Notu
Bu proje, veri yapılarının (Hash Map, Heap, Trie) çalışma mantığını derinlemesine anlamak ve gerçek hayat senaryosu (Siber Güvenlik) üzerinde uygulamak amacıyla geliştirilmiştir.