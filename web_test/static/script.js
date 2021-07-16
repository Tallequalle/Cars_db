$(document).ready(function(){
 // Show Input element
 $('.edit').click(function(){
  $('.txtedit').hide();
  $(this).next('.txtedit').show().focus();
  $(this).hide();
 });

 // Save data
 $(".txtedit").focusout(function(){
 // Get edit id, field name and value
  var id = this.id;
  var split_id = id.split("_");
  var field_name = split_id[0];
  var edit_id = split_id[1];
  var value = $(this).val();

  // Hide Input element
  $(this).hide();

  // Hide and Change Text of the container with input element
  $(this).prev('.edit').show();
  $(this).prev('.edit').text(value);

  $.ajax({
   url: '/update',
   type: 'post',
   data: { field:field_name, value:value, id:edit_id },
   success:function(response){
      if(response == 1){
         console.log('Save successfully');
      }else{
         console.log("Not saved.");
      }
   }
  });
 });
});