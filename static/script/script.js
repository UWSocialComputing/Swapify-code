document.addEventListener("DOMContentLoaded", function() {
    // Get all Sonny item containers
    var sonnyContainers = document.querySelectorAll(".sonny_items_container");

    // Add click event listener to each Sonny item container
    sonnyContainers.forEach(function(container) {
        container.addEventListener("click", function() {
            // Get Sonny Angel details
            var name = container.querySelector("h5").textContent;
            var series = container.querySelector("p:nth-of-type(1)").textContent;
            var category = container.querySelector("p:nth-of-type(2)").textContent;
            var mrk_value = container.querySelector("p:nth-of-type(3)").textContent;
            var userLink = container.querySelector(".listing-info a").href; // Get the user profile link
            var user = container.querySelector(".listing-info a").textContent; // Get the
            var imageSrc = container.querySelector("img").src;

            // Update modal content
            var modalTitle = document.querySelector("#myModal .modal-content h2");
            modalTitle.textContent = name;

            var modalDetails = document.querySelector("#myModal .modal-content #modal-details");
            modalDetails.innerHTML = `
                <img src="${imageSrc}" alt="${name}">
                <p><a href="${userLink}">${user}</a></p>
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