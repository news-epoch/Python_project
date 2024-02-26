

if __name__ == '__main__':
    for i in range(1, 2000):
        with open("test.txt", "a", encoding="utf-8") as fp:
            fp.write("https://connect.werally.com/searchResults/02108/page-{}?term=oncology&searchType=person&lat=42.360253&long=-71.058291&propFlow=true".format(str(i))+"\n")
