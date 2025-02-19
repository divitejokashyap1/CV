import os
from django.shortcuts import render
from django.conf import settings
from pdf2image import convert_from_path

def resume_images_view(request):
    # 1) Build the absolute path to your PDF file
    pdf_path = os.path.join(settings.BASE_DIR, 'myCV' , 'static', 'cv', 'pdfs', 'resume.pdf')

    # 2) Convert PDF pages to a list of PIL images
    try:
        pages = convert_from_path(pdf_path)
    except Exception as e:
        # If there's an error (file not found, etc.), handle it
        return render(request, 'resume_images.html', {
            'images': [],
            'error': f"Could not open PDF: {e}"
        })

    # 3) Save each page as an image in MEDIA_ROOT, then collect the URLs
    image_urls = []
    for i, page in enumerate(pages):
        image_filename = f'resume_page_{i+1}.png'
        image_path = os.path.join(settings.MEDIA_ROOT, image_filename)
        
        # Save the image in PNG format
        page.save(image_path, 'PNG')
        
        # Build the URL to serve the image
        image_url = settings.MEDIA_URL + image_filename
        image_urls.append(image_url)

    # Create the context dictionary
    context = {'images': image_urls}
    
    # 4) Render the template with a list of image URLs
    return render(request, 'resume_images.html', context)