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
           var url = $("#url_add_cart").attr("data-url");
           var in_stock = $("[data-in-stock="+product_id+"]").text();

           console.log('product_id', product_id, 'in_stock', in_stock);

           data = {
            'product_id': product_id,
            }

            $.ajax({
                type: "POST",
                url: url,
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
                        $("[data-container-cart="+product_id+"]").append('<a href="#" data-link-to-cart="'+product_id+'" class="go_to_cart">go to cart</a>');
                    },
                error: function (response) {
                    }
            });
     });
});

// КОНЦЕНТРИРУЙСЯ НА МОМЕНТЕ, КОНЦЕНТРИРУЙСЯ НА ЗАДАЧЕ, КОНЦЕНТРИРУЙСЯ НА ТОМ ЧТО СЕЙЧАС ДЕЛАЕШЬ
// english -> 5 раз в неделю по 3-4 часа !!!

//1! +
// при резервировании продукта вместо кнопки
//ставить то сколько продуктов зарезервиров прольватель

//2! +
// добавление товара в корзину -> после добавления товара менять состояние кнопки

//3!
// увеличение товара в корзине -> обновлять данные на фронте
// уменьшение товара в корзине -> обновлять данные на фронте

//4!
// удаление товара из корзины

//5!
// починить кнопку search

//6!
// написать email_bealder
// добавить celery

//7!
// сверстать страницы -> home, orders, reserved product contact

//8!
// переписать на drf

//9!
// повторить все пройденные материалы
// перерешать задачи со стражеровки до автоматизма

//10!
// желательно поработать с тестами