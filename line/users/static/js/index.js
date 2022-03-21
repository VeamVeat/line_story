
var product_id = 1;

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

var headers = {
    "X-Requested-With": "XMLHttpRequest",
    "X-CSRFToken": getCookie("csrftoken"),
}

 $('.increase_product').click(function(e){
       var product_id = $(this).attr("data-increase-product");
       var url_increase_product = $("#url_increase_product").attr("data-url");

       console.log('product_id', product_id,
        'url_increase_product', url_increase_product);

       data = {
           'product_id': product_id,
       }

        $.ajax({
            type: "POST",
            url: url_increase_product,
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(data),
            dataType: 'JSON',
            headers: headers,
            success: function(response){
                    $("[data-container-cart="+product_id+"]").append('<a href="'+url_to_cart+'" data-link-to-cart="'+product_id+'" class="go_to_cart">go to cart</a>');
                },
            error: function (response) {
                    alert('not enough products in stock');
                }
        });
 });

 $('.diminish_product').click(function(e){
       var product_id = $(this).attr("data-diminish-product");
       var url_diminish_product = $("#url_diminish_product").attr("data-url");

       console.log('product_id', product_id,
                    'url_increase_product', url_increase_product);

       data = {
           'product_id': product_id,
       }

        $.ajax({
            type: "POST",
            url: url_increase_product,
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(data),
            dataType: 'JSON',
            headers: headers,
            success: function(response){
                    alert(response.message);
                    $("[data-add-cart="+product_id+"]").hide();
                    $("[data-container-cart="+product_id+"]").append('<a href="'+url_to_cart+'" data-link-to-cart="'+product_id+'" class="go_to_cart">go to cart</a>');
                },
            error: function (response) {
                    alert('not enough products in stock');
                }
        });
 });

