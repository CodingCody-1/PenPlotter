import time
from math import pi, sin, cos, sqrt, acos, asin
import Plotter as plotter

# ---------------------------------------------------------- #
# This code is 100% not stolen from "https://github.com/flodek/Mini_pen_plotter_RaspberryPI/blob/master/Gcode_executer.py"

def extract_XY(input):
    # given a movement command line, return the X Y position
    xchar_loc = input.index('X')
    i = xchar_loc+1
    while (47 < ord(input[i]) < 58) | (input[i] == '.') | (input[i] == '-'):
        i += 1
    x_pos = float(input[xchar_loc+1:i])

    ychar_loc = input.index('Y')
    i = ychar_loc+1
    while (47 < ord(input[i]) < 58) | (input[i] == '.') | (input[i] == '-'):
        i += 1
    y_pos = float(input[ychar_loc+1:i])

    return x_pos, y_pos


def extract_IJ(input):
    # given a G02 or G03 movement command line, return the I J position
    ichar_loc = input.index('I')
    i = ichar_loc+1
    while (47 < ord(input[i]) < 58) | (input[i] == '.') | (input[i] == '-'):
        i += 1
    i_pos = float(input[ichar_loc+1:i])

    jchar_loc = input.index('J')
    i = jchar_loc+1
    while (47 < ord(input[i]) < 58) | (input[i] == '.') | (input[i] == '-'):
        i += 1
    j_pos = float(input[jchar_loc+1:i])

    return i_pos, j_pos

# ---------------------------------------------------------- #
# This code is 100% not stolen from "https://github.com/flodek/Mini_pen_plotter_RaspberryPI/blob/master/Gcode_executer.py"

def run_gcode(filename):  # read and execute G code
    brain.screen.clear_screen()
    brain.screen.print("Running GCode\nPlease wait...")
    plotter.SetPenDown(False)
    for lines in open(filename, 'r'):
        print(lines)
        if lines == []:
            1  # blank lines

        elif lines[0:3] == 'G90':
            print('start')

        elif lines[0:3] == 'G20':  # working in inch
            dx /= 25.4
            dy /= 25.4
            print('Working in inch')

        elif lines[0:3] == 'G21':  # working in mm
            print('Working in mm')

        elif lines[0:3] == 'M05':
            plotter.SetPenDown(False)

        elif lines[0:3] == 'M03':
            plotter.SetPenDown(True)

        elif lines[0:3] == 'M02':
            plotter.SetPenDown(False)
            print('finished. shuting down')
            break

        elif (lines[0:3] == 'G1F') | (lines[0:4] == 'G1 F'):
            1  # do nothing

        elif (lines[0:5] == 'G01 Z'):
            plotter.SetPenDown(True)

        elif (lines[0:5] == 'G00 Z'):
            plotter.SetPenDown(False)

        # |(lines[0:3]=='G02')|(lines[0:3]=='G03'):
        elif (lines[0:3] == 'G0 ') | (lines[0:3] == 'G1 ') | (lines[0:3] == 'G00') | (lines[0:3] == 'G01'):
            # linear engraving movement
            if (lines[0:3] == 'G0 ' or lines[0:3] == 'G00'):
                engraving = False
            else:
                engraving = True

            plotter.SetPenDown(engraving)

            if (lines.find('X') != -1 and lines.find('Y') != -1):
                [x_pos, y_pos] = XYposition(lines)
                goto(x_pos, y_pos)

        elif (lines[0:3] == 'G02') | (lines[0:3] == 'G03'):  # circular interpolation
            if (lines.find('X') != -1 and lines.find('Y') != -1 and lines.find('I') != -1 and lines.find('J') != -1):
                plotter.SetPenDown(True)

                old_x_pos = x_pos
                old_y_pos = y_pos

                [x_pos, y_pos] = XYposition(lines)
                [i_pos, j_pos] = IJposition(lines)

                xcenter = old_x_pos+i_pos  # center of the circle for interpolation
                ycenter = old_y_pos+j_pos

                Dx = x_pos-xcenter
                # vector [Dx,Dy] points from the circle center to the new position
                Dy = y_pos-ycenter

                r = sqrt(i_pos**2+j_pos**2)   # radius of the circle

                # pointing from center to current position
                e1 = [-i_pos, -j_pos]
                if (lines[0:3] == 'G02'):  # clockwise
                    # perpendicular to e1. e2 and e1 forms x-y system (clockwise)
                    e2 = [e1[1], -e1[0]]
                else:  # counterclockwise
                    # perpendicular to e1. e1 and e2 forms x-y system (counterclockwise)
                    e2 = [-e1[1], e1[0]]

                # [Dx,Dy]=e1*cos(theta)+e2*sin(theta), theta is the open angle

                costheta = (Dx*e1[0]+Dy*e1[1])/r**2
                # theta is the angule spanned by the circular interpolation curve
                sintheta = (Dx*e2[0]+Dy*e2[1])/r**2

                # there will always be some numerical errors! Make sure abs(costheta)<=1
                if costheta > 1:
                    costheta = 1
                elif costheta < -1:
                    costheta = -1

                theta = acos(costheta)
                if sintheta < 0:
                    theta = 2.0*pi-theta

                # number of point for the circular interpolation
                no_step = int(round(r*theta/dx/5.0))

                for i in range(1, no_step+1):
                    tmp_theta = i*theta/no_step
                    tmp_x_pos = xcenter+e1[0] * \
                        cos(tmp_theta)+e2[0]*sin(tmp_theta)
                    tmp_y_pos = ycenter+e1[1] * \
                        cos(tmp_theta)+e2[1]*sin(tmp_theta)
                    goto(tmp_x_pos, tmp_y_pos)