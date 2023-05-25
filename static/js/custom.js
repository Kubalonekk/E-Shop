
function ItemsCount(){
    $.ajax({
        url: `http://127.0.0.1:8000/api/order/`,
        type: 'GET',
        mode: 'same-origin',
        processData: false,
        success: function(response){
            console.log(response)
            var html = `
            <span  id="car_items_count" class="position-absolute top-0 left-100 translate-middle badge rounded-pill bg-light text-dark">${response.get_cart_objects_quantity}</span>
            `
            $('#car_items_count').empty();
            $('#car_items_count').append(html);

           
        },
        error: function(response) {
            console.log(response);
        }

    });
}
