# views.py
from django.http import HttpResponse
import matplotlib.pyplot as plt
import io
from PIL import Image

def generate_chart(request):
    # Get parameters from request
    chart_type = request.GET.get('type', 'bar')
    data_values = [int(x) for x in request.GET.get('data', '1,2,3,4').split(',')]
    
    # Create a figure and render the chart
    plt.figure(figsize=(10, 6))
    if chart_type == 'bar':
        plt.bar(range(len(data_values)), data_values)
    elif chart_type == 'line':
        plt.plot(data_values)
    # Add more chart types as needed
    
    # Save to buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    # Convert to desired format if not PNG
    output_format = request.GET.get('format', 'png').lower()
    if output_format != 'png':
        img = Image.open(buffer)
        output_buffer = io.BytesIO()
        img.save(output_buffer, format=output_format.upper())
        output_buffer.seek(0)
        buffer = output_buffer
    
    # Return response
    return HttpResponse(
        buffer.getvalue(), 
        content_type=f'image/{output_format}'
    )