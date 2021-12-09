const buttons = document.querySelectorAll('.club-request');

for (const button of buttons){
    button.addEventListener('click', evt => {
        const data = {
            club_id: evt.target.id
        }
        fetch('/clubrequest', {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
              'Content-Type': 'application/json',
            },
          })
          .then(response => response.text())
            // second then is to gray out button if request went throught
          .then(responseJSON => {
            evt.target.innerHTML = responseJSON;
            evt.target.disabled = true;
          });
        });
}


