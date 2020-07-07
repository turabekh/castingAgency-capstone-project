function setJwt(token) {
    localStorage.setItem("JWT_TOKEN", token)
}

function getJWT(){
    jwt = localStorage.getItem("JWT_TOKEN") || null;
    return jwt;
}

function logout() {
    localStorage.setItem("JWT_TOKEN", null)
}

function getAndSetJWTFromURLHash() {
    activeToken = document.querySelector("#active-token");
    var hashToken = window.location.hash;
    console.log("hash", hashToken)
    var lst = hashToken.split("=");
    if (lst.includes("#access_token")) {
        setJwt(("Bearer " + lst[1].split("&")[0]))
    }
    else {
        logout();
    }

}

getAndSetJWTFromURLHash()
var jwt_token = getJWT();
if (jwt_token) {
    document.querySelector("#active-token").textContent = jwt_token
}
