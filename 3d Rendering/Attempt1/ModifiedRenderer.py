"""
References: http://codentronix.com/2011/05/12/rotating-3d-cube-using-python-and-pygame/
"""  
import sys, math, pygame 
from operator import itemgetter
 
class Cube3D:
	def __init__(self, x = 0, y = 0, z = 0, width=0, height=0, depth=0, win_width = 640, win_height = 480):
		self.x, self.y, self.z, self.width, self.height, self.depth = float(x), float(y), float(z), float(width), float(height), float(depth)
		self.angle = 0
		self.transformedVertices = []
		self.vertices = [
			Point3D((-1*width)+x,height,-1*depth),
			Point3D(width+x,height,-1*depth),
			Point3D(width+x,-1*height,-1*depth),
			Point3D((-1*width)+x,-1*height,-1*depth),
			Point3D((-1*width)+x,height,depth),
			Point3D(width+x,height,depth),
			Point3D(width+x,-1*height,depth),
			Point3D((-1*width)+x,-1*height,depth)
		]
		self.z = 0
		# Define the vertices that compose each of the 6 faces. These numbers are
		# indices to the vertices list defined above.
		self.faces  = [(0,1,2,3),(1,5,6,2),(5,4,7,6),(4,0,3,7),(0,4,5,1),(3,2,6,7)]
		# Define colors for each face
		self.colors = [(255,0,255),(255,0,0),(0,255,0),(0,0,255),(0,255,255),(255,255,0)]
		self.screen = pygame.display.set_mode((win_width, win_height))
		
	def render(self, pygame):
		self.transformedVertices = []
		for v in self.vertices:
			r = v.rotateX(self.angle)
			p = r.project(self.screen.get_width(), self.screen.get_height(), 256, 4)
			self.transformedVertices.append(p)
		avg_z = self.calculateAvgZ()
		for tmp in sorted(avg_z,key=itemgetter(1),reverse=True):
			face_index = tmp[0]
			f = self.faces[face_index]
			pointlist = [(self.transformedVertices[f[0]].x, self.transformedVertices[f[0]].y), (self.transformedVertices[f[1]].x, self.transformedVertices[f[1]].y),
						 (self.transformedVertices[f[1]].x, self.transformedVertices[f[1]].y), (self.transformedVertices[f[2]].x, self.transformedVertices[f[2]].y),
						 (self.transformedVertices[f[2]].x, self.transformedVertices[f[2]].y), (self.transformedVertices[f[3]].x, self.transformedVertices[f[3]].y),
						 (self.transformedVertices[f[3]].x, self.transformedVertices[f[3]].y), (self.transformedVertices[f[0]].x, self.transformedVertices[f[0]].y)]
			pygame.draw.polygon(self.screen,self.colors[face_index],pointlist)

	def calculateAvgZ(self):
		avg_z = []
		i = 0
		for f in self.faces:
			z = (self.transformedVertices[f[0]].z + self.transformedVertices[f[1]].z + self.transformedVertices[f[2]].z + self.transformedVertices[f[3]].z) / 4.0
			avg_z.append([i,z])
			i = i + 1
		return avg_z
		
 
class Point3D:
	def __init__(self, x = 0, y = 0, z = 0):
		self.x, self.y, self.z = float(x), float(y), float(z)
 
	def rotateX(self, angle):
		""" Rotates the point around the X axis by the given angle in degrees. """
		rad = angle * math.pi / 180
		cosa = math.cos(rad)
		sina = math.sin(rad)
		y = self.y * cosa - self.z * sina
		z = self.y * sina + self.z * cosa
		return Point3D(self.x, y, z)
 
	def rotateY(self, angle):
		""" Rotates the point around the Y axis by the given angle in degrees. """
		rad = angle * math.pi / 180
		cosa = math.cos(rad)
		sina = math.sin(rad)
		z = self.z * cosa - self.x * sina
		x = self.z * sina + self.x * cosa
		return Point3D(x, self.y, z)
 
	def rotateZ(self, angle):
		""" Rotates the point around the Z axis by the given angle in degrees. """
		rad = angle * math.pi / 180
		cosa = math.cos(rad)
		sina = math.sin(rad)
		x = self.x * cosa - self.y * sina
		y = self.x * sina + self.y * cosa
		return Point3D(x, y, self.z)
 
	def project(self, win_width, win_height, fov, viewer_distance):
		""" Transforms this 3D point to 2D using a perspective projection. """
		factor = fov / (viewer_distance + self.z)
		x = self.x * factor + win_width / 2
		y = -self.y * factor + win_height / 2
		return Point3D(x, y, self.z)
 
class Simulation:
	def __init__(self, win_width = 640, win_height = 480):
		pygame.init()
 
		self.screen = pygame.display.set_mode((win_width, win_height))
		pygame.display.set_caption("463 Warehouse Project")
		self.clock = pygame.time.Clock()
		self.cubes = []
		self.cube1 = Cube3D(5,0,0,1,1,1,win_width,win_height)
		self.cubes.append(self.cube1)
		self.cube2 = Cube3D(0,0,0,1,2,1,win_width,win_height)
		self.cubes.append(self.cube2)
 
	def run(self):
		""" Main Loop """
		while 1:
			self.renderCubes()
			self.cube1.angle += 1
			self.cube2.angle -= 1
			pygame.display.flip()
 
	def renderCubes(self):
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
		self.clock.tick(50)
		self.screen.fill((0,32,0))
		for cube in self.cubes:
			cube.render(pygame)
if __name__ == "__main__":
	Simulation().run()
