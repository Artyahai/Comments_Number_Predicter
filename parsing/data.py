from parser import Create_Dataset
links = ()
for n in links:
    ds = Create_Dataset(n, 1, 1)
    ds.save_to_db()
