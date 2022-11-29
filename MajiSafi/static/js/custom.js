let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //Country code IN KENYA
        componentRestrictions: {'country': ['ke']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        console.log('place name=>', place.name)
    }

        // get the address components and assign them to the fields


}

$(document).ready(function(){
    // Add  to Cart
    $('.add_to_cart').on('click', function(e){
        e.preventDefault();
        
        product_id = $(this).attr('data-id');
        url = $(this).attr('data-url');


        // No need to pass the data dictionary because by default the url will contain the product_id

        // data = {
        //     product_id: product_id,
        // }
        

        //  Send the product_id to add to cart view using the Ajax Request
        // alert(product_id)
        $.ajax({
            type: 'GET',
            url: url,
            // data: data,
            success: function(response){
                // alert(response)
                console.log(response)
                if(response.status == 'login_required'){
                    // console.log(response)

                    // Implement SweetAlert Function
                    swal(response.message, '', 'info').then(function(){
                        window.location = '/login';
                    })
                }
                if(response.status == 'Failed'){
                    swal(response.message, '', 'error')
                }else{
                     // console.log(response.cart_counter['cart_count'])
                $('#cart_counter').html(response.cart_counter['cart_count']);
                $('#qty-'+product_id).html(response.qty);

                }

            }

        })
    })

    // Place the Quantity on Each Product

    $('.item_qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        console.log(qty)
        $('#'+the_id).html(qty)
    })


    // Decrease Cart

    $('.decrease_cart').on('click', function(e){
        e.preventDefault();
        
        product_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

      
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                // alert(response)
                console.log(response)
                if(response.status == 'login_required'){
                    // console.log(response)

                    // Implement SweetAlert Function
                    swal(response.message, '', 'info').then(function(){
                        window.location = '/login';
                    })
                }
                else if(response.status == 'Failed'){
                    swal(response.message, '', 'error')

                }
                else{
                     // console.log(response.cart_counter['cart_count'])
                $('#cart_counter').html(response.cart_counter['cart_count']);
                $('#qty-'+product_id).html(response.qty);

                }
               

            }

        })
    })


    // Delete Cart


    $('.delete_cart').on('click', function(e){
        e.preventDefault();
        
        cart_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

      
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                // alert(response)
                console.log(response)
                if(response.status == 'Failed'){
                    swal(response.message, '', 'error')

                }
                else{
                     // console.log(response.cart_counter['cart_count'])
                $('#cart_counter').html(response.cart_counter['cart_count']);
                swal(response.status, response.message, "success")

                }
               

            }

        })
    })
    



 
})
