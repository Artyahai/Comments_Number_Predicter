from parser import Create_Dataset
while True:
    link = input("Input your X link: ")
    ds = Create_Dataset(link, 1, 1)
    
    if link == 'exit':
        break
    else:
        ds.save_to_db()
