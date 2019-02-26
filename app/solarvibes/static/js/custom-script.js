/*================================================================================
	Item Name: Materialize - Material Design Admin Template
	Version: 4.0
	Author: PIXINVENT
	Author URL: https://themeforest.net/user/pixinvent/portfolio
================================================================================

NOTE:
------
PLACE HERE YOUR OWN JS CODES AND IF NEEDED.
WE WILL RELEASE FUTURE UPDATES SO IN ORDER TO NOT OVERWRITE YOUR CUSTOM SCRIPT IT'S BETTER LIKE THIS. */
// tabs table
$(document).ready(function(){
    $('ul.tabs').tabs({
      swipeable : true,
      responsiveThreshold : 1920
    });
	// TAB Color
	$(".tabs" ).css("background-color", themeColor);

	// TAB Indicator/Underline Color
	$(".tabs>.indicator").css("background-color", '#16b6a5');

	// TAB Text Color
	$(".tabs>li>a").css("color", '#16b6a5');

  });



$(document).ready(function(){
    $('.tooltipped').tooltip();
});
