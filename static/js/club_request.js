// get all club request buttons
const buttons = document.querySelectorAll('.club-request');

// add click event listener for all buttons
for (const button of buttons){
  button.addEventListener('click', evt => {
    // get club_id from button id
      const data = {
          club_id: evt.target.id
      }
      // send post request
      fetch('/clubrequest', {
          method: 'POST',
          body: JSON.stringify(data),
          headers: {
            'Content-Type': 'application/json',
          },
        })
        .then(response => response.text())
        // change request button if request was successful 
        .then(responseJSON => {
          evt.target.innerHTML = responseJSON;
          evt.target.disabled = true;
        });
      });
}


