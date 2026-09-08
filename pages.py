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
            <div class="image-card" data-filename="{filename}">
                <img src="/images/{filename}"
                     onclick="openImage('/images/{filename}')"
                     style="width:200px; height:200px; object-fit:cover; cursor:pointer;">

                <br>

                <span class="filename">{filename}</span>

                <br><br>

                <button type="button"
                        class="delete-button"
                        onclick="openDeleteModal('/delete/{filename}')">
                    &times;
                </button>
                
                <a href="/download/{filename}" class="download-button" title="Download">
                    &#8595;
                </a>
                
                <button type="button"
                        class="rename-button"
                        title="Rename"
                        onclick="openRenameModal('/rename/{filename}', this.closest('.image-card'))">
                    ✎
                </button>
                
            </div>
        """

    html += """
            </div>

            <div id="imageModal" class="modal">
                <span class="close" onclick="closeImage()">&times;</span>
                <img id="modalImage" class="modal-content" alt="Image">
            </div>
            
            <div id="deleteModal" class="delete-modal">
                <div class="delete-dialog">
                     <h2>Delete image?</h2>
                     <p>Are you sure you want to delete this image?</p>
                     
                     <form id="deleteForm" method="post">
                         <button type="button"
                                 class="cancel-button"
                                 onclick="closeDeleteModal()">
                             Cancel
                         </button>
                         
                         <button type="submit"
                                 class="confirm-delete-button">
                             Delete
                         </button>
                     </form>
                </div>
            </div>
            
            <div id="renameModal" class="delete-modal">
                <div class="delete-dialog">
                    <h2>Rename image</h2>
                    
                    <form id="renameForm" method="post">
                        <input
                            type="text"
                            id="newFilename"
                            name="new_filename"
                            required
                        >
                        
                        <br><br>
                        
                        <button type="button"
                                class="cancel-button"
                                onclick="closeRenameModal()">
                            Cancel
                        </button>
                        
                        <button type="submit"
                                class="confirm-delete-button">
                            Rename
                        </button>
                    </form>
                </div>
            </div>
            
<script>

    function openImage(src) {
        document.getElementById("modalImage").src = src;
        document.getElementById("imageModal").style.display = "flex";
    }

    function closeImage() {
        document.getElementById("imageModal").style.display = "none";
    }


    function openDeleteModal(url) {
        document.getElementById("deleteForm").action = url;
        document.getElementById("deleteModal").style.display = "flex";
    }

    function closeDeleteModal() {
        document.getElementById("deleteModal").style.display = "none";
    }


    let renameUrl = "";
    let renameCard = null;


    function openRenameModal(url, card) {
        renameUrl = url;
        renameCard = card;

        const oldFilename = card.dataset.filename;

        document.getElementById("newFilename").value = oldFilename;
        document.getElementById("renameModal").style.display = "flex";
    }


    function closeRenameModal() {
        document.getElementById("renameModal").style.display = "none";
    }


    document.getElementById("renameForm").addEventListener(
        "submit",
        async function(event) {

            event.preventDefault();

            const form = event.target;
            const newFilenameInput =
                document.getElementById("newFilename");

            const newFilename =
                newFilenameInput.value.trim();

            if (!newFilename || !renameCard) {
                return;
            }

            try {
                const response = await fetch(renameUrl, {
                    method: "POST",
                    body: new URLSearchParams(new FormData(form))
                });

                if (!response.ok) {
                    console.error(
                        "Rename failed:",
                        response.status
                    );
                    return;
                }

                const oldFilename =
                    renameCard.dataset.filename;

                let finalFilename = newFilename;

                if (!newFilename.includes(".")) {
                    const dotIndex =
                        oldFilename.lastIndexOf(".");

                    if (dotIndex !== -1) {
                        finalFilename =
                            newFilename +
                            oldFilename.substring(dotIndex);
                    }
                }

                const encodedFilename =
                    encodeURIComponent(finalFilename);

                renameCard.dataset.filename =
                    finalFilename;


                const filenameElement =
                    renameCard.querySelector(".filename");

                if (filenameElement) {
                    filenameElement.textContent =
                        finalFilename;
                }


                const image =
                    renameCard.querySelector("img");

                if (image) {
                    image.src =
                        `/images/${encodedFilename}`;

                    image.onclick = function() {
                        openImage(
                            `/images/${encodedFilename}`
                        );
                    };
                }


                const downloadButton =
                    renameCard.querySelector(
                        ".download-button"
                    );

                if (downloadButton) {
                    downloadButton.href =
                        `/download/${encodedFilename}`;
                }


                const deleteButton =
                    renameCard.querySelector(
                        ".delete-button"
                    );

                if (deleteButton) {
                    deleteButton.onclick = function() {
                        openDeleteModal(
                            `/delete/${encodedFilename}`
                        );
                    };
                }


                const renameButton =
                    renameCard.querySelector(
                        ".rename-button"
                    );

                if (renameButton) {
                    renameButton.onclick = function() {
                        openRenameModal(
                            `/rename/${encodedFilename}`,
                            renameCard
                        );
                    };
                }


                closeRenameModal();

            } catch (error) {
                console.error(
                    "Rename error:",
                    error
                );
            }
        }
    );
</script>
          
</body>
</html>
"""

    return html