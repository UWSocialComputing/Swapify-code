document.addEventListener("DOMContentLoaded", function() {
    // Get all Sonny item containers
    var sonnyContainers = document.querySelectorAll(".item-list li");

    // Add click event listener to each Sonny item container
    sonnyContainers.forEach(function(container) {
        container.addEventListener("click", function() {
            // Get Sonny Angel details
            var name = container.querySelector("h3").textContent;
            var series = container.querySelector("p:nth-of-type(1)").textContent;
            var category = container.querySelector("p:nth-of-type(2)").textContent;
            var mrk_value = container.querySelector("p:nth-of-type(3)").textContent;
            var imageSrc = container.querySelector("img").src;

            // Update modal content
            var modalTitle = document.querySelector("#myModal .modal-content h2");
            modalTitle.textContent = name;

            var modalDetails = document.querySelector("#myModal .modal-content #modal-details");
            modalDetails.innerHTML = `
                <img src="${imageSrc}" alt="${name}">
                <p>${series}</p>
                <p>${category}</p>
                <p>${mrk_value}</p>
            `;

            // Open the modal
            var modal = document.getElementById("myModal");
            modal.style.display = "block";
        });
    });

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
        var modal = document.getElementById("myModal");
        modal.style.display = "none";
    };

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        var modal = document.getElementById("myModal");
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };
});

/**
     //for editing
    document.addEventListener('DOMContentLoaded', () => {
        const editButtons = document.querySelectorAll('.editButton');

        editButtons.forEach(button => {
            button.addEventListener('click', function () {
                const targetFormId = this.getAttribute('data-target-form');
                const targetForm = document.getElementById(targetFormId);
                if (targetForm.style.display === 'none' || targetForm.style.display === '') {
                    targetForm.style.display = 'block';
                }
            });
        });
    });

    //for trading
    document.querySelectorAll('.tradeButton').forEach(button => {
        button.addEventListener('click', function () {
            const itemId = this.getAttribute('data-item-id');
            const itemImages = document.querySelectorAll(`.item-${itemId}`);
            itemImages.forEach(image => {
                if (image.classList.contains('darkened')) {
                    image.classList.remove('darkened');
                } else {
                    image.classList.add('darkened');
                }
            });
            // Send a request to the server to update the trade status
            fetch(`/toggle_trade/${itemId}`, {method: 'POST'})
                .then(response => {
                    if (response.ok) {
                        location.reload();
                    } else {
                        console.error('Failed to update trade status');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        });
    });
 **/