/**
 * Created by Bulat on 07.07.2016.
 */
$(document).ready(function(){
    $('#patients_list li span').hover(function() {
          $(this).stop().animate({ fontSize : '18px' });
    },
    function() {
          $(this).stop().animate({ fontSize : '16px' });
    });
});