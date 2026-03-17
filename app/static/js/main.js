document.addEventListener("DOMContentLoaded", function(){

/* REGISTER VALIDATION */

const registerForm = document.getElementById("registerForm");

if(registerForm){

registerForm.addEventListener("submit", function(e){

const name = document.getElementById("name").value.trim();
const email = document.getElementById("email").value.trim();
const password = document.getElementById("password").value;

const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

if(name.length < 2){
alert("Name must contain at least 2 characters");
e.preventDefault();
return;
}

if(!emailPattern.test(email)){
alert("Enter a valid email address");
e.preventDefault();
return;
}

if(password.length < 8){
alert("Password must be at least 8 characters long");
e.preventDefault();
return;
}

});

}


/* LOGIN VALIDATION */

const loginForm = document.getElementById("loginForm");

if(loginForm){

loginForm.addEventListener("submit", function(e){

const email = document.getElementById("email").value.trim();
const password = document.getElementById("password").value;

if(email === "" || password === ""){
alert("Please enter email and password");
e.preventDefault();
}

});

}

});

function confirmDelete(userId){
    if(confirm("Are you sure you want to delete this user?")){
        window.location.href = "/delete_user/" + userId;
    }
}
