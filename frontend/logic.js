document.querySelector("html").classList.add('js');

var fileInput  = document.querySelector( ".input-file" ),  
    button     = document.querySelector( ".input-file-trigger" ),
    the_return = document.querySelector(".file-return");
      
// button.addEventListener( "keydown", function( event ) {  
//     if ( event.keyCode == 13 || event.keyCode == 32 ) {  
//         fileInput.focus();  
//     }  
// });
button.addEventListener( "click", function( event ) {
    fileInput.focus();
    return false;
});  
fileInput.addEventListener( "change", function( event ) {  
    const file = fileInput.files[0]; // Get the selected file

    if (file) {
        const reader = new FileReader();

        reader.onload = function(event) {
            const jsonData = JSON.parse(event.target.result);
            console.log(jsonData); // Do something with the JSON data
            // Here you can perform any operations with the JSON data
            displayOdds(calculateOdds(jsonData));
        };

        reader.readAsText(file);
    } else {
        alert('Please select a file.');
    }
    // the_return.innerHTML = this.value;  
});  

function displayOdds(calculatedOdds) {
    const oddsText = `Your calculated odds: ${calculatedOdds}`;
    const oddsElement = document.createElement('p');
    oddsElement.textContent = oddsText;
    oddsElement.style.color = 'yellow';
    const form = document.getElementById('content');
    form.appendChild(oddsElement);
    // document.body.appendChild(oddsElement);
}

function calculateOdds(jsonData) {
    // Implement your logic to calculate odds from JSON data
    // For example:
    // return jsonData.someProperty / jsonData.anotherProperty;
    return 42; // Sample value
}