// This file holds the AJAX interaction functions essentially making -
// it a client side engine.

// Globals
site_url = 'http://localhost:5000'; // define the site root url here

function modalPop(which){
  var url=''; // url to fetch

  if(which == 'newProduct'){
    url='/products/new/'
  }else if(which == 'newCategory'){
    url='/category/new/'
  }

  $.get( site_url+url, function( data ) {
    $('.modal-content').html(data);
    $('#appModal').modal('show');
  });
}

$(function(){
  // Generic popover utility function to display roll over info messages
  $(".pop").popover({ trigger: "manual" , html: true, animation:false})
  .on("mouseenter", function () {
    var _this = this;
    $(this).popover("show");
    $(".popover").on("mouseleave", function () {
      $(_this).popover('hide');
    });
  }).on("mouseleave", function () {
    var _this = this;
    setTimeout(function () {
      if (!$(".popover:hover").length) {
        $(_this).popover("hide");
      }
    }, 300);
  });
});

function doLogout(){
  $.ajax({
    url:site_url+'/gdisconnect',
    type:"GET",
    data:'',
    contentType:"application/json; charset=utf-8",
    dataType:"json",
    success: function(result){
      if(result.status == 'Disconnected'){
        location.href = site_url;
      }
    }
  });
}
