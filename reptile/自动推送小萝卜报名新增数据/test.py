from datetime import datetime

if __name__ == '__main__':
    s= '2025-02-10T15:08:04.544Z'
    df = datetime.strptime(s, '%Y-%m-%dT%H:%M:%S.%fZ')
    print(df.strftime("%Y-%m-%d %H:%M:%S"))