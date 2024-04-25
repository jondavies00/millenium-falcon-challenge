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
            calculateOdds(jsonData).then(data => {if (data) {
                displayOdds(data)
            }})
           ;
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

async function calculateOdds(jsonData) {
    // Implement your logic to calculate odds from JSON data
    // For example:
    // return jsonData.someProperty / jsonData.anotherProperty;
    console.log("Requesting");
    const response = await fetch('http://localhost:80/solver/odds' ,{
        method : "POST",
        headers : { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
         },
        body : JSON.stringify({
            "empire_config":{
            "countdown": 8, 
            "bounty_hunters": [
              {"planet": "Hoth", "day": 6 }, 
              {"planet": "Hoth", "day": 7 },
              {"planet": "Hoth", "day": 8 }
            ]
          }})
  
      });
    const json_ = await response.json()
    console.log(json_);
    return json_["odds"];
    // .then(response => r= response.json())
    // .then(data => console.log(data))
    // .catch(error => console.error('Error:', error));
    // console.log(r)
    // return r
    
}