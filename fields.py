import matplotlib as mpl


def gen_fields():
    fields = []
    rgbc = [[212, 212, 212], [186, 186, 186], [150, 150, 150],
            [115, 115, 115], [77, 77, 77], [59, 59, 59]]
    rgbc2 = []
    lims = [[[135, 195, 255], [0, 43, 87]], [
        [255, 210, 156], [173, 101, 14]], [[251, 255, 145], [205, 212, 21]], [[166, 255, 167], [6, 207, 8]], [[215, 156, 255], [118, 17, 186]]]
    bounds = [100, 200, 400, 600, 800,
              1000]
    l = 1000
    for item in lims:
        up = item[0]
        bo = item[1]
        d1 = (bo[0] - up[0])/7.0
        d2 = (bo[1] - up[1])/7.0
        d3 = (bo[2] - up[2])/7.0
        for i in range(7):
            rgbc.append([up[0] + d1*i, up[1] + d2*i, up[2] + d3*i])
        for i in range(5):
            l += 200
            bounds.append(l)

    l += 200
    bounds.append(l)
    rgbc.append([255, 122, 244])  # Upper bound
    for item in rgbc:
        for i in range(3):
            rgbc2.append([item[0]/255.0, item[1]/255.0, item[2]/255.0])
    cmap = mpl.colors.ListedColormap(rgbc2)
    cmap.set_under("white")
    fields.append({
        "cmap": cmap,
        "name": "cape",
    })
    return fields
