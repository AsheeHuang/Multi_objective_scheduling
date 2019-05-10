$(document).ready(function() {

  $('.select_ins').click(function(){
    var instance_num = $(this).attr('id');
    $('#dropdownMenu1').html(instance_num);
    document.getElementsByName('instance')[0].value=instance_num
    // $("#instance").removeAttr('hidden');
  })
});
