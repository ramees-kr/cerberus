
  // Table content
  var tbody = document.getElementById("url-table-body");
  
  // Clear existing content in the tbody
  tbody.innerHTML = "";
  
  // Counter for blocked URLs
  var blockedCount = 0;
  
  // Loop through the data array and generate table rows
  for (var i = 0; i < data.length; i++) {
    var row = document.createElement("tr");
  
    // Create URL cell
    var urlCell = document.createElement("td");
    urlCell.textContent = data[i].url;
    row.appendChild(urlCell);
  
    // Create Status cell
    var statusCell = document.createElement("td");
    var statusButton = document.createElement("button");
    statusButton.classList.add("status-toggle");
  
    statusButton.textContent = data[i].status;
    statusCell.appendChild(statusButton);
    row.appendChild(statusCell);
  
    // Append the row to the tbody
    tbody.appendChild(row);
  }
  
  document.getElementById("num-blocked").textContent = blockedCount;
  // Handling button click events and toggling the status
  
  var statusButtons = document.querySelectorAll(".status-toggle");
  // Select all elements with the class "status-toggle" and store them in the `statusButtons` variable
  
  statusButtons.forEach(function (button) {
    // Iterate over each button element in the `statusButtons` NodeList
  
    button.addEventListener("click", function () {
      // Add a click event listener to each button
  
      var currentStatus = button.classList.contains("unblocked")
        ? "Unblocked"
        : "Blocked";
      // Check if the button has the class "unblocked". If true, set `currentStatus` to "Unblocked"; otherwise, set it to "Blocked"
  
      var newStatus = currentStatus === "Unblocked" ? "Blocked" : "Unblocked";
      // Determine the opposite status based on the `currentStatus` value
  
      button.textContent = newStatus;
      // Update the text content of the button to reflect the new status
  
      button.classList.toggle("unblocked", newStatus === "Unblocked");
      button.classList.toggle("blocked", newStatus === "Blocked");
    });
  });
  
  // Handle search input
  var searchInput = document.getElementById("search-input");
  searchInput.addEventListener("input", function () {
    var searchText = searchInput.value.toLowerCase();
  
    var filteredData = data.filter(function (item) {
      return item.url.toLowerCase().includes(searchText);
    });
  
    renderTable(filteredData);
  });
  
  // Handle status filter
  var statusFilter = document.getElementById("status-filter");
  statusFilter.addEventListener("change", function () {
    var selectedStatus = statusFilter.value;
  
    var filteredData = data;
    if (selectedStatus !== "all") {
      filteredData = data.filter(function (item) {
        return item.status.toLowerCase() === selectedStatus;
      });
    }
  
    renderTable(filteredData);
  });
  
  // Render the table with provided data
  function renderTable(data) {
    tbody.innerHTML = "";
    var blockedCount = 0;
  
    for (var i = 0; i < data.length; i++) {
      var row = document.createElement("tr");
  
      var urlCell = document.createElement("td");
      urlCell.textContent = data[i].url;
      row.appendChild(urlCell);
  
      var statusCell = document.createElement("td");
      var statusButton = document.createElement("button");
      statusButton.classList.add("status-toggle");
  
      if (data[i].status === "Blocked") {
        statusButton.classList.add("blocked");
        blockedCount++;
      } else {
        statusButton.classList.add("unblocked");
      }
  
      statusButton.textContent = data[i].status;
      statusCell.appendChild(statusButton);
      row.appendChild(statusCell);
  
      tbody.appendChild(row);
    }
  
    document.getElementById("num-blocked").textContent = blockedCount;
  
    // Attach event listeners to the status buttons
    var statusButtons = document.querySelectorAll(".status-toggle");
    statusButtons.forEach(function (button) {
      button.addEventListener("click", function () {
        var currentStatus = button.classList.contains("unblocked")
          ? "Unblocked"
          : "Blocked";
  
        var newStatus = currentStatus === "Unblocked" ? "Blocked" : "Unblocked";
  
        button.textContent = newStatus;
        button.classList.toggle("unblocked", newStatus === "Unblocked");
        button.classList.toggle("blocked", newStatus === "Blocked");
  
            // Update the blocked count and display it
      var numBlocked = document.getElementById("num-blocked");
      blockedCount += currentStatus === "Blocked" ? -1 : 1;
      numBlocked.textContent = blockedCount;
      });
    });
  }
  
  // Initial rendering of the table
  renderTable(data);
  