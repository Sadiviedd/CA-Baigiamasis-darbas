document.addEventListener("DOMContentLoaded", function() {
  var rows = document.getElementsByClassName("expandable-row");
  for (var i = 0; i < rows.length; i++) {
    rows[i].addEventListener("click", function() {
      var content = this.nextElementSibling;
      content.style.display = content.style.display === "table-row" ? "none" : "table-row";
      
      var parentRow = this;
      while (parentRow && !parentRow.classList.contains("expandable-row")) {
        parentRow = parentRow.parentNode;
      }
      if (parentRow) {
        parentRow.style.backgroundColor = content.style.display === "table-row" ? "#E7E7E8" : "";
      }
    });
  }
});
