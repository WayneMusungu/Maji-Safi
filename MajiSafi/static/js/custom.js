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
    $('.add_to_cart').on('click', function(e){
        e.preventDefault();
        
        product_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        data = {
            product_id: product_id,
        }
        

        //  Send the product_id to add to cart view using the Ajax Request
        // alert(product_id)
        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            success: function(response){
                // alert(response)
                console.log(response)
            }

        })
    })

    // PLace the cart item quantity on load

    $('.item_qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        console.log(qty)
        $('#'+the_id).html(qty)
    })

 
})
