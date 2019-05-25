
if __name__ == "__main__":
	communities = []
	with open("./datas_paper/Dataset/communities/communities-2009-12-1.txt") as f:
		communities = [c.rstrip().split() for c in f.readlines()]