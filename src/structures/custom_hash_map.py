"""
Python'da dict tipi, aslında dahili olarak hash tablosu kullanır ve hızlı anahtar-değer eşleşmeleri sağlamak için optimize edilmiştir.
Ancak, kendi hash map implementasyonumu yazmanın, bu veri yapısının nasıl çalıştığını derinlemesine anlamak için çok öğretici olacağını düşünüyorum.
Hash map iki temel bileşene dayanır:
  - Hashing (Anahtarların Hashlenmesi): Anahtarların bir hash fonksiyonu ile belirli bir aralıkta sayısal değerlere dönüştürülmesi.
  - Collision Handling (Çakışma Yönetimi): İki farklı anahtarın aynı hash değerine sahip olması durumunda, bu çakışmayı nasıl yöneteceğimiz.
"""
class CustomHashMap:
  def __init__(self, size=1000):
    self.size = size  # Hash tablosunun boyutu (Kova sayısı)
    self.buckets = [[] for _ in range(size)]  # İçi boş listelerden oluşan bir liste oluşturur.for _ in range(size) ile for i in range(size) aynı işleve sahiptir.Ancak döngüde değişken kullanılmıyorsa bu değikei kullanmıyorum mesajı '_' karakteri ile verilir.
    self.count = 0  # Toplam eleman sayısı

  def _hash_function(self, key):  # Anahtarı (key) bir indeks numarasına çevirir.
    """
    pythonun gömülü hash() fonksiyonu immutable(int,float,str,tuple,vb) veri tiplerini hashlemek için kıullanılır.Sayılarda genelde kendisine eşit olur.
    Ancak string ve tuple gibi veri tiplerini belirli bir algoritmayla sayıya çevirir.
    örn : hash(42) = 42, hash(-7) = -7, hash("abc") = (örn) -152917, hash((1,2)) = (örn) 3713081631934410656
    Hash fonksiyonu, aynı değerler için her zaman aynı sayıyı üretir; farklı değerler için hash çakışması olasılığı çok düşüktür ama teorik olarak mümkündür.hash("abc") = hash("abc")
    """
    return hash(key) % self.size   # Tablo boyutuna göre mod alıyoruz.Sınırı aşmamak amacıyla

  def put(self, key, value):  # Anahtar-Değer çiftini ekler veya günceller.key = ip, value= frekans
    index = self._hash_function(key) # buckets liste tutan bir listedir.İndex değeri koyacagımız veya güncelleyeceiğimiz listeyi temsil eder.
    bucket = self.buckets[index] 

    # 1. Anahtar zaten bu kovada var mı diye bak?
    for i, (k, v) in enumerate(bucket): # Tuple'ları tek tek kontrol et
      if k == key: # Eğer eleman varsa
        bucket[i] = (key, value) # Değerini güncelle 
        return

    # 2. Yoksa yeni ekle
    bucket.append((key, value))
    self.count += 1

  def get(self, key):  # Anahtarın değerini döndürür. Yoksa None döner.
    index = self._hash_function(key)
    bucket = self.buckets[index]

    for k, v in bucket:
      if k == key:
        return v
    return None

  def increment(self, key): # Özel Fonksiyon: Bir anahtarın frekansını 1 artırır.Eğer anahtar yoksa, frekansı 1 olarak başlatır.
    current_val = self.get(key)
    if current_val is None:
      self.put(key, 1)
    else:
      self.put(key, current_val + 1)

  def contains(self, key): # get fonksiyonu ile temelde aynı şeyi yapar ancak bool deger döndürür.Okunabilirliği arttırmak için yazılmıştır.
    return self.get(key) is not None # Eğer değer varsa --> deger is not None --> True döner, Eğer değer yoksa --> None is not None --> False döner

