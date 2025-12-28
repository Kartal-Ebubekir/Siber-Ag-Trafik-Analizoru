from src.structures.custom_hash_map import CustomHashMap
from src.algorithms.heap_manager import MinHeap
from src.structures.trie import Trie
from src.algorithms.sorting import merge_sort_descending, quick_sort_alphabetical, binary_search_ip

class StreamProcessor:
  def __init__(self, k_top=10):
    self.k_top = k_top
    self.frequency_map = CustomHashMap(size=2000)
    self.top_k_heap = MinHeap(k_top)
    self.ip_trie = Trie()

  def process_item(self, item):
    self.ip_trie.insert(item) # Trie'ye Ekle

    # hash Map İşlemleri
    self.frequency_map.increment(item)
    current_freq = self.frequency_map.get(item)

    # heap yönetimi
    heap_index = self.top_k_heap.find_index(item)
    
    if heap_index != -1:
      self.top_k_heap.update_element(item, current_freq)
    
    else:
      if self.top_k_heap.size() < self.k_top:
        self.top_k_heap.push((current_freq, item))
      else:
        min_freq, min_item = self.top_k_heap.peek()
        if current_freq > min_freq:
          self.top_k_heap.pop()
          self.top_k_heap.push((current_freq, item))

  def get_top_list(self): # Ana liste için Merge Sort
    return merge_sort_descending(self.top_k_heap.heap)
  
  def get_alphabetical_list(self): # Raporlama için Quick Sort
    return quick_sort_alphabetical(self.top_k_heap.heap)
  
  def find_ip_binary(self, target_ip): # Arama için Quick Sort + Binary Search
    alpha_list = self.get_alphabetical_list()
    return binary_search_ip(alpha_list, target_ip)

  def search_ip(self, prefix): # Trie sonuçlarını bulur ve kendi Merge Sort algoritmamızla sıralar.
    raw_results = self.ip_trie.search_prefix(prefix) # ham IP listesini Trie'den al
    
    # frekansları bul ve paketle: [(50, '192.168...'), (10, '10.0...')]
    scored_results = []
    for ip in raw_results:
      freq = self.frequency_map.get(ip)
      scored_results.append((freq, ip))
  
    sorted_results = merge_sort_descending(scored_results) 
    final_list = [f"{ip:<16} (Frekans: {freq})" for freq, ip in sorted_results] # Ekranda güzel gözükmesi için string'e çevir
    
    return final_list