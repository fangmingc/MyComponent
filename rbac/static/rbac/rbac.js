

$(function(){
    $(".menu").click(function () {
        $(".second_menu").each(function () {
            $(this).css("display", "none")
        });
        $(this).next().css("display", "block")
    });
});