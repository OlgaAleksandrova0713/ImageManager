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
        
        <div class="music-background"></div>
        <div class="home-page">

            <h1 class="home-title">
                📷 IMAGE MANAGER
            </h1>

            <p class="home-subtitle">
                Your personal image gallery
            </p>

            <div class="categories">

                <a href="/category/fruits" class="category-card fruits-card">
                    <div class="category-overlay">
                        <h2>FRUITS</h2>
                    </div>
                </a>

                <div class="category-card nature-card">
                    <div class="category-overlay">
                        <h2>NATURE</h2>
                    </div>
                </div>

                <div class="category-card style-card">
                    <div class="category-overlay">
                        <h2>STYLE</h2>
                    </div>
                </div>

                <div class="category-card animals-card">
                    <div class="category-overlay">
                        <h2>ANIMALS</h2>
                    </div>
                </div>

                <div class="category-card city-card">
                    <div class="category-overlay">
                        <h2>CITY</h2>
                    </div>
                </div>

                <div class="category-card other-card">
                    <div class="category-overlay">
                        <h2>OTHER</h2>
                    </div>
                </div>

            </div>

            <div class="home-buttons">
                <a href="/upload" class="home-button">
                    Upload new image
                </a>

                <a href="/images/" class="home-button">
                    View gallery
                </a>
            </div>

            <audio controls loop>
                <source src="/static/music.mp3" type="audio/mpeg">
                Your browser does not support the audio element.
            </audio>
            
<script>
    const music = document.querySelector("audio");
    const cards = document.querySelectorAll(".category-card");

    music.addEventListener("play", function() {
        cards.forEach(function(card) {
            card.classList.add("music-active");
        });
    });

    music.addEventListener("pause", function() {
        cards.forEach(function(card) {
            card.classList.remove("music-active");
        });
    });

    music.addEventListener("ended", function() {
        cards.forEach(function(card) {
            card.classList.remove("music-active");
        });
    });

    document.addEventListener("click", function startMusic() {
        music.play().catch(function(error) {
            console.log("Autoplay blocked:", error);
        });

        document.removeEventListener("click", startMusic);
    });
</script>

        </div>

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
        <link rel="stylesheet" href="/static/upload.css">
    </head>
    <body>
    
        <div class="music-background"></div>
        <div class="upload-page">
        
            <h1 class="upload-title">
                📷 UPLOAD IMAGE
            </h1>
        
        <p class="upload-subtitle">
            Add a new image to your gallery
        </p>
        
        <div class="upload-card">
            
            <form action="/upload" method="POST" enctype="multipart/form-data">
                <label class="file-label">
                    Choose an image
                </label>
                
                <input
                    type="file"
                    name="image"
                    accept=".jpg,.png,.gif"
                    required
                >
                
                <label class="file-label">
                    Choose a category
                </label>
                
                <select name="category" required>
                    <option value="">Select category</option>
                    <option value="fruits">Fruits</option>
                    <option value="nature">Nature</option>
                    <option value="style">Style</option>
                    <option value="animals">Animals</option>
                    <option value="city">City</option>
                    <option value="other">Other</option>
                </select>
                
                <button type="submit" class="home-button">
                    Upload image
                </button>
            
            </form>
            
            <a href="/images/" class="home-button">
                View images
            </a>
        
        </div>
        
        <audio controls loop>
            <source src="/static/music.mp3" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
    
     </div>

