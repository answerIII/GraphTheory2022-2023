file = "out.digg-friends"
new_file = "out.true_digg_friends"

with open(file, mode="rt") as f:
    with open(new_file, mode="wt") as nf:
        for line in f.readlines()[1:]:
            u, v, w, t = map(float,line.split())
            if t != 0 and u != v and w >= 0:
                nf.write(line)
            else:
                print(line)

f.close()
nf.close()
