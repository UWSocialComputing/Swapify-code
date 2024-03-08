document.addEventListener("DOMContentLoaded", function() {
  // Get all item images
  var itemImages = document.querySelectorAll(".card-body .images img");

  // Add click event listener to each item image
  itemImages.forEach(function(image) {
      image.addEventListener("click", function() {
          // Get the parent div
          var parentDiv = image.closest(".card-body");
          // Get item details
          var nameElement = parentDiv.querySelector("h4");
          var name = nameElement.textContent.trim();
          var series = parentDiv.querySelector("p:nth-of-type(1)").textContent;
          var category = parentDiv.querySelector("p:nth-of-type(2)").textContent;
          var mrk_value = parentDiv.querySelector("p:nth-of-type(3)").textContent;
          var userLink = parentDiv.querySelector(".listing-info a").href;
          var user = parentDiv.querySelector(".listing-info a").textContent;
          var imageSrc = image.src;

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
