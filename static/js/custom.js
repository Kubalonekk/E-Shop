
function ItemsCount(){
    $.ajax({
        url: `http://127.0.0.1:8000/api/order/`,
        type: 'GET',
        mode: 'same-origin',
        processData: false,
        success: function(response){
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


function getData(){

    var tablica = [];
    $.ajax({
        url: 'http://127.0.0.1:8000/api/shopping_cart/',
        type: 'GET',
        success: function(response) {
            $("#products").empty();
            $.each(response, function(index, item) {
                var html = `
                <div id="${item.item_variant.id}">
                <div class="card rounded-3 mb-4">
                    <div class="card-body p-4">
                      <div class="row d-flex justify-content-between align-items-center">
                        <div id="img-${item.item_variant.id}" class="col-md-2 col-lg-2 col-xl-2">
                        <img src="${item.item.main_img}" class="img-fluid rounded-3" alt="Cotton T-shirt">
                        </div>
                        
                        <div class="col-md-3 col-lg-3 col-xl-3">
                          <p class="lead fw-normal mb-2"><a  class="text-dark" href="">${item.item.title}</a></p>
                          ${item.item_variant.size === null ? '<p><span class="text-muted"></span>' : `<p><span class="text-muted">Rozmiar:${item.item_variant.size.size}</span>`}
                        </div>
                        <div class="col-md-3 col-lg-3 col-xl-2 d-flex">
                         <i class="fas fa-minus m-1 text-primary" id="decrease" style="cursor: pointer;" data="${item.id}"></i>
                          <p>${item.quantity}</p>
                          <i class="fas fa-minus m-1 text-primary" id="increase" style="cursor: pointer;" data="${item.id}"></i>
                        </div>
                        <div class="col-md-3 col-lg-2 col-xl-2 offset-lg-1">
                          <h5 class="mb-0">${item.total} PLN</h5>
                        </div>
                        <div class="col-md-1 col-lg-1 col-xl-1 text-end">
                          <button  data="${item.id}" id="delete" type="button" class="btn btn-outline-danger">
                            <i class="fas fa-trash fa-lg"></i></a>
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                `
                
                $('#products').append(html);
            });
        },
        error: function(response) {
            console.log(response);
        }
      });
    }
    


$(document).on('click', '#increase', function(e){
    var id = $(this).attr('data');
    $.ajax({
        url: `http://127.0.0.1:8000/api/single_item_cart/${id}/`,
        type: 'PUT',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
        processData: false,
        success: function(response){
          updateData(response);
          ItemsCount();
          GetSummary()
           
        },
        error: function(response) {
            console.log(response);
        }

    });
})

$(document).on('click', '#delete', function(e){
  var id = $(this).attr('data');
  $.ajax({
      url: `http://127.0.0.1:8000/api/remove_item_from_cart/${id}/`,
      type: 'DELETE',
      headers: {'X-CSRFToken': csrftoken},
      mode: 'same-origin',
      processData: false,
      success: function(response){
        $(`#${response.data.item_variant.id}`).fadeOut(400);
        ItemsCount();
        GetSummary()
         
      },
      error: function(response) {
          console.log(response);
      }

  });
})




$(document).on('click', '#decrease', function(e){
  var id = $(this).attr('data');
  $.ajax({
      url: `http://127.0.0.1:8000/api/single_item_cart/${id}/`,
      type: 'DELETE',
      headers: {'X-CSRFToken': csrftoken},
      mode: 'same-origin',
      processData: false,
      success: function(response){
        updateData(response);
        ItemsCount();
        GetSummary()
         
      },
      error: function(response) {
          console.log(response);
      }

  });
})

function updateData(response){
  var html = `
 
  <div class="card rounded-3 mb-4">
      <div class="card-body p-4">
        <div class="row d-flex justify-content-between align-items-center">
          <div id="img-${response.data.item_variant.id}" class="col-md-2 col-lg-2 col-xl-2">
          <img src="${response.data.item.main_img}" class="img-fluid rounded-3" alt="Cotton T-shirt">
          </div>
          
          <div class="col-md-3 col-lg-3 col-xl-3">
            <p class="lead fw-normal mb-2"><a  class="text-dark" href="">${response.data.item.title}</a></p>
            ${response.data.item_variant.size === null ? '<p><span class="text-muted"></span>' : `<p><span class="text-muted">Rozmiar:${response.data.item_variant.size.size}</span>`}
          </div>
          <div class="col-md-3 col-lg-3 col-xl-2 d-flex">
          <i class="fas fa-minus m-1 text-primary" id="decrease" style="cursor: pointer;" data="${response.data.id}"></i>
            <p>${response.data.quantity}</p>
          <i class="fas fa-plus m-1 text-primary" id="increase" style="cursor: pointer;" data="${response.data.id}"></i>
          </div>
          <div class="col-md-3 col-lg-2 col-xl-2 offset-lg-1">
            <h5 class="mb-0">${response.data.total} PLN</h5>
          </div>
          <div class="col-md-1 col-lg-1 col-xl-1 text-end">
            <button  data="${response.data.id}" id="delete" type="button" class="btn btn-outline-danger">
              <i class="fas fa-trash fa-lg"></i></a>
            </button>
          </div>
        </div>
      </div>
    </div>
  `
  if (response.data.quantity === 0) {
    $(`#${response.data.item_variant.id}`).fadeOut(400);
  } else {
    $(`#${response.data.item_variant.id}`).empty();
    $(`#${response.data.item_variant.id}`).append(html);
  }  

}

function GetSummary(){
  $.ajax({
      url: `http://127.0.0.1:8000/api/order/`,
      type: 'GET',
      success: function(response){
        $("#summary").empty();
        if (response.cupon === null) {
        var summary = `
        <div class="card rounded-3 mb-4">
          <div class="card-body p-4">
            <div>
              <div class="d-inline">Do zapłaty</div>
              <div class="d-inline float-end pr-5"> ${response.cart_total} PLN</div>
            </div>
          </div>
        </div>
        `
        $('#summary').append(summary)
        } else {
          var summary = `
          <div class="card rounded-3 mb-4">
            <div class="card-body p-4">
              <div>
                <div class="d-inline">Suma</div>
                <div class="d-inline float-end pr-5">${response.cart_total_without_cupon} PLN</div>
              </div>
              <div>
                <div class="d-inline">Kupon: ${response.cupon.name}
                <button id="delete_cupon" type="button" class="btn btn-outline-danger btn-sm">
                 <i class="fas fa-trash fa-xs"></i>
                 </button></div>
                <div class="d-inline float-end pr-5 text-danger">- ${response.cupon_value} PLN</div>
              </div>
              
              <div>
                <div class="d-inline">Do zapłaty</div>
                <div class="d-inline float-end pr-5"> ${response.cart_total} PLN</div>
              </div>
            </div>
          </div>
          `
          $('#summary').append(summary);
        }
         
      },
      error: function(response) {
        console.log(response)
  
      }

  });
}
$(document).on('click', '#delete_cupon', function(e){
  var id = $(this).attr('data');
  $.ajax({
      url: `http://127.0.0.1:8000/api/cupon/`,
      type: 'DELETE',
      headers: {'X-CSRFToken': csrftoken},
      mode: 'same-origin',
      processData: false,
      success: function(response){
        GetSummary();
         
      },
      error: function(response) {
          console.log(response);
      }

  });
})

$(document).on('click', '#cuponButton', function(e){
  e.preventDefault();
  var cupon = $("#form1").val();
  console.log(cupon);
  $.ajax({
    url: `http://127.0.0.1:8000/api/cupon/`,
    type: 'POST',
    headers: {'X-CSRFToken': csrftoken},
    mode: 'same-origin',
    data: `cupon=${cupon}`,
    processData: false,
    success: function(response){
      $('#form1').val("");
      GetSummary();
      console.log(response)

      
    },
    error: function(response) {
      $('#form1').val("");
      alert(response.responseJSON.message);
        

    }

});
});







function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');
