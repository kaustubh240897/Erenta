// main js


/* slider one */
// ....
 $(".slider-one")
  .not(".slick-initialized")
  .slick({
  	autoplay: true,
  	autoplaySpeed: 3000,
  	dots: true,
  	prevArrow: ".site-slider .slider-btn .prev",
  	nextArrow: ".site-slider .slider-btn .next",
  	adaptiveHeight: false,

  });

 /* second slider */

 $(".slider-two")
  .not(".slick-initialized")
  .slick({
    autoplay: true,
  	prevArrow: ".site-slider-two .prev",
  	nextArrow: ".site-slider-two .next",
  	slidesToShow:3,
  	slidesToScroll:1,
  	autoplaySpeed:3000,

  });





  $(document).ready(function () {

 
  $('.third-button').on('click', function () {

    $('.animated-icon3').toggleClass('open');
  });
});




$(".btn-group, .dropdown").hover(
                        function () {
                            $('>.dropdown-menu', this).stop(true, true).fadeIn("fast");
                            $(this).addClass('open');
                        },
                        function () {
                            $('>.dropdown-menu', this).stop(true, true).fadeOut("fast");
                            $(this).removeClass('open');
                        });


// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal

var btn = document.getElementById("myBtn");
var btn3 = document.getElementById("myBtn3");
// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn.onclick = function() {
  modal.style.display = "block";
}
// for btn3 js 
btn3.onclick = function() {
  modal.style.display = "block";
}
// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
} 