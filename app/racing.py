import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import imageio
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_agg import FigureCanvasAgg

class AnimatedLineChartService:
    def __init__(self, data):
        self.df = pd.DataFrame(data)
        
    def create_animation(self, output_filename, fps=10, duration=5):
        fig, ax = plt.subplots(figsize=(12, 6), dpi=100)
        
        months = self.df['month']
        traffic = self.df['traffic']
        sales = self.df['sales']
        
        traffic_line, = ax.plot([], [], 'b-', linewidth=2, label='Traffic')
        sales_line, = ax.plot([], [], 'r-', linewidth=2, label='Sales')
        
        ax.set_xlim(0, len(months) - 1)
        ax.set_ylim(0, max(traffic.max(), sales.max()) * 1.1)
        ax.set_xlabel('Month')
        ax.set_ylabel('Value')
        ax.set_title('Traffic and Sales Over Time')
        ax.legend()
        
        ax.set_xticks(range(len(months)))
        ax.set_xticklabels(months, rotation=45)
        
        def animate(frame):
            traffic_line.set_data(range(frame + 1), traffic[:frame + 1])
            sales_line.set_data(range(frame + 1), sales[:frame + 1])
            return traffic_line, sales_line
        
        anim = FuncAnimation(fig, animate, frames=len(months), interval=1000/fps, blit=True)
        
        # Save as GIF
        writer = imageio.get_writer(output_filename, fps=fps)
        canvas = FigureCanvasAgg(fig)
        for frame in range(len(months)):
            animate(frame)
            canvas.draw()
            image = np.frombuffer(canvas.buffer_rgba(), dtype='uint8')
            image = image.reshape((int(fig.get_figheight() * fig.dpi),
                                   int(fig.get_figwidth() * fig.dpi),
                                   4))[:, :, :3]
            writer.append_data(image)
        writer.close()
        
        plt.close(fig)
        print(f"Animation saved as {output_filename}")

def create_animated_line_chart(data, output_filename, fps=10, duration=5):
    service = AnimatedLineChartService(data)
    service.create_animation(output_filename, fps, duration)


# Sample data (replace this with your actual data)
# Data provided
data = [
    { 'month': "Jan", 'traffic': 1000, 'sales': 500 },
    { 'month': "Feb", 'traffic': 1200, 'sales': 600 },
    { 'month': "Mar", 'traffic': 1350, 'sales': 550 },
    { 'month': "Apr", 'traffic': 1500, 'sales': 700 },
    { 'month': "May", 'traffic': 1400, 'sales': 650 },
    { 'month': "Jun", 'traffic': 1600, 'sales': 800 },
    { 'month': "Jul", 'traffic': 1800, 'sales': 750 },
    { 'month': "Aug", 'traffic': 2000, 'sales': 900 },
    { 'month': "Sep", 'traffic': 1900, 'sales': 850 },
    { 'month': "Oct", 'traffic': 2100, 'sales': 1000 },
    { 'month': "Nov", 'traffic': 2300, 'sales': 1100 },
    { 'month': "Dec", 'traffic': 2500, 'sales': 1200 },
]

# Create the animated line chart
create_animated_line_chart(
    data=data,
    output_filename='traffic_sales_line_chart.gif',
    fps=5,
    duration=1
)

print("Animated line chart created. Check 'traffic_sales_line_chart.gif' in your current directory.")