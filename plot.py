import numpy as np
import matplotlib.pyplot as plt
import math

def get_camber_formula_first(x, m, p):
  return (m / (p ** 2)) * ((2 * p * x) - (x ** 2))

def get_camber_formula_second(x, m, p):
  return (m / ((1 - p) ** 2)) * (1 - (2 * p) + (2 * p * x) - (x ** 2))

def get_camber_derivate_first(x, m, p):
  return ((2 * m) / (p ** 2)) * (p - x)

def get_camber_derivate_second(x, m, p):
  return ((2 * m) / ((1 - p) ** 2)) * (p - x)

def get_camber_points(m, p, no_of_points):
  x = []
  for i in range(no_of_points):
    x.append(i / no_of_points)
  y = []
  dy = []
  for i in range(no_of_points):
    if x[i] < p:
      y.append(get_camber_formula_first(x[i], m, p))
      dy.append(get_camber_derivate_first(x[i], m, p))
    else:
      y.append(get_camber_formula_second(x[i], m, p))
      dy.append(get_camber_derivate_second(x[i], m, p))
  return (x, y, dy)

def thickness_form(x, t_c_ratio):
  a0 = 0.2969
  a1 = - 0.1260
  a2 = - 0.3516
  a3 = 0.2843
  a4 = - 0.1015
  return 5 * (t_c_ratio) * ((a0 * (x ** 0.5)) + (a1 * x) + (a2 * (x ** 2)) + (a3 * (x ** 3)) + (a4 * (x ** 4)))

def get_thickness(m, p, t_c_ratio, no_of_points):
  x = []
  for i in range(no_of_points):
    x.append(i / no_of_points)
  y = []
  for i in range(no_of_points):
    y.append(thickness_form(x[i], t_c_ratio))
  return (x, y)

def plot(desig, no_of_points):

  t_c_ratio = int(desig[-2:]) / 100
  m = int(desig[-4]) / 100
  p = int(desig[-3]) / 10

  x, y_c, dy_c = get_camber_points(m, p, 100)
  thetas = []
  for dy in dy_c:
    thetas.append(math.atan(dy))
  _, y_t = get_thickness(m, p, t_c_ratio, 100)

  x_u = []
  y_u = []
  x_l = []
  y_l = []
  for i in range(len(x)):
    X = x[i]
    theta = thetas[i]
    Y_t = y_t[i]
    Y_c = y_c[i]
    x_u.append(X - Y_t * math.sin(theta))
    y_u.append(Y_c + Y_t * math.cos(theta))

    x_l.append(X + Y_t * math.sin(theta))
    y_l.append(Y_c - Y_t * math.cos(theta))

  plt.title(f"Plot for {desig}") 
  plt.xlabel("X")
  plt.ylabel("Y") 
  plt.gca().set_aspect('equal')
  plt.xlim([0, 1])
  plt.ylim([-0.25, 0.25])
  plt.plot(x, y_c, color = 'red')
  plt.plot(x_u, y_u, color = 'blue')
  plt.plot(x_l, y_l, color = 'blue')
  plt .show()

desig = input('Enter NACA 4 digit designation (Enter 4 digits): ')
plot('NACA ' + desig, 100)

