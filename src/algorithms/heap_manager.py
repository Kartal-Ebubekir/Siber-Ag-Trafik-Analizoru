class MinHeap:
  def __init__(self, k_limit): 
    self.heap = []  # Verileri tutacağımız liste
    self.k_limit = k_limit  # k_limit: Heap'in tutacağı maksimum eleman sayısı (Top-K için).

  def size(self):
    # Heap'teki eleman sayısını döndür
    return len(self.heap)

  # Binary treee'de sol çocuk 2*i+1, sağ çocuk 2*i+2 formülü ile bulunur.Sağ ve sol çocugun parent'ı ise (i-1) // 2 ile bulunur.Sol çocuk için : ((2*i+1)-1) //2 --> i ; Sağ çocuk için : ((2*i+2)-1) // 2 --> integer bölme oldugundan cevap yine --> i
  def _parent(self, i):
    return (i - 1) // 2  
  def _left_child(self, i):
    return 2 * i + 1
  def _right_child(self, i):
    return 2 * i + 2

  def _swap(self, i, j):
    # İki elemanın yerini değiştiren yardımcı fonksiyon
    self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

  def push(self, eleman): # Heap'e yeni bir eleman ekler ve düzeni sağlar.
    self.heap.append(eleman) # elemanı listenin sonuna ekle

    # Min heap kuralını bozmamak için yukarı doğru taşı
    current_index = len(self.heap)-1 # Son elemanın (eklediğimiz elemanın) indeksi
    self._heapify_up(current_index) # Min heap bozulmus mu diye yukarıya doğru ilerle.Eleman eklerken heapify up , silerken heapify down kullanılır.

  def _heapify_up(self,index): # Verilen indeksteki elemanı, kurala uyana kadar yukarı taşır.
    if index == 0 : # Köke ulaştıysa dur
      return
    
    parent_index = self._parent(index)
    if self.heap[index] < self.heap[parent_index] : # Eğer verilemn indeksteki eleman parentdan küçükse
      self._swap(index,parent_index) # İki elemaanı yer değiştir
      self._heapify_up(parent_index) # Yer değiştirme sonrasında gelen eleman parent'a yerleşmiş olur.Köke kadar devam etmek için parentın indeksiyle (recursive olarak) işlemi tekrarla. 

  def pop(self): # Kökü listeden çıkarır ve döndürür.
    if self.size() == 0:
      return None
    
    root = self.heap[0] # Döndüreceğimiz değer (çıkaracağımız değer, Kök)
    last_item = self.heap.pop() # Son elemanı köke taşıyoruz (Listeden sonuncuyu siliyoruz ve degerini last_item'a atıyoruz).Buradaki pop fonksiyonu pythonun yerleşik fonksiyonudur, tanımladıgımız pop fonksiyonu değildir.Pythonun pop fonksiyonu bir listeden verilen indeksteki elemanı çıkarır ve değerini döndürür.Eğer indeks verilmezse son elemanı çıkarır ve değerini döndürür.
    if self.size() > 0: # Eğer liste boşsa zaten self.heap.pop listenin ilk elemanını silmiş demektir bu durum listede sadece 1 eleman varken yaşanabilir.
      self.heap[0] = last_item # last_item root oluyor
      self._heapify_down(0) # Min heap bozulmus mu diye aşağılara doğru ilerle.Eleman eklerken heapify up , silerken heapify down kullanılır.
    
    return root 

  def _heapify_down(self,index): # Verilen indexteki elemanı kurala uyana kadar aşağı taşır. 
    smallest = index
    left = self._left_child(index)
    right = self._right_child(index)

    if left < self.size() and self.heap[left] < self.heap[smallest]:
      smallest = left

    if right < self.size() and self.heap[right] < self.heap[smallest]:
      smallest = right

    if smallest != index : # En küçük eleman baslangıctaki eleman değilse 
      self._swap(index,smallest)
      self._heapify_down(smallest) # Yer değiştirme sonrasında sadece bir düğümü düzeltmiş oluyoruz ancak leaflere kadar kontrol etmemiz gerekiyor bu sebeple recursive  olarak işleme devam ediyoruz.

  def peek(self): # Silmeden kökü göster
    return self.heap[0] if self.size() > 0 else None

  def find_index(self, ip): # Heap içinde bir IP adresinin hangi indekste olduğunu bulur.
    for i, item in enumerate(self.heap): # Heap'in içindeki elemanların yapısı: (frekans, ip) yani item[0] = frekans, item[1] = ip
      if item[1] == ip:
        return i
    return -1

  def update_element(self, ip, new_freq): # Heap'teki bir IP'nin frekansını günceller ve düzeni sağlar.
    index = self.find_index(ip)
    if index == -1:
      return # Eleman heap'te yoksa işlem yapma

    self.heap[index] = (new_freq, ip) # Güncelle

    # Frekans değiştiği için yerini tekrar bulmalı
    # Hem aşağı hem yukarı bakıyoruz, hangisi gerekirse o çalışır
    self._heapify_down(index)
    self._heapify_up(index)