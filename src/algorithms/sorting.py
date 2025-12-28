def merge_sort_descending(arr): # Frekansa göre büyükten küçüğe (descending) sıralar
  if len(arr) <= 1:
    return arr
  
  middle = len(arr) // 2
  leftside = merge_sort_descending(arr[:middle])
  rightside = merge_sort_descending(arr[middle:])
  return _merge_desc(leftside,rightside)

def _merge_desc(leftside, rightside):
  result = []
  i = j = 0
  while i < len(leftside) and j < len(rightside):
    # tuple yapısı: (frekans, ip) -> 0. index frekansı tutuyor
    if leftside[i][0] >= rightside[j][0]: 
      result.append(leftside[i]) # azalan sırada yazdıgımız icin büyük olanı alıyoruz
      i += 1
    else:
      result.append(rightside[j])
      j += 1
  
  result.extend(leftside[i:])
  result.extend(rightside[j:])
  return result

def quick_sort_alphabetical(arr):
  if len(arr) <= 1:
    return arr
  else:
    pivot = arr[0] # İlk elemanı pivot kabul ediyoruz
    less = [x for x in arr[1:] if x[1] <= pivot[1]] # Pivot'tan küçük olanlar (ascıı numarasına göre karşılaştırılıyor)
    greater = [x for x in arr[1:] if x[1] > pivot[1]] # Pivot'tan büyük olanlar
    return quick_sort_alphabetical(less) + [pivot] + quick_sort_alphabetical(greater)

def binary_search_ip(sorted_arr, target_ip): # Alfabetik sıralı listede Binary Search ile IP arar.Dönüş degeri: bulunursa (index, (freq, ip)), bulunamazsa -1
  low = 0
  high = len(sorted_arr)-1
  while low <= high:
    middle = (low+high) // 2

    if sorted_arr[middle][1] == target_ip:
      return middle,sorted_arr[middle]

    elif sorted_arr[middle][1] < target_ip:
      low = middle+1
    
    else: 
      high = middle-1
  
  return -1 # Aranan ip degeri bulunmazsa