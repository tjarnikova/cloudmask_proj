
# ch31bright_grid = np.array([[1,2,3,4],[2,3,4,1],[2,5,7,8]])
# w = np.mean(ch31bright_grid)
# y = np.std(ch31bright_grid)
import numpy as np
def meanstd(ch31bright_grid):

	import numpy as np

	rows = ch31bright_grid.shape[0]
	cols = ch31bright_grid.shape[1]

	stdar = np.zeros((rows,cols))
	meanar = np.zeros((rows,cols))

	#endrow
	er = rows - 1
	#end column
	ec = cols - 1


	for i in range(0,rows):
		for j in range(0,cols):
	 		if i == 0 or i == er or j ==0 or j ==ec:
	 			stdar[i,j] = np.nan
	 			meanar[i,j] = np.nan
	 		else:
	 			p = ch31bright_grid[i,j]
	 		
	 			a = ch31bright_grid[i-1,j-1]
	 			b = ch31bright_grid[i-1,j]
	 			c = ch31bright_grid[i-1,j+1]
	 			d = ch31bright_grid[i,j-1]
	 			e = ch31bright_grid[i,j+1]
	 			f = ch31bright_grid[i+1,j-1]
	 			g = ch31bright_grid[i+1,j]
	 			h = ch31bright_grid[i+1,j+1]
	 			testlist = [a,b,c,d,e,f,g,h,p]
	 			stdar[i,j] = np.std(testlist)
	 			meanar[i,j] = np.mean(testlist)
	 			

	return stdar, meanar
