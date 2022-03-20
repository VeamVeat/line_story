$(document).ready(function (){
    var product_id = 1

    function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + "=")) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }

     $('.reserved_product').click(function(e){
           product_id = $(this).attr("data-id");
           $('#notification_reserved').text('');
           console.log('product_id', product_id);
     });

    $('#popup-form-reserve-product').submit(function(e){
        e.preventDefault();
        var url = $("#url_reserve_product").attr("data-url");
        var request_method = $(this).attr('method');
        var field_number = $('#post-number').val();

        console.log('field_form', field_number, 'id', product_id);

        data = {
            'product_id': product_id,
            'number_product': field_number,
        }

        $.ajax({
            type: request_method,
            url: url,
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(data),
            dataType: 'JSON',
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken"),
              },
            success: function(response){
                    if (response.error === false){
                        $('#post-number').val('');
                        $('#notification_reserved').text(response.message);
                        console.log('done');
                        $('#close_reserve_form')[0].click();
                        $("[data-id="+product_id+"]").hide();
                        $("[data-info="+product_id+"]").text('you have reserved '+field_number+' products');
                    } else{
                        $('#post-number').val('');
                        $('#notification_reserved').text(response.message);
                        console.log('done');
                    }
                },
            error: function (response) {
                  $('#notification_reserved').text('errors');
                }
        });
        return false;
    });

    $('.add_cart_btn').click(function(e){
           product_id = $(this).attr("data-add-cart");
           var url_add_cart = $("#url_add_cart").attr("data-url");
           var url_to_cart = $("#url_go_to_cart").attr("data-url");
           var in_stock = $("[data-in-stock="+product_id+"]").text();

           console.log('product_id', product_id, 'in_stock', in_stock);

           data = {
            'product_id': product_id,
            }

            $.ajax({
                type: "POST",
                url: url_add_cart,
                contentType: 'application/json; charset=utf-8',
                data: JSON.stringify(data),
                dataType: 'JSON',
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": getCookie("csrftoken"),
                  },
                success: function(response){
                        alert(response.message);
                        $("[data-add-cart="+product_id+"]").hide();
                        $("[data-container-cart="+product_id+"]").append('<a href="'+url_to_cart+'" data-link-to-cart="'+product_id+'" class="go_to_cart">go to cart</a>');
                    },
                error: function (response) {
                    }
            });
     });
});
