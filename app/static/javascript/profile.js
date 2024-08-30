// Mudar a password
let button_mudarPass = document.getElementById('change-password');
button_mudarPass.addEventListener('click', ()=> {
    let old_password = document.getElementById('old-password');
    let new_password = document.getElementById('new-password');
    let confirm_password = document.getElementById('confirm-password');

    if((new_password.value != confirm_password.value) || new_password.value.length < 8 || confirm_password.value.length < 8){
        new_password.style.borderColor = 'red';
        confirm_password.style.borderColor = 'red';
    }
    else{
        new_password.style.borderColor = 'white';
        confirm_password.style.borderColor = 'white';
        const email = $( "#email-input" ).val();
        $.ajax({
            type: "POST",
            url: "/profile",
            data: {
                'op': '4',
                'email': email,
                'old-password': old_password.value,
                'new-password': new_password.value,
                'confirm-password': confirm_password.value
            },
            success: function (request) {
                console.log(request);
                if(request.status === 404) {
                    old_password.style.borderColor = 'red';
                }
                else if(request.status === 200){
                    alert('Sucesso');
                }
            }
        });
        old_password.value = '';
        new_password.value = '';
        confirm_password.value = '';
    }
})