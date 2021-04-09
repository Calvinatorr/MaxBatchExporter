from pymxs import runtime as rt

def makePyramidMesh(side=20.0):
    halfside = side / 2.0
    pyramid = rt.mesh(
        vertices=[
            rt.point3(0.0, 0.0, side),
            rt.point3(-halfside, -halfside, 0.0),
            rt.point3(-halfside, halfside, 0.0),
            rt.point3(halfside, 0.0, 0.0)
        ],
        faces=[
            rt.point3(1, 2, 3),
            rt.point3(1, 3, 4),
            rt.point3(1, 4, 2),
            rt.point3(2, 3, 4)
        ]
    )\

    rt.redrawViews()
    return pyramid