def banner():
    with open("banner.txt","r") as f:
        for line in f.readlines():
            print(line,end="")