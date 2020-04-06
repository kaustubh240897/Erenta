/* slider */


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
  	prevArrow: ".site-slider-two .prev",
  	nextArrow: ".site-slider-two .next",
  	slidesToShow:4,
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