document.querySelector("html").classList.add('js');

var fileInput  = document.querySelector( ".input-file" ),  
    button     = document.querySelector( ".input-file-trigger" ),
    the_return = document.querySelector(".file-return");

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
            console.log(jsonData); 
            // Here you can perform any operations with the JSON data
            calculateOdds(jsonData).then(odds => {if (typeof odds === "number") {
                displayOdds(odds)
            }})
           ;
        };

        reader.readAsText(file);
    } else {
        alert('Please select a file.');
    }
});  

function displayOdds(calculatedOdds) {
    console.log("attempting display")
    const oddsText = `Your calculated odds: ${calculatedOdds}%!`;
    const oddsElement = document.createElement('p');
    oddsElement.textContent = oddsText;
    oddsElement.style.color = 'yellow';
    const form = document.getElementById('content');
    form.appendChild(oddsElement);
    // document.body.appendChild(oddsElement);
}

async function calculateOdds(jsonData) {
    const response = await fetch('http://localhost:80/solver/odds' ,{
        method : "POST",
        headers : { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
         },
        body : JSON.stringify({"empire_config": jsonData})
  
      });
    const odds  = await response.json()
    console.log(`Returning ${odds}`);
    return odds;
    
}