</body>
</html>
"""

def gallery_page(image_files, category=None):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Image Gallery</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>

    <body>
        <h1>{category.upper() if category else "Image Gallery"}</h1>

        <audio controls loop>
            <source src="/static/music.mp3" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>

        <br><br>

        <div class="gallery">
    """

    for filename in image_files:
        html += f"""
            <div class="image-card" 
                data-filename="{filename}"
                data-category="{category or ''}">
                
                <img src="/images/{category + '/' if category else ''}{filename}"
                     onclick="openImage('/images/{category + '/' if category else ''}{filename}')"
                     style="width:200px; height:200px; object-fit:cover; cursor:pointer;">
                     
                <div class="image-name">
                    {filename}
                </div>

                <br><br>

                <button type="button"
                        class="menu-button"
                        title="Actions"
                        onclick="openActionsMenu(this)">
                    ⋮
                </button>
                
                <div class="actions-menu">
                    <a 
                        href="/download/{category}/{filename}"
                        class="action-menu-item"
                        download
                        onclick="showDownloadMessage(this)"
                    >
                       Download
                    </a>
                    
                    <button type="button"
                            onclick="openRenameFromMenu(this)">
                        Rename
                    </button>
                    
                    <button type="button"
                            onclick="openDeleteFromMenu(this)">
                        Delete
                    </button>
                </div>
                
   
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
    
    function openActionsMenu(button) {
        const card = button.closest(".image-card");
        const menu = card.querySelector(".actions-menu");
        
        document.querySelectorAll(".actions-menu").forEach(function(item) {
            if (item !== menu) {
                item.style.display = "none";
            }
        });
        
        if (menu.style.display === "block") {
            menu.style.display = "none";
       } else {
           menu.style.display = "block";
       }
    }
    
    function openDownloadFromMenu(button) {
        const card = button.closest(".image-card");
        const filename = card.dataset.filename;
        const category = card.dataset.category;

        const link = document.createElement("a");
        link.href = `/download/${encodeURIComponent(category)}/${encodeURIComponent(filename)}`;
        link.download = filename;

        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        button.closest(".actions-menu").style.display = "none";
    }
    
    function openRenameFromMenu(button) {
        const card = button.closest(".image-card");
        const filename = card.dataset.filename;
        
        button.closest(".actions-menu").style.display = "none";
        
        openRenameModal(
            `/rename/${encodeURIComponent(card.dataset.category)}/${encodeURIComponent(filename)}`,
            card
        );
    }
    
    function openDeleteFromMenu(button) {
        const card = button.closest(".image-card");
        const category = card.dataset.category;
        const filename = card.dataset.filename;
        
        button.closest(".actions-menu").style.display = "none";

        openDeleteModal(
             `/delete/${encodeURIComponent(category)}/${encodeURIComponent(filename)}`,
            card
        );
    }
    
    document.addEventListener("click", function(event) {
        if (!event.target.closest(".image-card")) {
            document.querySelectorAll(".actions-menu").forEach(function(menu) {
                menu.style.display = "none";
            });
        }
    });
    
    let deleteUrl = "";
    let deleteCard = null;

    function openDeleteModal(url, card) {
        deleteUrl = url;
        deleteCard = card;
        
        document.getElementById("deleteModal").style.display = "flex";
    }

    function closeDeleteModal() {
        document.getElementById("deleteModal").style.display = "none";
    }
    
    document.getElementById("deleteForm").addEventListener(
        "submit",
        async function(event) {
        
            event.preventDefault();
        
            if (!deleteUrl || !deleteCard) {
                return;
            }
            
            try {
                const response = await fetch(deleteUrl, {
                    method: "POST"
                });
                
            if (!response.ok) {
                console.error(
                    "Delete failed:",
                    response.status
                );
                return;
            }
        
        showMessage(
            "Image deleted successfully!",
            deleteCard
        );
        
        deleteCard.remove();
            
        closeDeleteModal();
        
            
        } catch (error) {
            console.error(
                "Delete error:",
                error
            );
        }
    }
);

function showMessage(message, card) {
    const messageBox = document.createElement("div");
            
    messageBox.textContent = message;
    messageBox.className = "message-box";
    
    document.body.appendChild(messageBox);
            
    setTimeout(function() {
        messageBox.remove();
    }, 2500);
}

function showDownloadMessage(link) {
    setTimeout(function() {
        showMessage(
            "Image downloaded successfully!",
            link.closest(".image-card")
        );
    }, 3000);
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
                    renameCard.querySelector(".image-name");

                if (filenameElement) {
                    filenameElement.textContent =
                        finalFilename;
                }


                const image =
                    renameCard.querySelector("img");

                if (image) {
                    const category =
                        renameCard.dataset.category;
                        
                    image.src =
                        `/images/${category}/${encodedFilename}`;

                    image.onclick = function() {
                        openImage(
                            `/images/${category}/${encodedFilename}`
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