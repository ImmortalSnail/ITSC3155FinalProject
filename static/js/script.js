$(document).ready(function() {
  // Add click event listener to dropdown
  $('.dropdown').click(function(event) {
    event.stopPropagation(); // Stop event from bubbling up to document
    $(this).toggleClass('active');
  });
  
  // Add click event listener to document
  $(document).click(function() {
    // Remove active class from all dropdowns
    $('.dropdown').removeClass('active');
  });
});