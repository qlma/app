$(document).ready(function () {
    // Hide multiselect field
    $('#div_id_recipients').hide();
    // Remove all values from multiselect field
    $('#id_recipients').children().remove();
    // Init suggestive search and retrieve list of items as JSON using search function
    $("#suggestiveSearch").autocomplete({
        source: "/search",
        minLength: 1,
        delay: 200,
        autoFocus: true,
        select: function (event, ui) {
            // Show the user what options are selected
            $('#recipients_list').append('<span class="email-ids" id="' + ui.item.id + '">' + ui.item.label + '<span class="cancel-email">x</span></span>');
            // Add selected option to multiselect field
            $('#id_recipients').append('<option value="' + ui.item.id + '" selected>' + ui.item.label + '</option>');
        },
        close: function(event, ui)  {
            // Close event fires when selection options closes
            $('#suggestiveSearch')[0].value = ""; // Clear the input field 
        }
    });
});
// Remove selected recipient
$(document).on('click','.cancel-email',function(){
    // Retrieve id of selected item
    selected_to_cancel = $(this).parent().attr('id');
    // Remove selected item from multiselect options
    $("#id_recipients option[value='" + selected_to_cancel + "']").remove();
    // Remove selected item from recipients list
    $(this).parent().remove();
});