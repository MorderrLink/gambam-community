
var updateBtns = document.getElementsByClassName("update-cart");


var hiddenWarning = document.getElementsByClassName("warning")
console.log(hiddenWarning)



for(var i=0; i < updateBtns.length; i+=1) {
    updateBtns[i].addEventListener("click", function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:',productId,'action:', action)

        console.log("USER:", user)
        if (user === 'AnonymousUser') {
            console.log('User is not logged in')
        } else {
            updateUserOrder(productId, action)
        };

    }, false)

    
};
function updateUserOrder(productId, action) {
    console.log('user is logged in, sending data...')
    var url = '/update_item/'

    fetch(url, {
        method:"POST",
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body: JSON.stringify({'productId':productId, 'action':action})

    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {

        console.log("data:", data)
        location.reload()
    });
};