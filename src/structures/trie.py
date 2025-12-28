class TrieNode:
  def __init__(self):
    # Harfleri ve onlara bağlı diğer düğümleri tutacak yapı
    self.children = {} 
    
    # Burası kelimenin sonu mu?
    self.is_end_of_word = False

class Trie:
  def __init__(self):
    self.root = TrieNode()

  def insert(self, word):
    node = self.root
    for char in word:
      # Eğer bu harf çocuklarda yoksa, yeni bir yol (Node) aç
      if char not in node.children:
        node.children[char] = TrieNode()
      # O yola gir (aşağı in)
      node = node.children[char]
    # Kelime bitti, bayrağı dik
    node.is_end_of_word = True

  def search_prefix(self, prefix): # Verilen ön ek (prefix) ile başlayan tüm IP'leri bulur.Örn: '192.' verince '192.168.1.1' gibi tamamlanmışları döner.
    node = self.root
    # 1. Adım: Kullanıcının verdiği prefix'in sonuna kadar in (Klasörlere gir)
    for char in prefix:
      if char not in node.children:
        return [] # Öyle bir başlangıç yoksa boş dön
      node = node.children[char]
    
    # 2. Adım: Oradan aşağı sarkan tüm kelimeleri topla (Yardımcı fonk ile)
    results = []
    self._dfs(node, prefix, results)
    return results

  def _dfs(self, node, current_string, results): # Derinlik Öncelikli Arama (DFS): Ağacın derinliklerine inip bitmiş IP'leri toplar.
    if node.is_end_of_word:
      results.append(current_string)
    
    for char, child_node in node.children.items():
      self._dfs(child_node, current_string + char, results)