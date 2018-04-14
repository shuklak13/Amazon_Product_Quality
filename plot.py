import matplotlib.pyplot as plt
 
# x-coordinates of left sides of bars 
left = [10, 20, 30, 40]
 
# heights of bars
height = [1.93, 1.5, 2.22, 1.57 ]
 
# labels for bars
tick_label = ['ten', 'twenty', 'thirty', 'fourty']
 
# plotting a bar chart
plt.bar(left, height, tick_label = tick_label, width = 8)
 
# naming the x-axis
plt.xlabel('The number of sampling rounds')
# naming the y-axis
plt.ylabel('SpeedUp')
# plot title
plt.title('Performance Evaluation - SpeedUp')
 
# function to show the plot
plt.show()