$(function(){
  $('#my_board_contents ul[id != "tab1"]').hide();

  $('a').click(function(){

    $('#my_board_contents ul').hide();

    $($(this).attr('href')).show();

    $('.current').removeClass('current');

    $(this).addClass('current');
    return false;
  })
})
