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


                // subtotal, tax and the grand_total
                applyCartAmounts(
                    response.cart_amount['subtotal'],
                    response.cart_amount['tax'],
                    response.cart_amount['grand_total'],
                );

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
        cart_id = $(this).attr('id');

      
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

                applyCartAmounts(
                    response.cart_amount['subtotal'],
                    response.cart_amount['tax'],
                    response.cart_amount['grand_total'],
                );              

                // This should run only if the user is in the cart page

                if(window.location.pathname == '/cart/'){
                    removeCartItem(response.qty, cart_id);
                    checkEmptyCart();
                }

                
               
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


                applyCartAmounts(
                    response.cart_amount['subtotal'],
                    response.cart_amount['tax'],
                    response.cart_amount['grand_total'],
                );

                removeCartItem(0, cart_id)
                checkEmptyCart();
                }
            }
        })
    })

    // delete cart element if the quantity is 0

    function removeCartItem(cartItemQty, cart_id){
        if(cartItemQty <= 0){
            // remove the cart item element
            document.getElementById("cart-item-"+cart_id).remove()
        }
    }

     // Check if Cart is Empty and Display Cart is Empty 
     
     function checkEmptyCart(){
        var cart_counter = document.getElementById('cart_counter').innerHTML
        if(cart_counter == 0){
            document.getElementById("empty-cart").style.display = "block";
        }
     }

    //  Function to apply Cart Amounts
    function applyCartAmounts(subtotal, tax, grand_total){

        if(window.location.pathname == '/cart/'){

            $('#subtotal').html(subtotal)
            $('#tax').html(tax)
            $('#total').html(grand_total)
        }

    }

    $('.add_hour').on('click', function(e){
        e.preventDefault();
        // alert('test');
        var day = document.getElementById('id_day').value
        var from_hour = document.getElementById('id_from_hour').value
        var to_hour = document.getElementById('id_to_hour').value
        var is_closed = document.getElementById('id_is_closed').checked
        var csrf_token = $('input[name=csrfmiddlewaretoken]').val()
        var url = document.getElementById('add_hour_url').value

        console.log(day, from_hour, to_hour, is_closed, csrf_token)

        // Use dynamic condition

        if(is_closed){
            is_closed = 'True'
            condition = "day != ''"
        }else{
            is_closed = 'False'
            condition = "day != '' && from_hour != '' && to_hour != ''"
        }


        if(eval(condition)){
            // s   end ajax request
            $.ajax({
                type: 'POST',
                url: url,
                data: {
                    'day': day,
                    'from_hour': from_hour,
                    'to_hour': to_hour,
                    'is_closed': is_closed,
                    'csrfmiddlewaretoken':csrf_token,
                },
                success: function(response){
                    if(response.status == 'success'){
                        if(response.is_closed == 'Closed'){
                            html = '<tr><td><b>'+response.day+'</b></td><td>Closed</td><td><a href="#">Remove</a></td></tr>'
                        }
                        else{
                            // Append the opening hours time to be automatically updated when a vendor enters a day and use Javascript dynamic value we will be getting from the response
                            html = '<tr><td><b>'+response.day+'</b></td><td>'+response.from_hour+' - '+response.to_hour+'</td><td><a href="#">Remove</a></td></tr>'
                        }
                        
                        $('.opening_hours').append(html)
                        document.getElementById('opening_hours').reset();
                    }else{
                        swal(response.message, '', "error")
                    }
                    // console.log(response)
                }
            })
            console.log('add the entry')
        }else{
            swal('Please fill all the fields', '', 'info');
        }

    })

    // document ready close
        
})
