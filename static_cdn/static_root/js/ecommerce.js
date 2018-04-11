$(document).ready(function() {

  var contactForm = $(".contact-form")
  var contactFormMethod = contactForm.attr("method")
  var contactFormEndpoint = contactForm.attr("action")

  function displaySubmitting(submitBtn, defaultText, doSubmit) {
    if (doSubmit) {
      submitBtn.addClass("disabled")
      submitBtn.html("<i class='fa fa-spin fa-spinner'></i> Sending...")
    }
    else {
      submitBtn.removeClass("disabled")
      submitBtn.html(defaultText)
    }
  }

  contactForm.submit(function(event) {
    event.preventDefault()
    var contactFormSubmitBtn = contactForm.find("[type='submit']")
    var contactFormSubmitTxt = contactFormSubmitBtn.text()
    var contactFormData = contactForm.serialize()
    var thisForm = $(this)
    displaySubmitting(contactFormSubmitBtn, "", true)
    $.ajax({
      method: contactFormMethod,
      url: contactFormEndpoint,
      data: contactFormData,
      success: function(data) {
        contactForm[0].reset()
        $.alert({
          title: "Success!",
          content: data.message,
          theme: "modern",
        })
        setTimeout(function(){
          displaySubmitting(contactFormSubmitBtn,contactFormSubmitTxt, false)
        }, 2000)
      },
      error: function(error) {
        console.log(error.responseJSON)
        var jsonData = error.responseJSON
        var msg = ""

        $.each(jsonData, function(key, value) {
          msg +=  key + ": " + value[0].message + "<br/>"
        })
        $.alert({
          title:"Errors",
          content: msg,
          theme: "modern",
        })
      }
    })


  })





  var searchForm = $(".search-form")
  var searchInput = searchForm.find("[name='q']") // input name = 'q'
  var typingTimer;
  var typingInterval = 500 // .5 seconds
  var searchBtn = searchForm.find("[type='submit']")
  searchInput.keyup(function(event) {
      clearTimeout(typingTimer)
      typingTimer = setTimeout(performSearch, typingInterval)
  })

  function displaySearching() {
    searchBtn.addClass("disabled")
    searchBtn.html("<i class='fa fa-spin fa-spinner'></i> Searching...")
  }

  function performSearch() {
    displaySearching()
    var query = searchInput.val()
    setTimeout(function() {
      window.location.href = '/search/?q=' + query
    }, 1000)
  }

  var productForm = $(".form-product-ajax")

  productForm.submit(function(event) {
    event.preventDefault()
    console.log("Form is not sending")
    var thisForm = $(this)
    var actionEndpoint = thisForm.attr("data-endpoint")
    var httpMethod = thisForm.attr("method")
    var formData = thisForm.serialize();

    $.ajax({
      url: actionEndpoint,
      method: httpMethod,
      data: formData,
      success: function(data) {
        console.log("success")
        console.log(data)
        console.log("Added", data.added)
        console.log("Removed", data.removed)
        var submitSpan = thisForm.find(".submit-span")
        if (data.added) {
          submitSpan.html("<button type=submit class='btn btn-link btn-sm' style='padding:0px; cursor: pointer;'>Remove?</button>")
        }
        else {
          submitSpan.html("<button class='btn btn-success'>Add to Cart</button>")
        }
        var currentPath = window.location.href
        if (currentPath.indexOf("cart") != -1) {
          refreshCart()
        }
        console.log("Count:",data.cartItemCount)
        var cartItemCount = $(".cart-item-count")
        cartItemCount.text(data.cartItemCount)
      },
      error: function(errorData) {
        console.log("error")
        console.log(errorData)
        $.alert({
            title: 'Error with Form Submission',
            content: errorData,
            theme: 'modern',
            type: 'green',
        });
      }
    })
  })

  function refreshCart() {
    console.log("in current cart")
    var cartTable = $(".cart-table")
    var cartBody = cartTable.find(".cart-body")
    //cartBody.html("<h1>Changed</h1>");

    var productRows = cartBody.find(".cart-products")
    console.log(productRows.html)

    var currentUrl = window.location.href
    var refreshCartUrl = '/api/cart/'
    var refreshCartMethod = "GET"
    var data = {}
    $.ajax({
      url: refreshCartUrl,
      method: refreshCartMethod,
      data: data,
      success: function(data){
        console.log("success")
        console.log(data)
        var hiddenCartItemRemoveForm = $(".cart-item-remove-form")
        //console.log("Length: ", data.products.length)
        if (data.products.length > 0) {
          productRows.html(" ")
          //cartBody.prepend("<tr><td colspan=3>Coming Soon</td></tr>")
          i = data.products.length
          $.each(data.products, function(index, value) {
              console.log(value)
              var newCartItemRemove = hiddenCartItemRemoveForm.clone()
              newCartItemRemove.find(".cart-item-product-id").val(value.id)
              newCartItemRemove.css("display", "block")
              cartBody.prepend("<tr><th scope=\"row\">" + i +
                              "</th><td><a href='" + value.url +
                              "'>" + value.name + "</a>"
                              +newCartItemRemove.html() + "</td><td>" +
                              value.price + "</td></tr>")
              i--
          })

          cartBody.find(".cart-subtotal").text(data.sub_total)
          cartBody.find(".cart-total").text(data.total)
          //productRows.html("<tr><td colspan=3>Coming Soon</td></tr>")
        }
        else {
          window.location.href = currentUrl
        }
      },
      error: function(errorData) {
        console.log("error")
        console.log(errorData)
        $.alert({
            title: 'Error with Refreshing data',
            content: errorData,
            theme: 'modern',
            type: 'green',
        });
      }
    })
  }
})
