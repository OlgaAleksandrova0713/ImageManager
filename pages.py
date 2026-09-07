def home_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Image Manager</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <h1>Welcome to Image Manager!</h1>

        <div>
            <a href="/upload" class="button">Upload image</a>
            <a href="/images/" class="button">View images</a>
        </div>
        
        <br><br>

        <audio controls loop>
            <source src="/static/music.mp3" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
        

    </body>
    </html>
    """

def upload_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Upload image</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <h1>Upload image</h1>

        <form action="/upload" method="post" enctype="multipart/form-data">
            <input
                type="file"
                name="image"
                accept=".jpg,.png,.gif"
                required
            >
            <button type="submit">Upload</button>
        </form>

        <p>
            <a href="/images/" class="button">View images</a>
        </p>
        
        <br><br>

        <audio controls loop>
            <source src="/static/music.mp3" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
        
    </body>
    </html>
    """

def gallery_page(image_files):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Image Gallery</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>

    <body>
        <h1>Image Gallery</h1>

        <audio controls loop>
            <source src="/static/music.mp3" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>

        <br><br>

        <div class="gallery">
    """

    for filename in image_files:
        html += f"""
            <div class="image-card">
                <img src="/images/{filename}"
                     onclick="openImage('/images/{filename}')"
                     style="width:200px; height:200px; object-fit:cover; cursor:pointer;">
                <br>
                {filename}
            </div>
        """

    html += """
            </div>

            <div id="imageModal" class="modal">
                <span class="close" onclick="closeImage()">&times;</span>
                <img id="modalImage" class="modal-content" alt="Image">
            </div>

            <script>
                function openImage(src) {
                    document.getElementById("modalImage").src = src;
                    document.getElementById("imageModal").style.display = "flex";
                }

                function closeImage() {
                    document.getElementById("imageModal").style.display = "none";
                }
            </script>

        </body>
        </html>
        """

    return html