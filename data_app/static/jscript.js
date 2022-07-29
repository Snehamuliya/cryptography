// nav and its tab start

function showtab(tabs) {
      var tab = tabs;
      switch (tab) //this switch case replaces the tabContent
      {
        case "tab-1":
          document.getElementById('tab-container').innerHTML = document.getElementById("tab-1").innerHTML;
          break;
        case "tab-2":
          document.getElementById('tab-container').innerHTML = document.getElementById("tab-2").innerHTML;
          break;
        case "tab-3":
          document.getElementById('tab-container').innerHTML = document.getElementById("tab-3").innerHTML;
          break;
      }
    }

// nav and its tab close

// model code start

function openModal() {
    document.getElementById("backdrop").style.display = "block"
    document.getElementById("exampleModal").style.display = "block"
    document.getElementById("exampleModal").classList.add("show")
}
function closeModal() {
    document.getElementById("backdrop").style.display = "none"
    document.getElementById("exampleModal").style.display = "none"
    document.getElementById("exampleModal").classList.remove("show")
}
// Get the modal
var modal = document.getElementById('exampleModal');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    closeModal()
  }
}

// model code end