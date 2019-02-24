// This file holds the AJAX interaction functions essentially making -
// it a client side engine.

// Globals
site_url = 'http://localhost:5000'; // define the site root url here

function modalPop(which){
  var url=''; // url to fetch

  if(which == 'newProduct'){
    url='/products/new/'
  }

  $.get( site_url+url, function( data ) {
    $('.modal-content').html(data);
    $('#appModal').modal('show');
  });
}
