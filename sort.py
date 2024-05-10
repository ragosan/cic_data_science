def convert_to_range_mean(s):
    if s.startswith('>'):
        return float('500000')
    else:
        low, high = map(int, s.replace(',', '').split('-'))
        return (low + high) / 2

data = {
    '0-999': 1513, '1,000-1,999': 599, '10,000-14,999': 833, '100,000-124,999': 750, 
    '125,000-149,999': 483, '15,000-19,999': 529, '150,000-199,999': 434, '2,000-2,999': 390, 
    '20,000-24,999': 526, '200,000-249,999': 165, '25,000-29,999': 482, '250,000-299,999': 65, 
    '3,000-3,999': 305, '30,000-39,999': 728, '300,000-500,000': 74, '4,000-4,999': 289, 
    '40,000-49,999': 719, '5,000-7,499': 536, '50,000-59,999': 704, '60,000-69,999': 576, 
    '7,500-9,999': 408, '70,000-79,999': 524, '80,000-89,999': 405, '90,000-99,999': 377, 
    '> 500,000': 83
}


mean_key = min(data.keys(), key=lambda x: abs(sum(map(convert_to_range_mean, data.keys())) / len(data.keys())))
print("Mean Key:", mean_key)