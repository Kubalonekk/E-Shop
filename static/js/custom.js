// function getData(){

//     var tablica = [];
//     $.ajax({
//         url: 'http://127.0.0.1:8000/api/shopping_cart/',
//         type: 'GET',
//         success: function(response) {
//             console.log(response);
//             $("#test").empty();
//             $.each(response, function(index, item) {
//                 var obj = new Object();
//                 obj.slug = item.item.slug;
//                 obj.item_variant = item.item_variant.id;
//                 tablica.push(obj);
//                 var html = `
//                 <div id="${item.item_variant.id}">
//                 <div class="card rounded-3 mb-4">
//                     <div class="card-body p-4">
//                       <div class="row d-flex justify-content-between align-items-center">
//                         <div id="img-${item.item_variant.id}" class="col-md-2 col-lg-2 col-xl-2">
//                         <img src="${item.item.main_img}" class="img-fluid rounded-3" alt="Cotton T-shirt">
//                         </div>
                        
//                         <div class="col-md-3 col-lg-3 col-xl-3">
//                           <p class="lead fw-normal mb-2"><a  class="text-dark" href="">${item.item.title}</a></p>
//                           ${item.item_variant.size === null ? '<p><span class="text-muted"></span>' : `<p><span class="text-muted">Rozmiar:${item.item_variant.size.size}</span>`}
//                         </div>
//                         <div class="col-md-3 col-lg-3 col-xl-2 d-flex">
//                           <button type="button" id="decrease" data="${item.id}" class="btn btn-outline-secondary btn-number btn-sm">
//                             <span class="fa fa-minus"></span>
//                         </button>
//                           <p>${item.quantity}</p>
//                           <button type="button" id="increase" data="${item.id}" class="btn btn-outline-secondary btn-number btn-sm">
//                             <span class="fa fa-plus"></span>
//                         </button>
//                         </div>
//                         <div class="col-md-3 col-lg-2 col-xl-2 offset-lg-1">
//                           <h5 class="mb-0">${item.get_total} PLN</h5>
//                         </div>
//                         <div class="col-md-1 col-lg-1 col-xl-1 text-end">
//                           <button  data="${item.id}" id="delete" type="button" class="btn btn-outline-danger">
//                             <i class="fas fa-trash fa-lg"></i></a>
//                           </button>
//                         </div>
//                       </div>
//                     </div>
//                   </div>
//                 </div>
//                 `
                
//                 $('#test').append(html);
//             });
//         },
//         error: function(response) {
//             console.log(response);
//         }
//       });
//     }
    


// $(document).on('click', '#increase', function(e){
//     var id = $(this).attr('data');
//     $.ajax({
//         url: `http://127.0.0.1:8000/api/single_item_cart/${id}/`,
//         type: 'PUT',
//         headers: {'X-CSRFToken': csrftoken},
//         mode: 'same-origin',
//         processData: false,
//         success: function(response){
//           updateData(response);
           
//         },
//         error: function(response) {
//             console.log(response);
//         }

//     });
// })

// $(document).on('click', '#delete', function(e){
//   var id = $(this).attr('data');
//   $.ajax({
//       url: `http://127.0.0.1:8000/api/remove_item_from_cart/${id}/`,
//       type: 'DELETE',
//       headers: {'X-CSRFToken': csrftoken},
//       mode: 'same-origin',
//       processData: false,
//       success: function(response){
//         $(`#${response.data.item_variant.id}`).fadeOut(400);
         
//       },
//       error: function(response) {
//           console.log(response);
//       }

//   });
// })


// $(document).on('click', '#decrease', function(e){
//   var id = $(this).attr('data');
//   $.ajax({
//       url: `http://127.0.0.1:8000/api/single_item_cart/${id}/`,
//       type: 'DELETE',
//       headers: {'X-CSRFToken': csrftoken},
//       mode: 'same-origin',
//       processData: false,
//       success: function(response){
//         updateData(response);
         
//       },
//       error: function(response) {
//           console.log(response);
//       }

//   });
// })

// function updateData(response){
//   console.log(response)
//   var html = `
 
//   <div class="card rounded-3 mb-4">
//       <div class="card-body p-4">
//         <div class="row d-flex justify-content-between align-items-center">
//           <div id="img-${response.data.item_variant.id}" class="col-md-2 col-lg-2 col-xl-2">
//           <img src="${response.data.item.main_img}" class="img-fluid rounded-3" alt="Cotton T-shirt">
//           </div>
          
//           <div class="col-md-3 col-lg-3 col-xl-3">
//             <p class="lead fw-normal mb-2"><a  class="text-dark" href="">${response.data.item.title}</a></p>
//             ${response.data.item_variant.size === null ? '<p><span class="text-muted"></span>' : `<p><span class="text-muted">Rozmiar:${response.data.item_variant.size.size}</span>`}
//           </div>
//           <div class="col-md-3 col-lg-3 col-xl-2 d-flex">
//             <button type="button" id="decrease" data="${response.data.id}" class="btn btn-outline-secondary btn-number btn-sm">
//               <span class="fa fa-minus"></span>
//           </button>
//             <p>${response.data.quantity}</p>
//             <button type="button" id="increase" data="${response.data.id}" class="btn btn-outline-secondary btn-number btn-sm">
//               <span class="fa fa-plus"></span>
//           </button>
//           </div>
//           <div class="col-md-3 col-lg-2 col-xl-2 offset-lg-1">
//             <h5 class="mb-0">${response.data.get_total} PLN</h5>
//           </div>
//           <div class="col-md-1 col-lg-1 col-xl-1 text-end">
//             <button  data="${response.data.id}" id="delete" type="button" class="btn btn-outline-danger">
//               <i class="fas fa-trash fa-lg"></i></a>
//             </button>
//           </div>
//         </div>
//       </div>
//     </div>
//   `
//   if (response.data.quantity === 0) {
//     $(`#${response.data.item_variant.id}`).fadeOut(400);
//   } else {
//     $(`#${response.data.item_variant.id}`).empty();
//     $(`#${response.data.item_variant.id}`).append(html);
//   }  

// }


// function itemsCount(){
//     $.ajax({
//         url: `http://127.0.0.1:8000/api/order/`,
//         type: 'GET',
//         mode: 'same-origin',
//         processData: false,
//         success: function(response){
//             console.log(response)
//             var html = `
//             <span  id="car_items_count" class="position-absolute top-0 left-100 translate-middle badge rounded-pill bg-light text-dark">${response.get_cart_objects_quantity}</span>
//             `
//             $('#car_items_count').empty();
//             $('#car_items_count').append(html);

        
//         },
//         error: function(response) {
//             console.log(response);
//         }

//     });
//     }






// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             // Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }
// const csrftoken = getCookie('csrftoken');