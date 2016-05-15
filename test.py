
def run_outer():
    tdict = {
        1: "outer",
    }
    tlist = ["outer"]
    run_inner(tdict, tlist)
    return (tdict, tlist)

def run_inner(tdict, tlist):
    tdict[1] = "inner"
    tdict[2] = "inner"
    tlist.append("inner")


if __name__ == "__main__":
    print(run_outer())