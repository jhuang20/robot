from display import *
from draw import *
from parser import *
from matrix import *
import math

screen = new_screen()
color = [ 0, 255, 0 ]
edges = []
polygons = []
t = new_matrix()
ident(t)
csystems = [ t ]
ARG_COMMANDS = [ 'box', 'sphere', 'torus', 'circle', 'bezier', 'hermite', 'line', 'scale', 'move', 'rotate', 'save' ]

def parse_file( fname, edges, polygons, csystems, screen, color ):

    f = open(fname)
    lines = f.readlines()
    t=new_matrix()
    ident(t)
    step = 100
    step_3d = 20

    c = 0
    while c < len(lines):
        line = lines[c].strip()
        #print ':' + line + ':'

        if line in ARG_COMMANDS:
            c+= 1
            args = lines[c].strip().split(' ')
        if line== 'push':
            csystems.append(t[:])

        if line== 'pop':
            csystems=csystems[:-1]
            t=csystems[-1]

        if line == 'sphere':
            #print 'SPHERE\t' + str(args)
            t=csystems[-1]
            add_sphere(polygons,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step_3d)
            matrix_mult( t, polygons )
            #print(t)
            #print(polygons)
            draw_lines(edges, screen, color)
            draw_polygons(polygons, screen, color)
            edges = []
            polygons = []

        elif line == 'torus':
            t=csystems[-1]
            #print 'TORUS\t' + str(args)
            add_torus(polygons,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), step_3d)
            matrix_mult( t, polygons )
            draw_lines(edges, screen, color)
            draw_polygons(polygons, screen, color)
            edges = []
            polygons = []
            #ident(t)

        elif line == 'box':
            t=csystems[-1]
            #print 'BOX\t' + str(args)
            add_box(polygons,
                    float(args[0]), float(args[1]), float(args[2]),
                    float(args[3]), float(args[4]), float(args[5]))
            #print(polygons)
            matrix_mult( t, polygons )
            #print(polygons)
            draw_lines(edges, screen, color)
            draw_polygons(polygons, screen, color)
            edges = []
            polygons = []
            #ident(t)

        elif line == 'circle':
            t=csystems[-1]
            #print 'CIRCLE\t' + str(args)
            add_circle(edges,
                       float(args[0]), float(args[1]), float(args[2]),
                       float(args[3]), step)
            matrix_mult( t, edges )
            draw_lines(edges, screen, color)
            draw_polygons(polygons, screen, color)
            edges = []
            polygons = []
            #ident(t)

        elif line == 'hermite' or line == 'bezier':
            t=csystems[-1]
            #print 'curve\t' + line + ": " + str(args)
            add_curve(edges,
                      float(args[0]), float(args[1]),
                      float(args[2]), float(args[3]),
                      float(args[4]), float(args[5]),
                      float(args[6]), float(args[7]),
                      step, line)
            matrix_mult( t, edges )
            draw_lines(edges, screen, color)
            draw_polygons(polygons, screen, color)
            edges = []
            polygons = []
            #ident(t)

        elif line == 'line':
            t=csystems[-1]
            #print 'LINE\t' + str(args)

            add_edge( edges,
                      float(args[0]), float(args[1]), float(args[2]),
                      float(args[3]), float(args[4]), float(args[5]) )
            matrix_mult( t, edges )
            draw_lines(edges, screen, color)
            draw_polygons(polygons, screen, color)
            edges = []
            polygons = []
            #ident(t)

        elif line == 'scale':
            t=csystems[-1]
            #print 'SCALE\t' + str(args)
            v = make_scale(float(args[0]), float(args[1]), float(args[2]))
            #matrix_mult(v,t)
            matrix_mult(t,v)
            print(v)
            t=v[:]
            print(t)
            csystems[-1]=t[:]


        elif line == 'move':
            t=csystems[-1]
            #print 'MOVE\t' + str(args)
            v = make_translate(float(args[0]), float(args[1]), float(args[2]))
            #matrix_mult(v,t)
            matrix_mult(t,v)
            print(v)
            t=v[:]
            print(t)
            csystems[-1]=t[:]

        elif line == 'rotate':
            t=csystems[-1]
            #print 'ROTATE\t' + str(args)
            theta = float(args[1]) * (math.pi / 180)

            if args[0] == 'x':
                v = make_rotX(theta)
            elif args[0] == 'y':
                v = make_rotY(theta)
            else:
                v = make_rotZ(theta)
            matrix_mult(t,v)
            print(v)
            t=v[:]
            print(t)
            csystems[-1]=t[:]

        elif line == 'ident':
            ident(transform)

        elif line == 'apply':
            matrix_mult( transform, edges )
            matrix_mult( transform, polygons )

        elif line == 'clear':
            edges = []
            polygons = []

        elif line == 'display' or line == 'save':
            #clear_screen(screen)
            #draw_lines(edges, screen, color)
            #draw_polygons(polygons, screen, color)

            if line == 'display':
                display(screen)
            else:
                save_extension(screen, args[0])
        c+= 1
parse_file( 'script', edges, polygons, csystems, screen, color )
