from cgi import test
from viewerGL import ViewerGL
import glutils
from mesh import Mesh
from cpe3d import Object3D, Camera, Transformation3D, Text
import numpy as np
import OpenGL.GL as GL
import pyrr
import time
import random

def main():
    viewer = ViewerGL()

    viewer.set_camera(Camera())
    viewer.cam.transformation.translation.y = 2
    viewer.cam.transformation.rotation_center = viewer.cam.transformation.translation.copy()

    program3d_id = glutils.create_program_from_file('shader.vert', 'shader.frag')
    programGUI_id = glutils.create_program_from_file('gui.vert', 'gui.frag')

    
    m = Mesh.load_obj('stegosaurus.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([2, 2, 2, 1]))
    tr = Transformation3D()
    tr.translation.y = -np.amin(m.vertices, axis=0)[1]
    tr.translation.z = -20
    tr.rotation_center.z = 0.2
    texture = glutils.load_texture('stegosaurus.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object(o)

    r = Mesh()
    p0, p1, p2, p3 = [-25, 0, -25], [25, 0, -25], [25, 0, 25], [-25, 0, 25]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    r.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    r.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('route.jpg')
    o = Object3D(r.load_to_gpu(), r.get_nb_triangles(), program3d_id, texture, Transformation3D())
    viewer.add_object(o)
    
    
    c=Mesh.load_obj('cube.obj')
    vao=c.load_to_gpu()
    c.normalize()
    # c.apply_matrix(pyrr.matrix44.create_from_scale([1, 5, 5, 1]))
    texture = glutils.load_texture('font_cube.jpg')
    
    for j in range(50):
    
        nb_cube=random.randint(2,3)
        for i in range(nb_cube):
            tr = Transformation3D()
            tr.translation.x = random.randint(-8,8)
            tr.translation.y = -np.amin(c.vertices, axis=0)[1]
            tr.translation.z = 40*j
            tr.rotation_center.z = 0.2
            p = Object3D(vao, c.get_nb_triangles(), program3d_id, texture, tr)
            viewer.add_object(p)

               
    viewer.run(viewer,programGUI_id)

if __name__ == '__main__':
    main()