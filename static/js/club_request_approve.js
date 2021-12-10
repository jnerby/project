// get all club approval buttons
const buttons = document.querySelectorAll('.club-approval');

// add event listener for all buttons
for (const button of buttons){
    button.addEventListener('click', evt => {
        const data = {
            // get club_user_id from button id
            club_user_id: evt.target.id
        }
        // send post request
        fetch('/approval', {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json',
                },
            })
            .then(response => response.text())
            // replace button text
            .then(result => {
                evt.target.innerHTML = result;
            });
    });
}