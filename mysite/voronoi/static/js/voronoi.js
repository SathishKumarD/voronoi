$(function(){


// set the height of the search results column so the scrollbar does not appear
$('#results').height($(window).height() - $('.allheader').height());

// when a filter is selected update the hidden input fields in the form
$(".dropdown-menu.filter li a").click(function(){
	var name = $(this).parents().eq(1).attr("name");
	var prefix = $(this).attr("prefix");
	var value = $(this).attr("value");
	var element = $(this).parents().eq(2).children("a");
	if (value)
		element.find('span').text(prefix+ " < "+ value);
	else
		element.find('span').text(prefix);
	$("input[name='"+name+"']").text(value);
	$("input[name='"+name+"']").val(value);

});

// auto comple search suggestion
$( "#search2" ).autocomplete({
  source: function( request, response ) {
    $.ajax( {
      url: "/get_search_suggestions",
      data: {
        address: request.term,
        rent: $("input[name='rent']").val(),
        bus_stop_time: $("input[name='bus_stop_time']").val()
      },
      success: function( data ) {
        response( data );
      }
    } );
  },
  minLength: 0,
  select: function( event, ui ) {
    $('#search2').val(ui.item.label);
    if (ui.item.value ==='address'){
      var url = window.location.origin;
      url += "/"+ui.item.id;
      window.location.href = url;
    }
    else{
      var filterObj = getFilterObject();
      filterObj[ui.item.value] = ui.item.label;
      $('#searchType').attr('name',ui.item.value);
      $('#searchType').val(ui.item.label);
      refreshResults();
    }
    return false;
  }
} );
});



