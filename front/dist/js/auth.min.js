$(function () {
    $("#btn").click(function () {
        $(".mask-wrapper").show();
    });
    $(".close-btn").click(function () {
        $(".mask-wrapper").hide();
    })
});

$(function () {
    $(".switch").click(function () {
        var scrollWrapper = $(".scroll-wrapper");
        var currentLeft = scrollWrapper.css("left");
        currentLeft = parseInt(currentLeft);
        if(currentLeft < 0) {
            scrollWrapper.animate({"left": "0"});
            $(".signin-group").css("visibility", "visible");
            $(".signup-group").css("visibility", "hidden");
        } else {
            $(".signup-group").css("visibility", "visible");
            $(".signin-group").css("visibility", "hidden");
            scrollWrapper.animate({"left": "-400px"});
        }
    })
});