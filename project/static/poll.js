// There is one choice by default
form_count = 1;

// when the button 'add another' is clicked then create a new input element
$(document.body).on("click", "#add-another",function(e) {
  form_count ++;
  new_choice = $('<div class="form-group"><label>Choice ' + form_count + '</label><input type="text" class="form-control" name="choice_' + form_count + '" /></div>');
  // append the new element in your html
  $("#form_choices").append(new_choice);
})