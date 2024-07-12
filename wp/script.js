// Function to update the content based on the selected dropdown option
function updateContent() {
    const dropdown = document.getElementById('dropdown');
    const selectedOption = dropdown.value;

    // Fetch the JSON data
    fetch('/path/to/data.json')
        .then(response => response.json())
        .then(data => {
            const options = data.options;
            console.log('Data fetched:', options); // Debugging output

            // Find the selected option's data in the JSON
            const selectedData = options.find(option => option.id === selectedOption);

            if (selectedData) {
                console.log('Selected data:', selectedData); // Debugging output

                // Update the image and text content
                document.getElementById('content-image').src = selectedData.src;
                document.getElementById('content-title').textContent = selectedData.title;
                document.getElementById('content-paragraph1').textContent = selectedData.paragraph1;
                document.getElementById('content-paragraph2').textContent = selectedData.paragraph2;
            } else {
                console.warn('No data found for selected option:', selectedOption); // Debugging output
            }
        })
        .catch(error => console.error('Error fetching the JSON data:', error));
}

// Function to populate the dropdown options
function populateDropdown() {
    const dropdown = document.getElementById('dropdown');

    // Fetch the JSON data
    fetch('/path/to/data.json')
        .then(response => response.json())
        .then(data => {
            const options = data.options;
            console.log('Data fetched:', options); // Debugging output

            // Populate the dropdown with options
            options.forEach(option => {
                const optionElement = document.createElement('option');
                optionElement.value = option.id;
                optionElement.textContent = option.title;
                dropdown.appendChild(optionElement);
            });

            console.log('Dropdown populated:', dropdown); // Debugging output
        })
        .catch(error => console.error('Error fetching the JSON data:', error));
}

// Wait for the DOM to fully load before executing the script
document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM fully loaded and parsed'); // Debugging output

    // Populate the dropdown with options
    populateDropdown();
});
